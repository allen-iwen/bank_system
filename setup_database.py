import os
import sys
import subprocess
import sqlite3
import getpass
from datetime import datetime, timedelta
import random

def print_title(text):
    print(f"\n{'=' * 60}")
    print(f" {text}")
    print(f"{'=' * 60}")

def run_command(cmd):
    print(f"执行命令: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return False

def create_env_file(db_type, mysql_password=None):
    """创建.env文件"""
    print_title("创建环境配置文件")
    
    if db_type == "sqlite":
        db_url = "sqlite:///app.db"
    else:  # mysql
        db_url = f"mysql://root:{mysql_password}@localhost/bank_customer_portrait"
    
    env_content = f"""FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-{datetime.now().strftime('%Y%m%d')}

# 数据库URL
DATABASE_URL={db_url}

# 应用相关配置
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print(f"已创建.env文件，使用{db_type}数据库")
    return True

def create_sqlite_database():
    """直接创建SQLite数据库"""
    print_title("创建SQLite数据库")
    
    db_path = "app.db"
    if os.path.exists(db_path):
        print(f"数据库文件{db_path}已存在，备份后重新创建")
        backup_path = f"{db_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.rename(db_path, backup_path)
    
    # 创建数据库连接
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(64) UNIQUE NOT NULL,
        email VARCHAR(120) UNIQUE NOT NULL,
        password_hash VARCHAR(128) NOT NULL,
        role VARCHAR(20) NOT NULL DEFAULT 'customer',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建客户表
    cursor.execute('''
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        name VARCHAR(64) NOT NULL,
        gender VARCHAR(10),
        age INTEGER,
        occupation VARCHAR(64),
        income VARCHAR(64),
        assets FLOAT DEFAULT 0.0,
        risk_preference VARCHAR(64),
        investment_horizon VARCHAR(20),
        education VARCHAR(64),
        family_status VARCHAR(64),
        financial_goals VARCHAR(128),
        customer_value FLOAT DEFAULT 3.0,
        product_preferences VARCHAR(128),
        service_frequency VARCHAR(20),
        digital_preference VARCHAR(20),
        registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    # 创建客户经理表
    cursor.execute('''
    CREATE TABLE managers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        name VARCHAR(64) NOT NULL,
        gender VARCHAR(10),
        age INTEGER,
        department VARCHAR(64),
        position VARCHAR(64),
        expertise VARCHAR(128),
        performance_score FLOAT DEFAULT 3.0,
        service_years INTEGER DEFAULT 0,
        customer_count INTEGER DEFAULT 0,
        max_customers INTEGER DEFAULT 10,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    # 创建匹配记录表
    cursor.execute('''
    CREATE TABLE matching_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        manager_id INTEGER NOT NULL,
        matching_score FLOAT DEFAULT 0.0,
        matching_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        matching_status VARCHAR(20) DEFAULT '自动匹配',
        manager_comments TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (manager_id) REFERENCES managers(id)
    )
    ''')
    
    # 提交事务
    conn.commit()
    conn.close()
    
    print("SQLite数据库创建成功")
    return True

def create_test_data_sqlite():
    """创建SQLite测试数据"""
    print_title("生成测试数据")
    
    import hashlib
    
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    
    # 清空现有数据
    cursor.execute("DELETE FROM matching_records")
    cursor.execute("DELETE FROM customers")
    cursor.execute("DELETE FROM managers")
    cursor.execute("DELETE FROM users")
    
    # 密码散列函数 (简化版)
    def generate_password_hash(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    # 创建管理员用户
    admin_password_hash = generate_password_hash('admin123')
    cursor.execute('''
    INSERT INTO users (username, email, password_hash, role)
    VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin@example.com', admin_password_hash, 'admin'))
    
    # 创建客户经理
    manager_password_hash = generate_password_hash('123456')
    managers = []
    for i in range(1, 4):  # 3个客户经理
        cursor.execute('''
        INSERT INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?)
        ''', (f'manager{i}', f'manager{i}@example.com', manager_password_hash, 'manager'))
        
        manager_user_id = cursor.lastrowid
        
        cursor.execute('''
        INSERT INTO managers (user_id, name, gender, age, department, position, expertise, performance_score, service_years)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            manager_user_id, 
            f'客户经理{i}',
            random.choice(['男', '女']),
            random.randint(28, 45),
            random.choice(['个人金融部', '企业金融部', '财富管理部']),
            random.choice(['初级经理', '中级经理', '高级经理']),
            random.choice(['个人贷款', '企业贷款', '理财产品', '外汇业务', '资产管理']),
            round(random.uniform(3.0, 5.0), 1),
            random.randint(1, 15)
        ))
        
        managers.append(cursor.lastrowid)  # 保存经理ID
    
    # 创建客户
    customer_password_hash = generate_password_hash('123456')
    customers = []
    for i in range(1, 11):  # 10个客户
        cursor.execute('''
        INSERT INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?)
        ''', (f'customer{i}', f'customer{i}@example.com', customer_password_hash, 'customer'))
        
        customer_user_id = cursor.lastrowid
        
        cursor.execute('''
        INSERT INTO customers (
            user_id, name, gender, age, occupation, income, assets, 
            risk_preference, investment_horizon, education, family_status,
            financial_goals, customer_value, product_preferences, 
            service_frequency, digital_preference
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            customer_user_id,
            f'客户{i}',
            random.choice(['男', '女']),
            random.randint(18, 70),
            random.choice(['学生', '上班族', '企业主', '自由职业', '退休人士']),
            random.choice(['5000以下', '5000-10000', '10000-20000', '20000-50000', '50000以上']),
            random.randint(10000, 10000000),
            random.choice(['保守型', '稳健型', '平衡型', '积极型', '激进型']),
            random.choice(['短期', '中期', '长期']),
            random.choice(['高中及以下', '大专', '本科', '硕士', '博士']),
            random.choice(['单身', '已婚无子女', '已婚有子女', '离异']),
            random.choice(['子女教育', '养老规划', '财富增值', '资产配置', '税务规划', '保险保障', '房产投资']),
            round(random.uniform(1.0, 5.0), 1),
            random.choice(['存款', '理财产品', '基金', '保险', '贷款', '信用卡', '外汇', '股票']),
            random.choice(['低', '中', '高']),
            random.choice(['低', '中', '高'])
        ))
        
        customers.append(cursor.lastrowid)  # 保存客户ID
    
    # 创建匹配记录
    for customer_id in customers:
        manager_id = random.choice(managers)
        
        matching_score = round(random.uniform(60.0, 95.0), 2)
        matching_time = datetime.now() - timedelta(days=random.randint(0, 30))
        
        cursor.execute('''
        INSERT INTO matching_records (
            customer_id, manager_id, matching_score, matching_time, matching_status
        )
        VALUES (?, ?, ?, ?, ?)
        ''', (
            customer_id,
            manager_id,
            matching_score,
            matching_time.strftime('%Y-%m-%d %H:%M:%S'),
            random.choice(['待确认', '已确认', '已拒绝', '自动匹配'])
        ))
    
    # 提交事务
    conn.commit()
    conn.close()
    
    print("测试数据生成完成!")
    print("\n测试账号：")
    print("管理员: admin / admin123")
    print("客户经理: manager1-3 / 123456")
    print("客户: customer1-10 / 123456")
    
    return True

def try_mysql_connection(password):
    """测试MySQL连接"""
    try:
        import pymysql
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password=password
        )
        conn.close()
        return True
    except Exception as e:
        print(f"MySQL连接测试失败: {e}")
        return False

def try_install_dependencies():
    """尝试安装依赖项"""
    print_title("安装必要依赖")
    
    # 升级pip
    run_command("pip install --upgrade pip")
    
    # 安装基础依赖
    packages = [
        "flask",
        "flask-sqlalchemy",
        "flask-login",
        "flask-migrate",
        "flask-cors",
        "flask-wtf",
        "python-dotenv",
        "email-validator"
    ]
    
    for package in packages:
        print(f"\n安装 {package}...")
        if not run_command(f"pip install {package}"):
            print(f"警告: {package} 安装失败，但继续尝试...")
    
    # 如果选择了MySQL，安装MySQL依赖
    try:
        import pymysql
        print("pymysql已安装")
    except ImportError:
        print("安装pymysql...")
        run_command("pip install pymysql")
    
    try:
        import mysqlclient
        print("mysqlclient已安装")
    except ImportError:
        print("尝试安装mysqlclient...")
        if not run_command("pip install mysqlclient"):
            print("mysqlclient安装失败，但SQLite仍然可以工作")
    
    print("依赖安装完成")

def main():
    print_title("数据库配置向导")
    print("这个脚本将帮助您配置数据库，创建表并生成测试数据。")
    print("请选择数据库类型:")
    print("1. SQLite (轻量级，无需外部数据库，默认)")
    print("2. MySQL (需要MySQL服务器)")
    
    try:
        choice = input("请选择 [1/2]: ").strip()
        if not choice:
            choice = "1"  # 默认SQLite
        
        # 安装依赖
        try_install_dependencies()
        
        if choice == "1":
            # 选择了SQLite
            create_env_file("sqlite")
            create_sqlite_database()
            create_test_data_sqlite()
        elif choice == "2":
            # 选择了MySQL
            print("\n您需要提供MySQL的root密码以创建数据库")
            mysql_password = getpass.getpass("请输入MySQL root密码: ")
            
            # 测试连接
            if try_mysql_connection(mysql_password):
                print("MySQL连接成功！")
                create_env_file("mysql", mysql_password)
                
                # 使用flask进行数据库迁移
                os.environ['DATABASE_URL'] = f"mysql://root:{mysql_password}@localhost/bank_customer_portrait"
                
                print("\n使用Flask-Migrate创建数据库...")
                run_command("flask db init")
                run_command("flask db migrate -m '初始化数据库'")
                run_command("flask db upgrade")
                
                # 生成测试数据
                run_command("""
                flask shell << EOF
                from app.utils.data_generator import generate_test_data
                generate_test_data(num_customers=10, num_managers=3)
                exit()
                EOF
                """)
            else:
                print("MySQL连接失败，是否切换到SQLite? (y/n)")
                fallback = input().strip().lower()
                if fallback == 'y':
                    create_env_file("sqlite")
                    create_sqlite_database()
                    create_test_data_sqlite()
                else:
                    print("设置中止，请检查MySQL连接信息后重试")
                    return
        else:
            print("无效的选择，默认使用SQLite")
            create_env_file("sqlite")
            create_sqlite_database()
            create_test_data_sqlite()
        
        print_title("设置完成")
        print("数据库设置完成，您可以通过以下命令运行应用:")
        print("1. 启动后端: flask run")
        print("2. 启动前端: npm run dev")
        
        start = input("是否现在启动应用? (y/n): ").strip().lower()
        if start == 'y':
            if sys.platform.startswith('win'):
                subprocess.Popen("start cmd /c \"flask run\"", shell=True)
                subprocess.Popen("start cmd /c \"npm run dev\"", shell=True)
            else:
                print("\n请在两个不同的终端窗口运行以下命令:")
                print("终端1: flask run")
                print("终端2: npm run dev")
    
    except KeyboardInterrupt:
        print("\n设置被用户中断")
    except Exception as e:
        print(f"\n设置过程中出错: {str(e)}")
        print("您可以尝试手动设置:")
        print("1. 编辑.env文件设置数据库连接")
        print("2. 运行 'flask db init; flask db migrate; flask db upgrade'")
        print("3. 使用 'flask shell' 运行 'from app.utils.data_generator import generate_test_data; generate_test_data()'")

if __name__ == "__main__":
    main() 