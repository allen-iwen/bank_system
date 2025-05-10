import os
import sys
import subprocess
import time
from flask.cli import FlaskGroup
from run import app
import pymysql

cli = FlaskGroup(app)

def create_database():
    """创建数据库（支持MySQL和SQLite）"""
    try:
        print("正在配置数据库...")
        
        # 从环境变量获取数据库连接信息
        db_url = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
        
        # 检查是SQLite还是MySQL
        if db_url.startswith('sqlite:'):
            print(f"使用SQLite数据库: {db_url}")
            # SQLite不需要创建数据库文件，SQLAlchemy会自动创建
            return True
        
        if db_url.startswith('mysql:'):
            print(f"使用MySQL数据库: {db_url}")
            
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
            
            try:
                # 连接到MySQL服务器（不指定数据库）
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
                    print(f"数据库 '{db_name}' 已存在")
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
                
        print(f"不支持的数据库URL格式: {db_url}")
        return False
    except Exception as e:
        print(f"创建数据库时出错: {str(e)}")
        return False

@cli.command("setup")
def setup():
    """设置应用：创建数据库、执行迁移、生成测试数据"""
    
    # 加载.env文件
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        print("已加载.env文件")
    
    # 创建数据库
    if not create_database():
        print("无法配置数据库，中止设置")
        return
    
    # 检查migrations/versions目录是否存在，不存在则创建
    versions_dir = os.path.join('migrations', 'versions')
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)
        print(f"已创建目录: {versions_dir}")
    
    try:
        # 初始化数据库迁移
        print("初始化数据库迁移...")
        subprocess.run(["flask", "db", "init"], check=True)
    except subprocess.CalledProcessError:
        # 如果迁移已经初始化，这一步可能会失败，但我们可以继续
        print("迁移已经初始化或初始化失败")
    
    try:
        # 生成迁移脚本
        print("生成迁移脚本...")
        subprocess.run(["flask", "db", "migrate", "-m", "初始化数据库"], check=True)
        
        # 执行迁移
        print("执行数据库迁移...")
        subprocess.run(["flask", "db", "upgrade"], check=True)
        
        # 导入数据生成模块并生成测试数据
        print("生成测试数据...")
        from app.utils.data_generator import generate_test_data
        generate_test_data(num_customers=20, num_managers=5)
        
        print("\n设置完成！您现在可以使用以下命令运行应用：")
        print("后端: flask run")
        print("前端: npm run dev")
        print("\n测试账号:")
        print("管理员: 用户名=admin, 密码=admin123")
        print("客户: 用户名=customer1-20, 密码=123456")
        print("客户经理: 用户名=manager1-5, 密码=123456")
    except Exception as e:
        print(f"设置过程中出错: {str(e)}")

if __name__ == '__main__':
    cli() 