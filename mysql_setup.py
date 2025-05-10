import os
import sys
import subprocess
import pymysql

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

def install_dependencies():
    """安装MySQL相关依赖"""
    print_title("安装MySQL依赖")
    
    # 先升级pip
    run_command("pip install --upgrade pip")
    
    # 安装必要的MySQL依赖
    packages = [
        "mysqlclient",
        "pymysql"
    ]
    
    for package in packages:
        print(f"\n安装 {package}...")
        if not run_command(f"pip install {package}"):
            print(f"警告: {package} 安装失败，尝试继续...")
    
    print("MySQL依赖安装完成")

def create_mysql_database():
    """创建MySQL数据库"""
    print_title("配置MySQL数据库")
    
    try:
        # 从环境变量获取数据库连接信息
        db_url = os.environ.get('DATABASE_URL', 'mysql://root:219213@localhost/bank_customer_portrait')
        
        # 解析连接字符串
        parts = db_url.replace('mysql://', '').split('/')
        auth_host = parts[0].split('@')
        db_name = parts[1]
        
        if ':' in auth_host[0]:
            user, password = auth_host[0].split(':')
        else:
            user = auth_host[0]
            password = ''
            
        host = auth_host[1]
        
        print(f"连接信息: 用户={user}, 主机={host}, 数据库={db_name}")
        
        # 连接到MySQL服务器（不指定数据库）
        try:
            conn = pymysql.connect(
                host=host,
                user=user,
                password=password
            )
            
            # 创建游标
            cursor = conn.cursor()
            
            # 检查数据库是否存在
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            result = cursor.fetchone()
            
            if result:
                print(f"数据库 '{db_name}' 已存在，无需创建")
            else:
                # 创建数据库
                cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"数据库 '{db_name}' 创建成功")
            
            # 关闭连接
            conn.close()
            return True
        except Exception as e:
            print(f"连接MySQL时出错: {str(e)}")
            print("请检查MySQL服务是否运行以及连接信息是否正确")
            return False
    
    except Exception as e:
        print(f"创建数据库时出错: {str(e)}")
        return False

def create_tables():
    """使用Flask-Migrate创建表"""
    print_title("创建数据库表")
    
    # 检查migrations/versions目录是否存在，不存在则创建
    if not os.path.exists("migrations"):
        os.makedirs("migrations/versions", exist_ok=True)
        print("已创建migrations/versions目录")
    
    # 初始化迁移
    if not run_command("flask db init"):
        print("初始化迁移失败，但继续尝试...")
    
    # 生成迁移脚本
    if not run_command("flask db migrate -m '初始化数据库'"):
        print("生成迁移脚本失败，但继续尝试...")
    
    # 应用迁移
    if not run_command("flask db upgrade"):
        print("应用迁移失败，但继续尝试...")
    
    print("表创建步骤完成")

def generate_test_data():
    """生成测试数据"""
    print_title("生成测试数据")
    
    # 使用Flask shell运行数据生成
    shell_command = """
from app.utils.data_generator import generate_test_data
generate_test_data(num_customers=10, num_managers=3)
"""
    
    with open("gen_data.py", "w") as f:
        f.write(shell_command)
    
    if run_command("flask shell < gen_data.py"):
        print("测试数据生成成功")
    else:
        print("测试数据生成失败，请手动检查")
    
    # 清理临时文件
    if os.path.exists("gen_data.py"):
        os.remove("gen_data.py")

def main():
    print_title("MySQL数据库设置")
    
    # 安装依赖
    install_dependencies()
    
    # 创建数据库
    if not create_mysql_database():
        print("MySQL数据库创建失败，中止设置")
        return
    
    # 先配置环境变量
    os.environ['DATABASE_URL'] = 'mysql://root:219213@localhost/bank_customer_portrait'
    
    # 创建表
    create_tables()
    
    # 生成测试数据
    generate_test_data()
    
    print_title("设置完成")
    print("MySQL数据库设置完成，您可以通过以下命令运行应用:")
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