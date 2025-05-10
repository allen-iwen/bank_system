from app import db
from datetime import datetime

class Manager(db.Model):
    """客户经理模型"""
    __tablename__ = 'managers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    name = db.Column(db.String(64))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    department = db.Column(db.String(64))  # 所属部门
    position = db.Column(db.String(64))  # 职位
    expertise = db.Column(db.String(128))  # 专业领域
    performance_score = db.Column(db.Float, default=3.0)  # 绩效评分(1-5)
    service_years = db.Column(db.Integer, default=0)  # 服务年限
    customer_count = db.Column(db.Integer, default=0)  # 负责客户数量
    max_customers = db.Column(db.Integer, default=10)  # 最大负责客户数量
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    matching_records = db.relationship('MatchingRecord', backref='manager', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Manager {self.name}, expertise={self.expertise}>'
    
    def is_available(self):
        """检查经理是否还能接受更多客户"""
        return self.customer_count < self.max_customers 