# 银行客户画像及客户经理分配系统

## 项目介绍

本系统是一个基于Python Flask和Vue.js的银行客户画像及客户经理智能分配平台，旨在通过数据分析和智能算法，实现客户与客户经理的最优匹配，提升银行的客户服务质量和管理效率。

## 技术栈

### 后端技术
- Python Flask：Web框架
- SQLAlchemy：ORM框架
- JWT：用户认证
- Machine Learning：智能匹配算法

### 前端技术
- Vue.js 3：前端框架
- Element Plus：UI组件库
- ECharts：数据可视化
- Pinia：状态管理
- Vue Router：路由管理

## 功能特性

### 多角色用户系统
- 客户登录和注册
- 客户经理登录和管理
- 管理员系统控制

### 客户画像管理
- 客户信息管理
- 客户分类标签
- 需求分析
- 兴趣爱好记录

### 智能匹配系统
- 自动匹配算法
- 匹配度评分
- 手动调整功能
- 匹配历史记录

### 数据分析和可视化
- 客户分布分析
- 匹配效果统计
- 业务增长趋势
- 实时数据监控

## 快速开始

以下是快速启动项目的步骤：

### 环境准备

确保你的系统已安装以下软件：
- Python 3.8+
- Node.js 16+
- MySQL 5.7+

### 克隆项目

```bash
git clone <项目地址>
cd 银行客户画像系统
```

### 创建并激活虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 安装后端依赖

```bash
pip install -r requirements.txt
pip install pymysql
```

### 安装前端依赖

```bash
npm install
```

### 配置环境变量

创建或编辑 `.env` 文件，设置必要的环境变量：

```
SECRET_KEY=dev-key-please-change-in-production
DATABASE_URL=mysql://root:password@localhost/bank_customer_portrait
FLASK_APP=run.py
FLASK_ENV=development
```

根据你的MySQL配置修改 `DATABASE_URL`。

### 一键设置（推荐）

我们提供了一键设置脚本，可以自动创建数据库、执行迁移并生成测试数据：

```bash
python setup.py setup
```

### 手动设置

如果你想手动执行各个步骤：

1. 创建MySQL数据库：

```sql
CREATE DATABASE bank_customer_portrait CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 初始化数据库迁移：

```bash
flask db init
flask db migrate -m "初始化数据库"
flask db upgrade
```

3. 生成测试数据：

```bash
flask shell
```

在Flask shell中执行：

```python
from app.utils.data_generator import generate_test_data
generate_test_data()
exit()
```

### 启动应用

1. 启动后端服务：

```bash
flask run
```

2. 在另一个终端启动前端开发服务器：

```bash
npm run dev
```

### 访问应用

打开浏览器，访问：http://localhost:3000

## 测试账号

设置脚本会自动生成以下测试账号：

- 管理员：username=admin, password=admin123
- 客户：username=customer1-20, password=123456
- 客户经理：username=manager1-5, password=123456

## 常见问题

### 数据库连接问题

- 确保MySQL服务已启动
- 检查.env文件中的DATABASE_URL是否正确
- 确认用户名和密码是否正确

### 依赖安装问题

如果安装依赖过程中遇到问题，请尝试：

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

对于前端依赖问题：

```bash
npm cache clean --force
npm install
```

### 前端API请求问题

如果前端无法正确请求后端API：
- 确保后端服务正在运行
- 检查vite.config.js中的代理设置是否正确
- 检查浏览器控制台是否有错误信息

## 项目结构

```
银行客户画像系统/
├── app/                      # Flask应用目录
│   ├── api/                  # API蓝图
│   ├── auth/                 # 认证蓝图
│   ├── main/                 # 主功能蓝图
│   ├── models.py             # 数据模型定义
│   ├── utils/                # 工具函数
│   └── __init__.py           # 应用初始化
├── migrations/               # 数据库迁移文件
├── src/                      # Vue前端源码
│   ├── api/                  # API服务
│   ├── assets/               # 静态资源
│   ├── components/           # 公共组件
│   ├── router/               # 路由配置
│   ├── views/                # 页面视图
│   ├── App.vue               # 根组件
│   └── main.js               # 入口文件
├── .env                      # 环境变量
├── config.py                 # 应用配置
├── package.json              # NPM配置
├── requirements.txt          # Python依赖
├── run.py                    # 应用入口
├── setup.py                  # 设置脚本
└── vite.config.js            # Vite配置
```

## 系统架构

### 后端架构
- RESTful API设计
- 分层架构：路由层、服务层、数据层
- 中间件：认证、日志、异常处理

### 前端架构
- 组件化设计
- 响应式布局
- 状态管理
- 路由管理

### 数据库设计
- 用户表
- 客户信息表
- 客户经理表
- 匹配记录表

## 安全特性

- JWT身份认证
- 密码加密存储
- 角色权限控制
- 操作日志记录
- 数据访问控制

## 开发团队

- 产品经理：需求分析和功能规划
- 后端开发：API实现和数据处理
- 前端开发：界面设计和交互实现
- 算法工程师：匹配算法优化
- 测试工程师：功能测试和质量保证

## 版本历史

### v1.0.0 (2023-08-15)
- 完整的用户认证系统
- 基础的客户管理功能
- 智能匹配算法初版
- 数据可视化面板