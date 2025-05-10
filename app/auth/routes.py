from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.auth import bp
from app.models import User, Customer, Manager
from app.auth.forms import LoginForm, RegistrationForm
import jwt
import datetime
from functools import wraps
from flask import current_app

@bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'message': '用户已登录'}), 400
    
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user is None or not user.check_password(data.get('password')):
        return jsonify({'message': '用户名或密码错误'}), 401
    
    login_user(user)
    
    # 生成JWT令牌
    token = jwt.encode({
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'])
    
    return jsonify({
        'message': '登录成功',
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role
        },
        'token': token
    })

@bp.route('/logout')
def logout():
    logout_user()
    return jsonify({'message': '退出登录成功'})

@bp.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify({'message': '用户已登录'}), 400
    
    data = request.get_json()
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'message': '用户名已存在'}), 400
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'message': '邮箱已被注册'}), 400
    
    user = User(
        username=data.get('username'),
        email=data.get('email'),
        role=data.get('role', 'customer')
    )
    user.set_password(data.get('password'))
    
    # 根据角色创建相应的用户信息
    if user.role == 'customer':
        customer = Customer(
            user=user,
            name=data.get('name'),
            age=data.get('age'),
            occupation=data.get('occupation'),
            total_assets=data.get('total_assets', 0.0),
            demands=data.get('demands', []),
            hobbies=data.get('hobbies', [])
        )
        db.session.add(customer)
    elif user.role == 'manager':
        manager = Manager(
            user=user,
            name=data.get('name'),
            capabilities=data.get('capabilities', []),
            hobbies=data.get('hobbies', [])
        )
        db.session.add(manager)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': '注册成功',
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role
        }
    })

@bp.route('/user')
@login_required
def get_user():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.role
    })

# JWT令牌验证装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 从请求头获取token
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': '缺少认证令牌'}), 401
        
        try:
            # 解码令牌
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({'message': '无效的用户令牌'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': '令牌已过期，请重新登录'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': '无效的认证令牌'}), 401
        
        # 将当前用户传递给被装饰的函数
        return f(current_user, *args, **kwargs)
    
    return decorated