#!/bin/bash
# 银行客户画像系统一键部署脚本 (Linux/Mac)
# 作者：银行客户画像系统团队
# 版本：1.0.0
# 日期：2025-05-06

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # 恢复默认颜色

# 工作目录
WORK_DIR=$(pwd)

# 函数：显示标题
show_title() {
    echo -e "\n${CYAN}======================================================="
    echo -e "          银行客户画像系统一键部署工具                 "
    echo -e "=======================================================${NC}"
    echo ""
}

# 函数：显示步骤
show_step() {
    echo -e "\n${GREEN}-------------------------------------------------------"
    echo -e " $1"
    echo -e "-------------------------------------------------------${NC}"
}

# 函数：命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 函数：检查Python环境
setup_python_env() {
    show_step "检查Python环境"
    
    if ! command_exists python3; then
        echo -e "${RED}未检测到Python 3，请先安装Python 3.8或更高版本${NC}"
        echo -e "${YELLOW}在Ubuntu系统上可以使用: sudo apt install python3 python3-venv python3-pip${NC}"
        echo -e "${YELLOW}在macOS系统上可以使用: brew install python3${NC}"
        exit 1
    fi
    
    python_version=$(python3 --version)
    echo -e "${GREEN}检测到 $python_version${NC}"
    
    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}创建Python虚拟环境...${NC}"
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            echo -e "${RED}创建虚拟环境失败，请检查Python安装是否完整${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}检测到已有虚拟环境${NC}"
    fi
    
    # 激活虚拟环境
    echo -e "${YELLOW}激活虚拟环境...${NC}"
    source venv/bin/activate
}

# 函数：安装Python依赖
install_python_dependencies() {
    show_step "安装Python依赖"
    
    # 升级pip
    python -m pip install --upgrade pip
    
    # 安装基础依赖
    packages=(
        "flask" 
        "flask-sqlalchemy" 
        "flask-login" 
        "flask-migrate" 
        "flask-cors" 
        "flask-wtf" 
        "python-dotenv" 
        "pymysql"
        "email-validator"
    )
    
    echo -e "${YELLOW}安装Python包...${NC}"
    for package in "${packages[@]}"; do
        echo -e "${NC}正在安装 $package...${NC}"
        pip install $package
        if [ $? -ne 0 ]; then
            echo -e "${YELLOW}安装 $package 失败，但继续安装其他依赖...${NC}"
        fi
    done
    
    # 尝试安装MySQL客户端
    echo -e "${YELLOW}尝试安装MySQL客户端...${NC}"
    pip install mysqlclient
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}安装mysqlclient失败，将使用pymysql作为替代${NC}"
        
        # 在某些系统上，可能需要安装额外的系统包
        if command_exists apt-get; then
            echo -e "${YELLOW}检测到Debian/Ubuntu系统，尝试安装系统依赖...${NC}"
            echo -e "${YELLOW}可能需要输入sudo密码${NC}"
            sudo apt-get update
            sudo apt-get install -y python3-dev default-libmysqlclient-dev build-essential
            pip install mysqlclient
        elif command_exists brew; then
            echo -e "${YELLOW}检测到macOS系统，尝试安装系统依赖...${NC}"
            brew install mysql-client
            pip install mysqlclient
        fi
    fi
}

# 函数：检查Node.js环境
setup_node_env() {
    show_step "检查Node.js环境"
    
    if ! command_exists node; then
        echo -e "${RED}未检测到Node.js，请先安装Node.js 16或更高版本${NC}"
        echo -e "${YELLOW}下载地址: https://nodejs.org/en/download/${NC}"
        echo -e "${YELLOW}在Ubuntu系统上可以使用: curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - && sudo apt-get install -y nodejs${NC}"
        echo -e "${YELLOW}在macOS系统上可以使用: brew install node@16${NC}"
        exit 1
    fi
    
    node_version=$(node --version)
    npm_version=$(npm --version)
    echo -e "${GREEN}检测到 Node.js $node_version${NC}"
    echo -e "${GREEN}检测到 npm $npm_version${NC}"
    
    # 检查npx是否可用
    if ! command_exists npx; then
        echo -e "${YELLOW}安装npx...${NC}"
        npm install -g npx
    fi
}

# 函数：安装Node.js依赖
install_node_dependencies() {
    show_step "安装Node.js依赖"
    
    # 安装前端依赖
    echo -e "${YELLOW}安装前端依赖...${NC}"
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}安装前端依赖失败，尝试使用--force参数...${NC}"
        npm install --force
    fi
    
    # 安装Vite
    echo -e "${YELLOW}安装Vite...${NC}"
    npm install vite @vitejs/plugin-vue --save-dev
    npm install -g vite
}

# 函数：配置环境变量
setup_env_file() {
    local db_type=$1
    local db_password=$2
    
    show_step "配置环境变量"
    
    if [ "$db_type" = "mysql" ]; then
        db_url="mysql://root:$db_password@localhost/bank_customer_portrait"
    else
        db_url="sqlite:///app.db"
    fi
    
    current_date=$(date +%Y%m%d)
    secret_key=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
    
    cat > .env << EOF
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-$current_date

# 数据库URL
DATABASE_URL=$db_url

# 应用相关配置
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
EOF
    
    echo -e "${GREEN}已创建.env文件，使用 $db_type 数据库${NC}"
}

# 函数：初始化数据库
init_database() {
    local db_type=$1
    
    show_step "初始化数据库"
    
    # 清理旧的迁移文件
    if [ -d "migrations" ]; then
        echo -e "${YELLOW}移除旧的迁移文件...${NC}"
        rm -rf migrations
    fi
    
    # 初始化Flask迁移
    echo -e "${YELLOW}初始化数据库迁移...${NC}"
    flask db init
    flask db migrate -m "初始化数据库"
    flask db upgrade
    
    # 如果迁移失败，使用gen_data.py直接创建
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}迁移失败，尝试使用gen_data.py创建数据库...${NC}"
        python gen_data.py
    fi
}

# 函数：修复并优化Vite配置
fix_vite_config() {
    show_step "优化前端配置"
    
    vite_config_path="vite.config.js"
    if [ -f "$vite_config_path" ]; then
        # 使用sed修改配置
        if grep -q "host: true" "$vite_config_path"; then
            sed -i.bak "s/host: true/host: '0.0.0.0'/" "$vite_config_path"
        fi
        
        # 确保配置文件中有正确的代理设置
        if ! grep -q "/api" "$vite_config_path"; then
            echo -e "${YELLOW}添加API代理配置...${NC}"
            sed -i.bak "s/server: {/server: {\n    proxy: {\n      '\/api': {\n        target: 'http:\/\/localhost:5000',\n        changeOrigin: true,\n        rewrite: (path) => path.replace(\/^\\/api\/, '')\n      }\n    },/" "$vite_config_path"
        fi
        
        echo -e "${GREEN}已优化Vite配置${NC}"
    else
        echo -e "${YELLOW}未找到vite.config.js文件，跳过配置优化${NC}"
    fi
}

# 函数：创建启动脚本
create_start_script() {
    show_step "创建启动脚本"
    
    cat > start.sh << 'EOF'
#!/bin/bash
# 银行客户画像系统启动脚本

# 颜色定义
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo -e "${CYAN}======================================================="
echo -e "          银行客户画像系统启动工具                     "
echo -e "=======================================================${NC}"
echo ""

# 激活虚拟环境
source venv/bin/activate

# 选择启动模式
echo -e "${YELLOW}请选择启动模式:${NC}"
echo "1. 仅启动后端（Flask API）"
echo "2. 仅启动前端（Vite开发服务器）"
echo "3. 同时启动前端和后端（推荐）"
echo ""

read -p "请输入选择 [1-3]: " choice

case $choice in
    1)
        echo -e "${GREEN}启动后端服务...${NC}"
        gnome-terminal -- bash -c "cd '$(pwd)'; source venv/bin/activate; flask run; exec bash" 2>/dev/null || \
        xterm -e "cd '$(pwd)'; source venv/bin/activate; flask run; exec bash" 2>/dev/null || \
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && source venv/bin/activate && flask run"' 2>/dev/null || \
        konsole --workdir $(pwd) -e "source venv/bin/activate; flask run" 2>/dev/null || \
        {
            echo "无法启动新终端窗口，在当前窗口运行";
            flask run;
        }
        ;;
    2)
        echo -e "${GREEN}启动前端服务...${NC}"
        gnome-terminal -- bash -c "cd '$(pwd)'; npm run dev; exec bash" 2>/dev/null || \
        xterm -e "cd '$(pwd)'; npm run dev; exec bash" 2>/dev/null || \
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && npm run dev"' 2>/dev/null || \
        konsole --workdir $(pwd) -e "npm run dev" 2>/dev/null || \
        {
            echo "无法启动新终端窗口，在当前窗口运行";
            npm run dev;
        }
        ;;
    3)
        echo -e "${GREEN}启动后端服务...${NC}"
        gnome-terminal -- bash -c "cd '$(pwd)'; source venv/bin/activate; flask run; exec bash" 2>/dev/null || \
        xterm -e "cd '$(pwd)'; source venv/bin/activate; flask run; exec bash" 2>/dev/null || \
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && source venv/bin/activate && flask run"' 2>/dev/null || \
        konsole --workdir $(pwd) -e "source venv/bin/activate; flask run" 2>/dev/null || \
        {
            echo "无法启动新终端窗口，在后台运行后端服务";
            nohup flask run > flask.log 2>&1 &
            echo "后端服务已在后台启动，日志保存在 flask.log";
        }
        
        sleep 2
        
        echo -e "${GREEN}启动前端服务...${NC}"
        gnome-terminal -- bash -c "cd '$(pwd)'; npm run dev; exec bash" 2>/dev/null || \
        xterm -e "cd '$(pwd)'; npm run dev; exec bash" 2>/dev/null || \
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && npm run dev"' 2>/dev/null || \
        konsole --workdir $(pwd) -e "npm run dev" 2>/dev/null || \
        {
            echo "无法启动新终端窗口，在当前窗口运行前端服务";
            npm run dev;
        }
        
        echo ""
        echo -e "${GREEN}服务已启动:${NC}"
        echo "- 前端地址: http://localhost:5173"
        echo "- 后端API: http://localhost:5000/api"
        ;;
    *)
        echo "无效选择，退出"
        ;;
esac
EOF
    
    chmod +x start.sh
    echo -e "${GREEN}已创建启动脚本 start.sh${NC}"
}

# 函数：显示完成信息
show_completed() {
    show_step "部署完成"
    
    echo -e "${GREEN}银行客户画像系统部署已完成!${NC}"
    echo ""
    echo -e "${YELLOW}您可以使用以下命令启动系统:${NC}"
    echo "  ./start.sh"
    echo ""
    echo -e "${YELLOW}测试账号:${NC}"
    echo "- 管理员: admin / admin123"
    echo "- 客户经理: manager1-3 / 123456"
    echo "- 客户: customer1-10 / 123456"
    echo ""
    echo -e "${YELLOW}系统地址:${NC}"
    echo "- 前端界面: http://localhost:5173"
    echo "- 后端API: http://localhost:5000/api"
}

# 主函数：执行部署流程
main() {
    show_title
    
    # 检查是否有root权限
    if [ "$EUID" -eq 0 ]; then
        echo -e "${YELLOW}警告: 您正在以root用户运行此脚本。建议使用普通用户运行，必要时使用sudo命令。${NC}"
        read -p "是否继续? (y/n): " continue_as_root
        if [ "$continue_as_root" != "y" ]; then
            echo "退出安装。"
            exit 1
        fi
    fi
    
    # 询问数据库类型
    echo ""
    echo -e "${YELLOW}请选择数据库类型:${NC}"
    echo "1. SQLite (推荐，无需额外配置)"
    echo "2. MySQL (需要MySQL服务器)"
    
    read -p "请输入选择 [1/2]: " db_choice
    
    if [ "$db_choice" = "2" ]; then
        db_type="mysql"
        echo ""
        echo -e "${YELLOW}请输入MySQL的root密码:${NC}"
        read -s db_password
        echo ""
    else
        db_type="sqlite"
        db_password=""
    fi
    
    # 执行部署步骤
    setup_python_env
    install_python_dependencies
    setup_node_env
    install_node_dependencies
    setup_env_file "$db_type" "$db_password"
    init_database "$db_type"
    fix_vite_config
    create_start_script
    show_completed
    
    # 询问是否立即启动
    echo ""
    read -p "是否立即启动系统? (y/n): " start_now
    if [ "$start_now" = "y" ]; then
        ./start.sh
    fi
}

# 开始部署流程
main 