import os
import sys
from pathlib import Path
import subprocess
import sqlite3
import shutil

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

def backup_files():
    """备份关键文件"""
    print_title("备份关键文件")
    
    # 备份config.py
    if os.path.exists("config.py"):
        shutil.copy2("config.py", "config.py.bak")
        print("已备份 config.py -> config.py.bak")

def fix_config_file():
    """修复配置文件"""
    print_title("修复配置文件")
    
    config_content = """import os
import sys
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# 确保先加载环境变量
env_path = os.path.join(basedir, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
    print("已加载环境变量")

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    # 默认使用SQLite数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 客户分类权重配置
    CUSTOMER_CLASSIFICATION_WEIGHTS = {
        'assets': 0.4,  # 总资产权重
        'demands': 0.3,  # 需求匹配度权重
        'hobbies': 0.3   # 爱好匹配度权重
    }
    
    # 客户分类阈值
    CLASSIFICATION_THRESHOLDS = {
        'A': 0.8,  # 80分以上为A类
        'B': 0.6,  # 60-80分为B类
        'C': 0.4,  # 40-60分为C类
        'D': 0.2,  # 20-40分为D类
        'E': 0.0   # 20分以下为E类
    }
    
    # 每个客户经理最大客户数量
    MAX_CUSTOMERS_PER_MANAGER = 20
"""
    
    with open("config.py", "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print("config.py 文件已修复")

def create_direct_db():
    """直接创建SQLite数据库，不依赖Flask-Migrate"""
    print_title("创建SQLite数据库")
    
    # 删除现有数据库文件
    if os.path.exists("app.db"):
        os.remove("app.db")
        print("已删除旧数据库文件")
    
    # 创建新数据库
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    
    # 创建表结构
    tables = [
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(64) UNIQUE,
            email VARCHAR(120) UNIQUE,
            password_hash VARCHAR(128),
            role VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        
        """
        CREATE TABLE managers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name VARCHAR(64),
            capabilities TEXT,
            hobbies TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """,
        
        """
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name VARCHAR(64),
            age INTEGER,
            occupation VARCHAR(64),
            total_assets FLOAT,
            demands TEXT,
            hobbies TEXT,
            classification VARCHAR(1),
            manager_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (manager_id) REFERENCES managers (id)
        )
        """,
        
        """
        CREATE TABLE matching_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            manager_id INTEGER,
            match_score FLOAT,
            match_reason TEXT,
            created_by VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (manager_id) REFERENCES managers (id)
        )
        """
    ]
    
    for table_sql in tables:
        cursor.execute(table_sql)
    
    conn.commit()
    conn.close()
    
    print("数据库表结构创建成功")

def create_test_data():
    """手动创建测试数据"""
    print_title("创建测试数据")
    
    # 从werkzeug导入密码哈希功能
    from werkzeug.security import generate_password_hash
    import json
    
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    
    # 添加管理员
    admin_password = generate_password_hash("admin123")
    cursor.execute(
        "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
        ("admin", "admin@example.com", admin_password, "admin")
    )
    
    # 添加客户经理
    demands_pool = ['储蓄', '理财', '投资', '保险', '贷款', '基金', '股票', '债券', '外汇', '信托']
    hobbies_pool = ['阅读', '旅游', '运动', '音乐', '美食', '摄影', '绘画', '书法', '园艺', '收藏', '钓鱼', '瑜伽']
    
    for i in range(1, 4):  # 创建3个客户经理
        manager_password = generate_password_hash("123456")
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (f"manager{i}", f"manager{i}@example.com", manager_password, "manager")
        )
        manager_user_id = cursor.lastrowid
        
        # 随机能力和爱好
        import random
        capabilities = random.sample(demands_pool, random.randint(3, 6))
        manager_hobbies = random.sample(hobbies_pool, random.randint(2, 5))
        
        cursor.execute(
            "INSERT INTO managers (user_id, name, capabilities, hobbies) VALUES (?, ?, ?, ?)",
            (
                manager_user_id, 
                f"客户经理{i}", 
                json.dumps(capabilities), 
                json.dumps(manager_hobbies)
            )
        )
    
    # 添加客户
    occupations = ['工程师', '教师', '医生', '律师', '会计', '设计师', '企业家', '公务员', '销售', '自由职业者']
    
    for i in range(1, 11):  # 创建10个客户
        customer_password = generate_password_hash("123456")
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (f"customer{i}", f"customer{i}@example.com", customer_password, "customer")
        )
        customer_user_id = cursor.lastrowid
        
        # 随机信息
        import random
        age = random.randint(25, 65)
        occupation = random.choice(occupations)
        total_assets = random.uniform(10000, 10000000)  # 1万到1000万
        demands = random.sample(demands_pool, random.randint(2, 5))
        customer_hobbies = random.sample(hobbies_pool, random.randint(2, 5))
        
        cursor.execute(
            "INSERT INTO customers (user_id, name, age, occupation, total_assets, demands, hobbies, classification) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                customer_user_id, 
                f"客户{i}", 
                age,
                occupation,
                total_assets,
                json.dumps(demands), 
                json.dumps(customer_hobbies),
                "C"  # 默认分类
            )
        )
    
    conn.commit()
    conn.close()
    
    print("测试数据创建成功")
    print("- 管理员账号: admin / admin123")
    print("- 客户经理账号: manager1-3 / 123456")
    print("- 客户账号: customer1-10 / 123456")

def main():
    print_title("数据库修复工具")
    
    # 步骤1: 备份文件
    backup_files()
    
    # 步骤2: 修复配置文件
    fix_config_file()
    
    # 步骤3: 创建SQLite数据库
    create_direct_db()
    
    # 步骤4: 创建测试数据
    create_test_data()
    
    print_title("修复完成")
    print("数据库问题已修复。您现在可以运行应用:")
    print("1. 启动后端: flask run")
    print("2. 启动前端: npm run dev")
    
    choice = input("是否现在启动应用? (y/n): ").strip().lower()
    if choice == 'y':
        if sys.platform.startswith('win'):
            subprocess.Popen("start cmd /c \"flask run\"", shell=True)
            subprocess.Popen("start cmd /c \"npm run dev\"", shell=True)
        else:
            print("\n请在两个不同的终端窗口运行以下命令:")
            print("终端1: flask run")
            print("终端2: npm run dev")

if __name__ == "__main__":
    main() 