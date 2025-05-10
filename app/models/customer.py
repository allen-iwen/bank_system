from app import db
from datetime import datetime

class Customer(db.Model):
    """客户模型"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    name = db.Column(db.String(64))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(64))
    income = db.Column(db.String(64))
    assets = db.Column(db.Float, default=0.0)
    risk_preference = db.Column(db.String(64))
    investment_horizon = db.Column(db.String(20))  # 投资期限：短期、中期、长期
    education = db.Column(db.String(64))
    family_status = db.Column(db.String(64))  # 家庭状况：单身、已婚无子女、已婚有子女等
    financial_goals = db.Column(db.String(128))  # 理财目标
    customer_value = db.Column(db.Float, default=3.0)  # 客户价值评分(1-5)
    product_preferences = db.Column(db.String(128))  # 产品偏好
    service_frequency = db.Column(db.String(20))  # 服务频率：低、中、高
    digital_preference = db.Column(db.String(20))  # 数字化渠道偏好：低、中、高
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    matching_records = db.relationship('MatchingRecord', backref='customer', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Customer {self.name}, age={self.age}>' 