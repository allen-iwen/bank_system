from flask import jsonify, request
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.models import Customer, Manager, MatchingRecord

def calculate_match_score(customer, manager):
    # 计算需求匹配度
    demands_match = len(set(customer.demands) & set(manager.capabilities)) / \
        max(len(customer.demands), len(manager.capabilities)) if customer.demands and manager.capabilities else 0
    
    # 计算爱好匹配度
    hobbies_match = len(set(customer.hobbies) & set(manager.hobbies)) / \
        max(len(customer.hobbies), len(manager.hobbies)) if customer.hobbies and manager.hobbies else 0
    
    # 计算资产分数（假设最高资产为1000万）
    assets_score = min(customer.total_assets / 10000000, 1.0)
    
    # 根据配置权重计算总分
    from flask import current_app
    weights = current_app.config['CUSTOMER_CLASSIFICATION_WEIGHTS']
    total_score = weights['assets'] * assets_score + \
                 weights['demands'] * demands_match + \
                 weights['hobbies'] * hobbies_match
    
    return total_score, demands_match, hobbies_match

def get_customer_classification(score):
    from flask import current_app
    thresholds = current_app.config['CLASSIFICATION_THRESHOLDS']
    
    for classification, threshold in thresholds.items():
        if score >= threshold:
            return classification
    return 'E'

@bp.route('/customers')
@login_required
def get_customers():
    if current_user.role not in ['admin', 'manager']:
        return jsonify({'message': '无权限访问'}), 403
    
    customers = Customer.query.all()
    return jsonify({
        'customers': [{
            'id': c.id,
            'name': c.name,
            'age': c.age,
            'occupation': c.occupation,
            'total_assets': c.total_assets,
            'demands': c.demands,
            'hobbies': c.hobbies,
            'classification': c.classification,
            'manager_id': c.manager_id
        } for c in customers]
    })

@bp.route('/managers')
@login_required
def get_managers():
    if current_user.role != 'admin':
        return jsonify({'message': '无权限访问'}), 403
    
    managers = Manager.query.all()
    return jsonify({
        'managers': [{
            'id': m.id,
            'name': m.name,
            'capabilities': m.capabilities,
            'hobbies': m.hobbies,
            'customer_count': m.customers.count()
        } for m in managers]
    })

@bp.route('/customer/<int:customer_id>/match')
@login_required
def match_customer(customer_id):
    if current_user.role != 'admin':
        return jsonify({'message': '无权限访问'}), 403
    
    customer = Customer.query.get_or_404(customer_id)
    managers = Manager.query.all()
    
    matches = []
    for manager in managers:
        # 检查客户经理是否已达到最大客户数
        if manager.customers.count() >= current_app.config['MAX_CUSTOMERS_PER_MANAGER']:
            continue
        
        score, demands_match, hobbies_match = calculate_match_score(customer, manager)
        matches.append({
            'manager_id': manager.id,
            'manager_name': manager.name,
            'score': score,
            'demands_match': demands_match,
            'hobbies_match': hobbies_match
        })
    
    # 按匹配分数排序
    matches.sort(key=lambda x: x['score'], reverse=True)
    
    return jsonify({'matches': matches})

@bp.route('/customer/<int:customer_id>/assign', methods=['POST'])
@login_required
def assign_customer(customer_id):
    if current_user.role != 'admin':
        return jsonify({'message': '无权限访问'}), 403
    
    data = request.get_json()
    customer = Customer.query.get_or_404(customer_id)
    manager = Manager.query.get_or_404(data['manager_id'])
    
    # 检查客户经理是否已达到最大客户数
    if manager.customers.count() >= current_app.config['MAX_CUSTOMERS_PER_MANAGER']:
        return jsonify({'message': '该客户经理已达到最大客户数量'}), 400
    
    score, demands_match, hobbies_match = calculate_match_score(customer, manager)
    customer.classification = get_customer_classification(score)
    customer.manager_id = manager.id
    
    # 创建匹配记录
    match_record = MatchingRecord(
        customer_id=customer.id,
        manager_id=manager.id,
        match_score=score,
        match_reason=f'需求匹配度: {demands_match:.2f}, 爱好匹配度: {hobbies_match:.2f}',
        created_by='admin'
    )
    
    db.session.add(match_record)
    db.session.commit()
    
    return jsonify({
        'message': '分配成功',
        'classification': customer.classification,
        'match_score': score
    })

@bp.route('/auto_match')
@login_required
def auto_match():
    if current_user.role != 'admin':
        return jsonify({'message': '无权限访问'}), 403
    
    # 获取所有未分配客户经理的客户
    unassigned_customers = Customer.query.filter_by(manager_id=None).all()
    managers = Manager.query.all()
    
    results = []
    for customer in unassigned_customers:
        best_match = None
        best_score = -1
        
        for manager in managers:
            # 检查客户经理是否已达到最大客户数
            if manager.customers.count() >= current_app.config['MAX_CUSTOMERS_PER_MANAGER']:
                continue
            
            score, demands_match, hobbies_match = calculate_match_score(customer, manager)
            if score > best_score:
                best_score = score
                best_match = {
                    'manager': manager,
                    'score': score,
                    'demands_match': demands_match,
                    'hobbies_match': hobbies_match
                }
        
        if best_match:
            customer.classification = get_customer_classification(best_score)
            customer.manager_id = best_match['manager'].id
            
            # 创建匹配记录
            match_record = MatchingRecord(
                customer_id=customer.id,
                manager_id=best_match['manager'].id,
                match_score=best_score,
                match_reason=f'需求匹配度: {best_match["demands_match"]:.2f}, '
                            f'爱好匹配度: {best_match["hobbies_match"]:.2f}',
                created_by='system'
            )
            
            db.session.add(match_record)
            results.append({
                'customer_id': customer.id,
                'customer_name': customer.name,
                'manager_id': best_match['manager'].id,
                'manager_name': best_match['manager'].name,
                'match_score': best_score,
                'classification': customer.classification
            })
    
    db.session.commit()
    return jsonify({'matches': results})