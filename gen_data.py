import os
os.environ['FLASK_APP'] = 'app'

from app import create_app, db
from app.models.user import User
from app.models.customer import Customer 
from app.models.manager import Manager
from app.models.matching_record import MatchingRecord
from werkzeug.security import generate_password_hash
import random
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    print("开始生成测试数据...")
    
    # 清空现有数据
    try:
        db.session.query(MatchingRecord).delete()
        db.session.query(Customer).delete()
        db.session.query(Manager).delete() 
        db.session.query(User).delete()
        db.session.commit()
        print("已清空现有数据")
    except Exception as e:
        print(f"清空数据时出错: {e}")
        db.session.rollback()
    
    # 创建管理员用户
    admin_user = User(
        username='admin',
        email='admin@example.com',
        password_hash=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(admin_user)
    db.session.commit()
    print("已创建管理员账号: admin / admin123")
    
    # 创建客户经理账户
    managers = []
    for i in range(1, 4):  # 3个客户经理
        manager_user = User(
            username=f'manager{i}',
            email=f'manager{i}@example.com',
            password_hash=generate_password_hash('123456'),
            role='manager'
        )
        db.session.add(manager_user)
        db.session.flush()  # 获取用户ID
        
        # 创建客户经理信息
        manager = Manager(
            user_id=manager_user.id,
            name=f'客户经理{i}',
            gender=random.choice(['男', '女']),
            age=random.randint(28, 45),
            department=random.choice(['个人金融部', '企业金融部', '财富管理部']),
            position=random.choice(['初级经理', '中级经理', '高级经理']),
            expertise=random.choice(['个人贷款', '企业贷款', '理财产品', '外汇业务', '资产管理']),
            performance_score=random.uniform(3.0, 5.0),
            service_years=random.randint(1, 15)
        )
        db.session.add(manager)
        managers.append(manager)
    
    db.session.commit()
    print(f"已创建3个客户经理账号")
    
    # 创建客户账户
    customers = []
    for i in range(1, 11):  # 10个客户
        customer_user = User(
            username=f'customer{i}',
            email=f'customer{i}@example.com',
            password_hash=generate_password_hash('123456'),
            role='customer'
        )
        db.session.add(customer_user)
        db.session.flush()  # 获取用户ID
        
        # 创建随机客户信息
        age = random.randint(18, 70)
        customer = Customer(
            user_id=customer_user.id,
            name=f'客户{i}',
            gender=random.choice(['男', '女']),
            age=age,
            occupation=random.choice(['学生', '上班族', '企业主', '自由职业', '退休人士']),
            income=random.choice(['5000以下', '5000-10000', '10000-20000', '20000-50000', '50000以上']),
            assets=random.randint(10000, 10000000),
            risk_preference=random.choice(['保守型', '稳健型', '平衡型', '积极型', '激进型']),
            investment_horizon=random.choice(['短期', '中期', '长期']),
            education=random.choice(['高中及以下', '大专', '本科', '硕士', '博士']),
            family_status=random.choice(['单身', '已婚无子女', '已婚有子女', '离异']),
            financial_goals=random.choice([
                '子女教育', '养老规划', '财富增值', '资产配置', '税务规划', 
                '保险保障', '房产投资', '创业投资'
            ]),
            customer_value=random.uniform(1.0, 5.0),
            product_preferences=random.choice([
                '存款', '理财产品', '基金', '保险', '贷款', '信用卡', '外汇', '股票'
            ]),
            service_frequency=random.choice(['低', '中', '高']),
            digital_preference=random.choice(['低', '中', '高']),
            registration_date=datetime.now() - timedelta(days=random.randint(1, 365))
        )
        db.session.add(customer)
        customers.append(customer)
    
    db.session.commit()
    print(f"已创建10个客户账号")
    
    # 创建随机匹配记录
    for customer in customers:
        manager = random.choice(managers)
        
        matching_score = random.uniform(60.0, 95.0)
        match_record = MatchingRecord(
            customer_id=customer.id,
            manager_id=manager.id,
            matching_score=matching_score,
            matching_time=datetime.now(),
            matching_status=random.choice(['待确认', '已确认', '已拒绝']) if random.random() > 0.5 else '自动匹配'
        )
        db.session.add(match_record)
    
    db.session.commit()
    print("已创建客户-经理匹配记录")
    
    print("测试数据生成完成!")
    print("\n测试账号：")
    print("管理员: admin / admin123")
    print(f"客户经理: manager1-3 / 123456")
    print(f"客户: customer1-10 / 123456") 