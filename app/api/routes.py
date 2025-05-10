from flask import jsonify, request, current_app
from app import db
from app.api import bp
from app.models import User, Customer, Manager, MatchingRecord
from app.auth.routes import token_required

# API健康检查
@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'success',
        'message': '系统运行正常'
    })

# 获取客户列表
@bp.route('/customers', methods=['GET'])
@token_required
def get_customers(current_user):
    if current_user.role != 'admin' and current_user.role != 'manager':
        return jsonify({'status': 'error', 'message': '权限不足'}), 403
    
    customers = Customer.query.all()
    result = []
    for customer in customers:
        result.append({
            'id': customer.id,
            'name': customer.name,
            'age': customer.age,
            'occupation': customer.occupation,
            'total_assets': customer.total_assets,
            'classification': customer.classification,
            'manager_id': customer.manager_id
        })
    return jsonify({'status': 'success', 'customers': result})

# 获取客户经理列表
@bp.route('/managers', methods=['GET'])
@token_required
def get_managers(current_user):
    if current_user.role != 'admin':
        return jsonify({'status': 'error', 'message': '权限不足'}), 403
    
    managers = Manager.query.all()
    result = []
    for manager in managers:
        result.append({
            'id': manager.id,
            'name': manager.name,
            'capabilities': manager.capabilities,
            'hobbies': manager.hobbies,
            'customer_count': manager.customers.count()
        })
    return jsonify({'status': 'success', 'managers': result})

# 获取匹配记录
@bp.route('/matching_records', methods=['GET'])
@token_required
def get_matching_records(current_user):
    if current_user.role != 'admin' and current_user.role != 'manager':
        return jsonify({'status': 'error', 'message': '权限不足'}), 403
    
    records = MatchingRecord.query.all()
    result = []
    for record in records:
        result.append({
            'id': record.id,
            'customer_id': record.customer_id,
            'customer_name': record.customer.name,
            'manager_id': record.manager_id,
            'manager_name': record.manager.name,
            'match_score': record.match_score,
            'match_reason': record.match_reason,
            'created_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({'status': 'success', 'records': result})

# 创建匹配记录
@bp.route('/create_match', methods=['POST'])
@token_required
def create_match(current_user):
    if current_user.role != 'admin':
        return jsonify({'status': 'error', 'message': '权限不足'}), 403
    
    data = request.get_json()
    customer_id = data.get('customer_id')
    manager_id = data.get('manager_id')
    
    if not customer_id or not manager_id:
        return jsonify({'status': 'error', 'message': '缺少必要参数'}), 400
    
    customer = Customer.query.get(customer_id)
    manager = Manager.query.get(manager_id)
    
    if not customer or not manager:
        return jsonify({'status': 'error', 'message': '客户或客户经理不存在'}), 404
    
    # 更新客户的客户经理
    customer.manager_id = manager_id
    
    # 计算匹配得分
    match_score = calculate_match_score(customer, manager)
    match_reason = generate_match_reason(customer, manager, match_score)
    
    # 创建匹配记录
    record = MatchingRecord(
        customer_id=customer_id,
        manager_id=manager_id,
        match_score=match_score,
        match_reason=match_reason,
        created_by='admin'
    )
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': '匹配创建成功',
        'record': {
            'id': record.id,
            'customer_id': record.customer_id,
            'manager_id': record.manager_id,
            'match_score': record.match_score,
            'match_reason': record.match_reason
        }
    })

# 辅助函数：计算匹配得分
def calculate_match_score(customer, manager):
    # 获取配置权重
    weights = current_app.config['CUSTOMER_CLASSIFICATION_WEIGHTS']
    
    # 初始化得分
    score = 0
    
    # 根据客户资产计算部分得分
    assets_score = min(customer.total_assets / 1000000, 1.0)  # 假设100万资产为满分
    score += assets_score * weights['assets']
    
    # 计算需求匹配度
    if customer.demands and manager.capabilities:
        customer_demands = set(customer.demands)
        manager_capabilities = set(manager.capabilities)
        matched_demands = customer_demands.intersection(manager_capabilities)
        demands_score = len(matched_demands) / len(customer_demands) if customer_demands else 0
        score += demands_score * weights['demands']
    
    # 计算爱好匹配度
    if customer.hobbies and manager.hobbies:
        customer_hobbies = set(customer.hobbies)
        manager_hobbies = set(manager.hobbies)
        matched_hobbies = customer_hobbies.intersection(manager_hobbies)
        hobbies_score = len(matched_hobbies) / max(len(customer_hobbies), 1)
        score += hobbies_score * weights['hobbies']
    
    return score

# 辅助函数：生成匹配原因
def generate_match_reason(customer, manager, score):
    reason = f"客户 {customer.name} 与客户经理 {manager.name} 的匹配得分为 {score:.2f}。"
    
    if customer.demands and manager.capabilities:
        customer_demands = set(customer.demands)
        manager_capabilities = set(manager.capabilities)
        matched_demands = customer_demands.intersection(manager_capabilities)
        if matched_demands:
            reason += f" 匹配的需求有：{', '.join(matched_demands)}。"
    
    if customer.hobbies and manager.hobbies:
        customer_hobbies = set(customer.hobbies)
        manager_hobbies = set(manager.hobbies)
        matched_hobbies = customer_hobbies.intersection(manager_hobbies)
        if matched_hobbies:
            reason += f" 共同的爱好有：{', '.join(matched_hobbies)}。"
    
    return reason 