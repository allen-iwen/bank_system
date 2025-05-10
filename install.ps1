# 银行客户画像系统一键部署脚本 (Windows PowerShell)
# 作者：银行客户画像系统团队
# 版本：1.0.0
# 日期：2025-05-06

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "          银行客户画像系统一键部署工具                 " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

# 工作目录
$WorkDir = Get-Location

# 函数：检查命令是否存在
function Test-CommandExists {
    param ($command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try {
        if (Get-Command $command) { return $true }
    } catch {
        return $false
    } finally {
        $ErrorActionPreference = $oldPreference
    }
}

# 函数：显示步骤标题
function Show-Step {
    param ($title)
    Write-Host ""
    Write-Host "-------------------------------------------------------" -ForegroundColor Green
    Write-Host " $title" -ForegroundColor Green
    Write-Host "-------------------------------------------------------" -ForegroundColor Green
}

# 函数：检查并创建Python虚拟环境
function Setup-PythonEnv {
    Show-Step "检查Python环境"
    
    if (-not (Test-CommandExists python)) {
        Write-Host "未检测到Python，请先安装Python 3.8或更高版本" -ForegroundColor Red
        Write-Host "下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }
    
    $pythonVersion = python --version
    Write-Host "检测到 $pythonVersion" -ForegroundColor Green
    
    # 检查虚拟环境
    if (-not (Test-Path "venv")) {
        Write-Host "创建Python虚拟环境..." -ForegroundColor Yellow
        python -m venv venv
        if (-not $?) {
            Write-Host "创建虚拟环境失败，请检查Python安装是否完整" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "检测到已有虚拟环境" -ForegroundColor Green
    }
    
    # 激活虚拟环境
    Write-Host "激活虚拟环境..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
}

# 函数：安装Python依赖
function Install-PythonDependencies {
    Show-Step "安装Python依赖"
    
    # 升级pip
    python -m pip install --upgrade pip
    
    # 安装基础依赖
    $packages = @(
        "flask", 
        "flask-sqlalchemy", 
        "flask-login", 
        "flask-migrate", 
        "flask-cors", 
        "flask-wtf", 
        "python-dotenv", 
        "pymysql",
        "email-validator"
    )
    
    Write-Host "安装Python包..." -ForegroundColor Yellow
    foreach ($package in $packages) {
        Write-Host "正在安装 $package..." -ForegroundColor Gray
        pip install $package
        if (-not $?) {
            Write-Host "安装 $package 失败，但继续安装其他依赖..." -ForegroundColor Yellow
        }
    }
    
    # 尝试安装MySQL客户端
    Write-Host "尝试安装MySQL客户端..." -ForegroundColor Yellow
    pip install mysqlclient
    if (-not $?) {
        Write-Host "安装mysqlclient失败，将使用pymysql作为替代" -ForegroundColor Yellow
    }
}

# 函数：检查Node.js环境
function Setup-NodeEnv {
    Show-Step "检查Node.js环境"
    
    if (-not (Test-CommandExists node)) {
        Write-Host "未检测到Node.js，请先安装Node.js 16或更高版本" -ForegroundColor Red
        Write-Host "下载地址: https://nodejs.org/en/download/" -ForegroundColor Yellow
        exit 1
    }
    
    $nodeVersion = node --version
    $npmVersion = npm --version
    Write-Host "检测到 Node.js $nodeVersion" -ForegroundColor Green
    Write-Host "检测到 npm $npmVersion" -ForegroundColor Green
    
    # 检查npx是否可用
    if (-not (Test-CommandExists npx)) {
        Write-Host "安装npx..." -ForegroundColor Yellow
        npm install -g npx
    }
}

# 函数：安装Node.js依赖
function Install-NodeDependencies {
    Show-Step "安装Node.js依赖"
    
    # 安装前端依赖
    Write-Host "安装前端依赖..." -ForegroundColor Yellow
    npm install
    if (-not $?) {
        Write-Host "安装前端依赖失败，尝试使用--force参数..." -ForegroundColor Yellow
        npm install --force
    }
    
    # 安装Vite
    Write-Host "安装Vite..." -ForegroundColor Yellow
    npm install vite @vitejs/plugin-vue --save-dev
    npm install -g vite
}

# 函数：配置环境变量
function Setup-EnvFile {
    param (
        [string]$dbType = "sqlite",
        [string]$dbPassword = ""
    )
    
    Show-Step "配置环境变量"
    
    $dbUrl = if ($dbType -eq "mysql") {
        "mysql://root:$dbPassword@localhost/bank_customer_portrait"
    } else {
        "sqlite:///app.db"
    }
    
    $secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
    $currentDate = Get-Date -Format "yyyyMMdd"
    
    $envContent = @"
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-$currentDate

# 数据库URL
DATABASE_URL=$dbUrl

# 应用相关配置
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
"@
    
    Set-Content -Path ".env" -Value $envContent -Encoding UTF8
    Write-Host "已创建.env文件，使用 $dbType 数据库" -ForegroundColor Green
}

# 函数：初始化数据库
function Init-Database {
    param (
        [string]$dbType = "sqlite"
    )
    
    Show-Step "初始化数据库"
    
    # 清理旧的迁移文件
    if (Test-Path "migrations") {
        Write-Host "移除旧的迁移文件..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force migrations
    }
    
    # 初始化Flask迁移
    Write-Host "初始化数据库迁移..." -ForegroundColor Yellow
    flask db init
    flask db migrate -m "初始化数据库"
    flask db upgrade
    
    # 如果迁移失败，使用gen_data.py直接创建
    if (-not $?) {
        Write-Host "迁移失败，尝试使用gen_data.py创建数据库..." -ForegroundColor Yellow
        python gen_data.py
    }
}

# 函数：修复并优化Vite配置
function Fix-ViteConfig {
    Show-Step "优化前端配置"
    
    $viteConfigPath = "vite.config.js"
    if (Test-Path $viteConfigPath) {
        $viteConfig = Get-Content -Path $viteConfigPath -Raw
        
        # 更新配置
        $viteConfig = $viteConfig -replace "host: true", "host: '0.0.0.0'"
        
        # 确保配置文件中有正确的代理设置
        if ($viteConfig -notmatch "/api") {
            Write-Host "添加API代理配置..." -ForegroundColor Yellow
            $viteConfig = $viteConfig -replace "server: \{", @"
server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    },
"@
        }
        
        Set-Content -Path $viteConfigPath -Value $viteConfig -Encoding UTF8
        Write-Host "已优化Vite配置" -ForegroundColor Green
    } else {
        Write-Host "未找到vite.config.js文件，跳过配置优化" -ForegroundColor Yellow
    }
}

# 函数：启动服务
function Start-Services {
    Show-Step "启动服务"
    
    # 创建启动脚本
    $startScriptContent = @"
# 银行客户画像系统启动脚本
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "          银行客户画像系统启动工具                     " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

# 激活虚拟环境
& ./venv/Scripts/Activate.ps1

# 选择启动模式
Write-Host "请选择启动模式:" -ForegroundColor Yellow
Write-Host "1. 仅启动后端（Flask API）"
Write-Host "2. 仅启动前端（Vite开发服务器）"
Write-Host "3. 同时启动前端和后端（推荐）"
Write-Host ""

`$choice = Read-Host "请输入选择 [1-3]"

switch (`$choice) {
    "1" {
        Write-Host "启动后端服务..." -ForegroundColor Green
        Start-Process powershell -ArgumentList "-NoExit -Command `"cd '$WorkDir'; ./venv/Scripts/Activate.ps1; flask run`""
    }
    "2" {
        Write-Host "启动前端服务..." -ForegroundColor Green
        Start-Process powershell -ArgumentList "-NoExit -Command `"cd '$WorkDir'; npm run dev`""
    }
    "3" {
        Write-Host "启动后端服务..." -ForegroundColor Green
        Start-Process powershell -ArgumentList "-NoExit -Command `"cd '$WorkDir'; ./venv/Scripts/Activate.ps1; flask run`""
        
        Start-Sleep -Seconds 2
        
        Write-Host "启动前端服务..." -ForegroundColor Green
        Start-Process powershell -ArgumentList "-NoExit -Command `"cd '$WorkDir'; npm run dev`""
        
        Write-Host ""
        Write-Host "服务已启动:" -ForegroundColor Green
        Write-Host "- 前端地址: http://localhost:5173"
        Write-Host "- 后端API: http://localhost:5000/api"
        Write-Host ""
        Write-Host "测试账号:" -ForegroundColor Green
        Write-Host "- 管理员: admin / admin123"
        Write-Host "- 客户经理: manager1-3 / 123456"
        Write-Host "- 客户: customer1-10 / 123456"
    }
    default {
        Write-Host "无效选择，退出" -ForegroundColor Red
    }
}
"@
    
    Set-Content -Path "start.ps1" -Value $startScriptContent -Encoding UTF8
    Write-Host "已创建启动脚本 start.ps1" -ForegroundColor Green
}

# 函数：显示完成信息
function Show-Completed {
    Show-Step "部署完成"
    
    Write-Host "银行客户画像系统部署已完成!" -ForegroundColor Green
    Write-Host ""
    Write-Host "您可以使用以下命令启动系统:" -ForegroundColor Yellow
    Write-Host "  .\start.ps1"
    Write-Host ""
    Write-Host "测试账号:" -ForegroundColor Yellow
    Write-Host "- 管理员: admin / admin123"
    Write-Host "- 客户经理: manager1-3 / 123456"
    Write-Host "- 客户: customer1-10 / 123456"
    Write-Host ""
    Write-Host "系统地址:" -ForegroundColor Yellow
    Write-Host "- 前端界面: http://localhost:5173"
    Write-Host "- 后端API: http://localhost:5000/api"
}

# 主函数：执行部署流程
function Start-Deployment {
    # 检查是否有管理员权限
    if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]"Administrator")) {
        Write-Host "建议以管理员权限运行此脚本，某些操作可能需要管理员权限" -ForegroundColor Yellow
        Write-Host "按任意键继续，或关闭此窗口以管理员身份重新运行" -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
    
    # 询问数据库类型
    Write-Host ""
    Write-Host "请选择数据库类型:" -ForegroundColor Yellow
    Write-Host "1. SQLite (推荐，无需额外配置)"
    Write-Host "2. MySQL (需要MySQL服务器)"
    
    $dbChoice = Read-Host "请输入选择 [1/2]"
    $dbType = if ($dbChoice -eq "2") { "mysql" } else { "sqlite" }
    $dbPassword = ""
    
    if ($dbType -eq "mysql") {
        Write-Host ""
        Write-Host "请输入MySQL的root密码:" -ForegroundColor Yellow
        $dbPassword = Read-Host -AsSecureString
        $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassword)
        $dbPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
    }
    
    # 执行部署步骤
    Setup-PythonEnv
    Install-PythonDependencies
    Setup-NodeEnv
    Install-NodeDependencies
    Setup-EnvFile -dbType $dbType -dbPassword $dbPassword
    Init-Database -dbType $dbType
    Fix-ViteConfig
    Start-Services
    Show-Completed
    
    # 询问是否立即启动
    Write-Host ""
    $startNow = Read-Host "是否立即启动系统? (y/n)"
    if ($startNow -eq "y") {
        & .\start.ps1
    }
}

# 开始部署流程
Start-Deployment 