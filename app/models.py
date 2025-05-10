from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager
import json
import sqlalchemy as sa
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.types import TypeDecorator, TEXT

# 自定义JSON类型，可以在SQLite中工作
class JSONType(TypeDecorator):
    impl = TEXT
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value
    
    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))  # admin, manager, customer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(64))
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(64))
    total_assets = db.Column(db.Float)
    demands = db.Column(JSONType)  # 存储需求列表
    hobbies = db.Column(JSONType)  # 存储爱好列表
    classification = db.Column(db.String(1))  # A, B, C, D, E
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('customer', uselist=False))
    manager = db.relationship('Manager', backref=db.backref('customers', lazy='dynamic'))

class Manager(db.Model):
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(64))
    capabilities = db.Column(JSONType)  # 存储能力列表
    hobbies = db.Column(JSONType)  # 存储爱好列表
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('manager', uselist=False))

class MatchingRecord(db.Model):
    __tablename__ = 'matching_records'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))
    match_score = db.Column(db.Float)  # 匹配得分
    match_reason = db.Column(db.Text)  # 匹配原因
    created_by = db.Column(db.String(20))  # system or admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    customer = db.relationship('Customer')
    manager = db.relationship('Manager')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))