import os
import sys
import subprocess
import time

def print_header(message):
    print("\n" + "=" * 60)
    print(f"  {message}")
    print("=" * 60)

def run_command(command, description=None):
    if description:
        print(f"\n>>> {description}...")
    
    print(f"执行命令: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {str(e)}")
        return False

def main():
    print_header("银行客户画像系统启动工具")
    
    # 检查虚拟环境
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if not in_venv:
        print("提示: 未检测到虚拟环境。建议在虚拟环境中运行项目。")
        choice = input("是否继续? (y/n): ").strip().lower()
        if choice != 'y':
            print("退出程序。请创建并激活虚拟环境后再运行。")
            return
    
    # 安装基础依赖
    print_header("安装基础依赖")
    if not run_command("pip install setuptools wheel", "安装基础工具"):
        return
    
    # 选择安装方式
    print_header("选择依赖安装方式")
    print("1. 安装完整依赖 (包含数据科学包，可能需要更长时间)")
    print("2. 安装轻量依赖 (移除数据科学包，安装更快)")
    
    choice = input("请选择 (1/2): ").strip()
    
    if choice == "1":
        if not run_command("pip install -r requirements.txt", "安装完整依赖"):
            print("依赖安装失败。尝试分步安装...")
            run_command("pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF Flask-Migrate Flask-CORS", "安装Flask相关依赖")
            run_command("pip install SQLAlchemy pymysql python-dotenv", "安装数据库依赖")
            run_command("pip install PyJWT passlib WTForms Werkzeug", "安装认证相关依赖")
            run_command("pip install faker", "安装Faker")
            run_command("pip install numpy pandas scikit-learn", "安装数据科学包")
    else:
        if not run_command("pip install -r requirements-light.txt", "安装轻量依赖"):
            print("依赖安装失败，尝试直接安装关键组件...")
            run_command("pip install Flask Flask-SQLAlchemy Flask-Login pymysql PyJWT", "安装关键组件")
    
    # 初始化项目
    print_header("初始化项目")
    if not os.path.exists("setup.py"):
        print("未找到setup.py文件，跳过初始化步骤。")
    else:
        if not run_command("python setup.py setup", "初始化项目数据库和测试数据"):
            print("项目初始化失败。请检查数据库配置和环境变量。")
    
    # 启动项目
    print_header("启动项目")
    print("1. 仅启动后端 (Flask API)")
    print("2. 仅启动前端 (Vite开发服务器)")
    print("3. 同时启动前端和后端 (需要两个终端)")
    
    choice = input("请选择 (1/2/3): ").strip()
    
    if choice == "1":
        run_command("flask run --port=5000", "启动Flask后端")
    elif choice == "2":
        run_command("npm run dev", "启动前端开发服务器")
    else:
        print("将依次在不同窗口启动后端和前端")
        # 在新窗口启动后端
        if sys.platform.startswith('win'):
            subprocess.Popen("start cmd /k flask run --port=5000", shell=True)
        else:
            print("请在新终端窗口执行: flask run --port=5000")
        
        time.sleep(2)  # 等待后端启动
        
        # 启动前端
        if sys.platform.startswith('win'):
            subprocess.Popen("start cmd /k npm run dev", shell=True)
        else:
            print("请在新终端窗口执行: npm run dev")
        
        print("\n前端和后端服务已在新窗口启动。")
        print("- 后端地址: http://localhost:5000")
        print("- 前端地址: http://localhost:3000")

if __name__ == "__main__":
    main() 