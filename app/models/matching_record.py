from app import db
from datetime import datetime

class MatchingRecord(db.Model):
    """客户-经理匹配记录"""
    __tablename__ = 'matching_records'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))
    matching_score = db.Column(db.Float, default=0.0)  # 匹配度评分
    matching_time = db.Column(db.DateTime, default=datetime.utcnow)  # 匹配时间
    matching_status = db.Column(db.String(20), default='自动匹配')  # 匹配状态：自动匹配、待确认、已确认、已拒绝
    manager_comments = db.Column(db.Text)  # 经理对匹配的评价
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<MatchingRecord customer_id={self.customer_id}, manager_id={self.manager_id}, score={self.matching_score}>' 