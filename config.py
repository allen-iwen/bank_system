import os
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
    # 默认使用SQLite数据库，但环境变量中优先使用MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 客户分类权重配置
    CUSTOMER_CLASSIFICATION_WEIGHTS = {
        'assets': 0.4,  # 总资产权重
        'risk_preference': 0.2,  # 风险偏好权重
        'investment_horizon': 0.2,  # 投资期限权重
        'financial_goals': 0.2   # 财务目标权重
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
