# 银行客户画像系统启动脚本
# 版本: 1.0
# 日期: 2023-12-05

# 设置颜色常量
$ColorInfo = "Cyan"
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"

# 打印标题
function Show-Title {
    Write-Host "`n============================================================" -ForegroundColor $ColorInfo
    Write-Host "              银行客户画像系统启动工具                " -ForegroundColor $ColorInfo
    Write-Host "============================================================`n" -ForegroundColor $ColorInfo
}

# 打印步骤标题
function Show-Step {
    param (
        [string]$Title,
        [int]$StepNumber
    )
    Write-Host "`n[$StepNumber] $Title" -ForegroundColor $ColorInfo
    Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo
}

# 检查命令是否存在
function Test-CommandExists {
    param (
        [string]$Command
    )
    
    $exists = $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
    
    return $exists
}

# 检查Python环境
function Test-PythonEnvironment {
    # 检查Python是否已安装
    $pythonExists = Test-CommandExists "python"
    
    if ($pythonExists) {
        $pythonVersion = python --version
        Write-Host "检测到Python: $pythonVersion" -ForegroundColor $ColorSuccess
        return $true
    } else {
        Write-Host "未检测到Python，请安装Python 3.6+后再试！" -ForegroundColor $ColorError
        return $false
    }
}

# 检查Node.js环境
function Test-NodeEnvironment {
    # 检查Node.js是否已安装
    $nodeExists = Test-CommandExists "node"
    
    if ($nodeExists) {
        $nodeVersion = node --version
        Write-Host "检测到Node.js: $nodeVersion" -ForegroundColor $ColorSuccess
        return $true
    } else {
        Write-Host "未检测到Node.js，请安装Node.js 16+后再试！" -ForegroundColor $ColorError
        return $false
    }
}

# 启动后端服务
function Start-BackendService {
    Show-Step -Title "启动后端服务" -StepNumber 1
    
    # 检查apply_fixes.py是否存在
    if (Test-Path "apply_fixes.py") {
        Write-Host "找到apply_fixes.py，启动后端服务..." -ForegroundColor $ColorInfo
        
        # 在新的PowerShell窗口中启动
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python apply_fixes.py"
        
        Write-Host "后端服务已在新窗口启动" -ForegroundColor $ColorSuccess
        Write-Host "API服务地址: http://localhost:5000" -ForegroundColor $ColorSuccess
    } else {
        Write-Host "未找到apply_fixes.py，尝试查找app.py或wsgi.py..." -ForegroundColor $ColorWarning
        
        if (Test-Path "app.py") {
            Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python app.py"
            Write-Host "使用app.py启动了后端服务" -ForegroundColor $ColorSuccess
        } elseif (Test-Path "wsgi.py") {
            Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python wsgi.py"
            Write-Host "使用wsgi.py启动了后端服务" -ForegroundColor $ColorSuccess
        } elseif (Test-Path "flask" -PathType Leaf) {
            Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; flask run"
            Write-Host "使用flask run命令启动了后端服务" -ForegroundColor $ColorSuccess
        } else {
            Write-Host "找不到后端启动文件，请手动启动后端服务" -ForegroundColor $ColorError
            return $false
        }
    }
    
    return $true
}

# 启动前端服务
function Start-FrontendService {
    Show-Step -Title "启动前端服务" -StepNumber 2
    
    # 检查是否有package.json文件
    if (Test-Path "package.json") {
        Write-Host "找到package.json，启动前端服务..." -ForegroundColor $ColorInfo
        
        # 在新的PowerShell窗口中启动
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; npm run dev"
        
        Write-Host "前端服务已在新窗口启动" -ForegroundColor $ColorSuccess
        
        # 获取前端端口号
        $frontendPort = 5173
        if (Test-Path "vite.config.js") {
            $viteConfig = Get-Content "vite.config.js" -Raw
            $portMatch = [regex]::Match($viteConfig, "port:\s*(\d+)")
            if ($portMatch.Success) {
                $frontendPort = $portMatch.Groups[1].Value
            }
        }
        
        Write-Host "前端访问地址: http://localhost:$frontendPort" -ForegroundColor $ColorSuccess
    } else {
        # 尝试在dist目录中查找静态文件
        if (Test-Path "dist" -PathType Container) {
            Write-Host "找到dist目录，前端应用已构建，无需启动开发服务器" -ForegroundColor $ColorInfo
            Write-Host "请直接访问 http://localhost:5000" -ForegroundColor $ColorSuccess
        } else {
            Write-Host "找不到package.json或dist目录，请确保前端代码已正确安装或构建" -ForegroundColor $ColorError
            return $false
        }
    }
    
    return $true
}

# 显示用户信息
function Show-UserInfo {
    Show-Step -Title "测试账号信息" -StepNumber 3
    
    Write-Host "您可以使用以下测试账号登录系统:" -ForegroundColor $ColorInfo
    Write-Host "- 管理员: admin / admin123" -ForegroundColor $ColorInfo
    Write-Host "- 客户经理: manager1 / 123456" -ForegroundColor $ColorInfo
    Write-Host "- 客户: customer1 / 123456" -ForegroundColor $ColorInfo
    
    Write-Host "`n服务启动成功！请在浏览器中打开相应地址访问系统。" -ForegroundColor $ColorSuccess
    Write-Host "如需停止服务，请在相应的终端窗口中按 Ctrl+C 或关闭窗口。" -ForegroundColor $ColorInfo
}

# 主函数
function Start-BankSystem {
    param (
        [string]$Mode = "all"  # 可选值: all, backend, frontend
    )
    
    Show-Title
    
    # 根据模式启动服务
    switch ($Mode) {
        "backend" {
            $pythonOk = Test-PythonEnvironment
            if ($pythonOk) {
                $backendStarted = Start-BackendService
                if ($backendStarted) {
                    Show-UserInfo
                }
            }
        }
        "frontend" {
            $nodeOk = Test-NodeEnvironment
            if ($nodeOk) {
                $frontendStarted = Start-FrontendService
                if ($frontendStarted) {
                    Show-UserInfo
                }
            }
        }
        default {  # "all"
            $pythonOk = Test-PythonEnvironment
            $nodeOk = Test-NodeEnvironment
            
            if ($pythonOk) {
                $backendStarted = Start-BackendService
            }
            
            if ($nodeOk) {
                $frontendStarted = Start-FrontendService
            }
            
            if ($backendStarted -or $frontendStarted) {
                Show-UserInfo
            }
        }
    }
}

# 参数处理
$mode = "all"  # 默认启动全部
if ($args.Count -gt 0) {
    $mode = $args[0].ToLower()
}

# 启动系统
Start-BankSystem -Mode $mode
