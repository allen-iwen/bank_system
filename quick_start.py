import os
import subprocess
import sys
from pathlib import Path

def print_step(message):
    print(f"\n===== {message} =====")

def run_cmd(cmd, error_msg=None):
    print(f"执行: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        if error_msg:
            print(f"错误: {error_msg}")
        return False

def ensure_env_file():
    """确保.env文件存在并配置了SQLite"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print_step("创建.env文件")
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("SECRET_KEY=dev-key-please-change-in-production\n")
            f.write("DATABASE_URL=sqlite:///app.db\n")
            f.write("FLASK_APP=run.py\n")
        print(".env文件已创建")
    else:
        # 检查是否已经配置了SQLite
        sqlite_configured = False
        with open(env_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "sqlite:///app.db" in content:
                sqlite_configured = True
        
        if not sqlite_configured:
            print_step("更新.env文件以使用SQLite")
            with open(env_path, "a", encoding="utf-8") as f:
                f.write("\n# SQLite数据库配置\n")
                f.write("DATABASE_URL=sqlite:///app.db\n")
            print(".env文件已更新")

def setup_database():
    """删除现有数据库并创建新的数据库结构"""
    # 删除现有的SQLite数据库文件（如果存在）
    db_path = Path("app.db")
    if db_path.exists():
        print_step("删除现有数据库")
        db_path.unlink()
        print("已删除app.db")
    
    print_step("初始化数据库")
    
    # 创建migrations/versions目录（如果不存在）
    versions_dir = Path("migrations/versions")
    if not versions_dir.exists():
        versions_dir.mkdir(parents=True, exist_ok=True)
        print("已创建migrations/versions目录")
    
    # 初始化迁移
    if run_cmd("flask db init", "初始化迁移失败。如果migrations目录已存在，这是正常的，继续执行。"):
        print("迁移初始化成功")
    
    # 生成迁移脚本
    if not run_cmd("flask db migrate -m '初始化数据库'", "生成迁移脚本失败"):
        return False
    
    # 应用迁移
    if not run_cmd("flask db upgrade", "应用迁移失败"):
        return False
    
    print("数据库设置成功")
    return True

def create_test_data():
    """创建测试数据"""
    print_step("生成测试数据")
    
    # 运行Flask shell命令生成测试数据
    shell_command = """
from app.utils.data_generator import generate_test_data
generate_test_data(num_customers=10, num_managers=3)
    """
    
    with open("shell_commands.py", "w") as f:
        f.write(shell_command)
    
    if not run_cmd("flask shell < shell_commands.py", "生成测试数据失败"):
        return False
    
    # 删除临时文件
    if os.path.exists("shell_commands.py"):
        os.remove("shell_commands.py")
    
    print("测试数据生成成功")
    return True

def main():
    print_step("银行客户画像系统快速启动工具")
    
    # 确保虚拟环境已激活
    if not hasattr(sys, "real_prefix") and not (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix):
        print("警告: 您似乎没有激活虚拟环境。建议先创建并激活虚拟环境。")
        choice = input("是否继续? (y/n): ")
        if choice.lower() != "y":
            print("已取消。请先激活虚拟环境再继续。")
            return
    
    # 确保关键包已安装
    print_step("安装关键依赖")
    run_cmd("pip install -r requirements-light.txt", "安装依赖失败，尝试手动安装。")
    
    # 确保.env文件存在且配置了SQLite
    ensure_env_file()
    
    # 设置数据库
    if not setup_database():
        print("数据库设置失败，中止操作")
        return
    
    # 创建测试数据
    if not create_test_data():
        print("测试数据生成失败，但可以继续使用系统")
    
    # 启动应用
    print_step("启动应用")
    print("1. 仅启动后端 (Flask)")
    print("2. 仅启动前端 (Vite)")
    print("3. 同时启动前端和后端")
    
    choice = input("请选择启动方式 (1/2/3): ")
    
    if choice == "1":
        run_cmd("flask run", "启动Flask服务器失败")
    elif choice == "2":
        run_cmd("npm run dev", "启动Vite开发服务器失败")
    else:
        # 在Windows上打开两个命令行窗口
        if sys.platform.startswith("win"):
            subprocess.Popen("start cmd /c \"flask run\"", shell=True)
            subprocess.Popen("start cmd /c \"npm run dev\"", shell=True)
        else:
            # 在Linux/Mac上提示用户在新终端中运行命令
            print("\n请在新的终端窗口中执行以下命令启动后端:")
            print("  flask run")
            print("\n请在另一个终端窗口中执行以下命令启动前端:")
            print("  npm run dev")
    
    print("\n应用启动完成！")
    print("- 后端API地址: http://localhost:5000")
    print("- 前端页面地址: http://localhost:3000")
    print("\n测试账号:")
    print("- 管理员: 用户名=admin, 密码=admin123")
    print("- 客户: 用户名=customer1-10, 密码=123456")
    print("- 客户经理: 用户名=manager1-3, 密码=123456")

if __name__ == "__main__":
    main() 