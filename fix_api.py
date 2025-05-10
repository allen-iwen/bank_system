from flask import Flask, jsonify, request, g, send_from_directory, render_template
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import datetime, timedelta
import json
import os
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 修复现有的app/__init__.py中的问题
def fix_api_routes(app):
    """为应用添加所有必要的API路由"""
    # 启用CORS，确保允许所有源
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    
    # 认证相关API
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        try:
            data = request.get_json()
            username = data.get('username', '')
            password = data.get('password', '')
            
            logger.info(f"尝试登录: {username}")
            
            # 模拟认证
            if username and password:
                # 模拟用户角色
                role = 'admin'
                if username.startswith('manager'):
                    role = 'manager'
                elif username.startswith('customer'):
                    role = 'customer'
                
                response_data = {
                    'token': 'mock-token-' + username,
                    'user': {
                        'id': random.randint(1, 100),
                        'username': username,
                        'role': role
                    }
                }
                
                logger.info(f"登录成功: {username}, 角色: {role}")
                return jsonify({
                    'status': 'success',
                    'message': '登录成功',
                    'data': response_data
                })
            else:
                logger.warning(f"登录失败: 用户名或密码错误")
                return jsonify({
                    'status': 'error',
                    'message': '用户名或密码错误',
                    'data': None
                }), 401
        except Exception as e:
            logger.error(f"登录异常: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'登录失败: {str(e)}',
                'data': None
            }), 500
    
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        try:
            data = request.get_json()
            username = data.get('username', '')
            
            logger.info(f"尝试注册: {username}")
            
            # 模拟注册
            if username:
                user_role = data.get('role', 'customer')
                user_data = {
                    'id': random.randint(1, 100),
                    'username': username,
                    'role': user_role
                }
                
                return jsonify({
                    'status': 'success',
                    'message': '注册成功',
                    'data': {'user': user_data}
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': '注册信息不完整',
                    'data': None
                }), 400
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'注册失败: {str(e)}',
                'data': None
            }), 500
    
    # 客户相关API
    @app.route('/api/customers', methods=['GET'])
    def get_customers():
        try:
            # 模拟客户数据
            customers = []
            for i in range(1, 11):
                customers.append({
                    'id': i,
                    'name': f'客户{i}',
                    'age': random.randint(20, 65),
                    'occupation': random.choice(['工程师', '教师', '医生', '自由职业者']),
                    'total_assets': round(random.uniform(10000, 1000000), 2),
                    'classification': random.choice(['A', 'B', 'C', 'D']),
                    'manager_id': random.randint(1, 3) if random.random() > 0.3 else None,
                    'risk_preference': random.choice(['保守型', '稳健型', '积极型']),
                    'hobbies': random.sample(['旅游', '阅读', '运动', '音乐', '美食'], k=random.randint(1, 3))
                })
            
            return jsonify({
                'status': 'success',
                'message': '获取客户列表成功',
                'data': {'customers': customers}
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取客户列表失败: {str(e)}',
                'data': None
            }), 500
    
    # 客户经理相关API
    @app.route('/api/managers', methods=['GET'])
    def get_managers():
        try:
            # 模拟客户经理数据
            managers = []
            for i in range(1, 4):
                managers.append({
                    'id': i,
                    'name': f'客户经理{i}',
                    'capabilities': random.sample(['存款', '理财', '贷款', '保险', '基金'], k=random.randint(2, 4)),
                    'hobbies': random.sample(['旅游', '阅读', '运动', '音乐', '美食'], k=random.randint(1, 3)),
                    'customer_count': random.randint(3, 8),
                    'department': random.choice(['个人金融部', '企业金融部', '财富管理部']),
                    'expertise': random.choice(['个人贷款', '企业贷款', '理财产品', '外汇业务'])
                })
            
            return jsonify({
                'status': 'success',
                'message': '获取客户经理列表成功',
                'data': {'managers': managers}
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取客户经理列表失败: {str(e)}',
                'data': None
            }), 500
    
    # 获取可用客户经理
    @app.route('/api/managers/available', methods=['GET'])
    def get_available_managers():
        try:
            # 模拟可用客户经理数据
            managers = []
            for i in range(1, 4):
                if random.random() > 0.3:  # 随机一些经理是可用的
                    managers.append({
                        'id': i,
                        'name': f'客户经理{i}',
                        'capabilities': random.sample(['存款', '理财', '贷款', '保险', '基金'], k=random.randint(2, 4)),
                        'hobbies': random.sample(['旅游', '阅读', '运动', '音乐', '美食'], k=random.randint(1, 3)),
                        'customer_count': random.randint(3, 8),
                        'max_customers': 10,
                        'is_available': True
                    })
            
            return jsonify({
                'status': 'success',
                'message': '获取可用客户经理成功',
                'data': {'managers': managers}
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取可用客户经理失败: {str(e)}',
                'data': None
            }), 500
    
    # 匹配记录相关API
    @app.route('/api/matching_records', methods=['GET'])
    def get_matching_records():
        try:
            # 模拟匹配记录数据
            records = []
            for i in range(1, 8):
                customer_id = random.randint(1, 10)
                manager_id = random.randint(1, 3)
                records.append({
                    'id': i,
                    'customer_id': customer_id,
                    'customer_name': f'客户{customer_id}',
                    'manager_id': manager_id,
                    'manager_name': f'客户经理{manager_id}',
                    'match_score': round(random.uniform(60, 95), 2),
                    'match_reason': '客户需求与经理能力匹配度高',
                    'created_at': (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                })
            
            return jsonify({
                'status': 'success',
                'message': '获取匹配记录成功',
                'data': {'records': records}
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取匹配记录失败: {str(e)}',
                'data': None
            }), 500
    
    # 匹配开始API
    @app.route('/api/matching/start', methods=['POST'])
    def start_matching():
        try:
            data = request.get_json()
            if data is None:
                data = {}
                
            mode = data.get('mode', 'auto')  # 自动或手动
            scope = data.get('scope', 'all')  # 所有客户或未分配客户
            
            logger.info(f"启动匹配: 模式={mode}, 范围={scope}")
            
            # 模拟匹配结果
            results = []
            num_customers = random.randint(3, 8)
            for i in range(1, num_customers+1):
                customer_id = random.randint(1, 10)
                manager_id = random.randint(1, 3)
                results.append({
                    'customer_id': customer_id,
                    'customer_name': f'客户{customer_id}',
                    'manager_id': manager_id,
                    'manager_name': f'客户经理{manager_id}',
                    'match_score': round(random.uniform(60, 95), 2),
                    'match_status': 'success'
                })
            
            return jsonify({
                'status': 'success',
                'message': f'已成功匹配{len(results)}个客户',
                'data': {
                    'matched_count': len(results),
                    'results': results
                }
            })
        except Exception as e:
            logger.error(f"启动匹配错误: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'开始匹配失败: {str(e)}',
                'data': None
            }), 500
    
    # 创建匹配记录
    @app.route('/api/create_match', methods=['POST'])
    def create_match():
        try:
            data = request.get_json()
            customer_id = data.get('customer_id')
            manager_id = data.get('manager_id')
            
            if not customer_id or not manager_id:
                return jsonify({
                    'status': 'error',
                    'message': '客户ID和客户经理ID不能为空',
                    'data': None
                }), 400
            
            match_score = round(random.uniform(60, 95), 2)
            
            record = {
                'id': random.randint(1, 100),
                'customer_id': customer_id,
                'manager_id': manager_id,
                'match_score': match_score,
                'match_reason': '客户需求与经理能力匹配度高'
            }
            
            return jsonify({
                'status': 'success',
                'message': '匹配创建成功',
                'data': {'record': record}
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'创建匹配记录失败: {str(e)}',
                'data': None
            }), 500
    
    # 统计相关API
    @app.route('/api/statistics', methods=['GET'])
    def get_statistics():
        try:
            # 模拟统计数据
            stats = {
                'customer_count': random.randint(80, 120),
                'manager_count': random.randint(5, 10),
                'match_count': random.randint(60, 100),
                'average_score': round(random.uniform(70, 90), 2),
                'class_distribution': {
                    'A': random.randint(10, 30),
                    'B': random.randint(20, 40),
                    'C': random.randint(20, 40),
                    'D': random.randint(10, 20),
                    'E': random.randint(5, 15)
                },
                'manager_workload': [
                    {'manager_id': 1, 'manager_name': '客户经理1', 'customer_count': random.randint(15, 25)},
                    {'manager_id': 2, 'manager_name': '客户经理2', 'customer_count': random.randint(10, 20)},
                    {'manager_id': 3, 'manager_name': '客户经理3', 'customer_count': random.randint(15, 30)}
                ]
            }
            
            return jsonify({
                'status': 'success',
                'message': '获取统计数据成功',
                'data': {'statistics': stats}
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取统计数据失败: {str(e)}',
                'data': None
            }), 500
    
    # 饼图数据
    @app.route('/api/getdrawPieChart', methods=['GET'])
    def get_draw_pie_chart():
        try:
            # 模拟饼图数据
            pie_data = [
                {'name': 'A类客户', 'value': random.randint(10, 30)},
                {'name': 'B类客户', 'value': random.randint(20, 40)},
                {'name': 'C类客户', 'value': random.randint(20, 40)},
                {'name': 'D类客户', 'value': random.randint(10, 20)},
                {'name': 'E类客户', 'value': random.randint(5, 15)}
            ]
            
            return jsonify({
                'status': 'success',
                'message': '获取饼图数据成功',
                'data': pie_data
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取饼图数据失败: {str(e)}',
                'data': None
            }), 500
    
    # 折线图数据
    @app.route('/api/getdrawLineChart', methods=['GET'])
    def get_draw_line_chart():
        try:
            # 模拟折线图数据
            months = ['1月', '2月', '3月', '4月', '5月', '6月']
            series = [
                {
                    'name': '新增客户',
                    'data': [random.randint(5, 15) for _ in range(6)]
                },
                {
                    'name': '匹配成功',
                    'data': [random.randint(3, 12) for _ in range(6)]
                }
            ]
            
            return jsonify({
                'status': 'success',
                'message': '获取折线图数据成功',
                'data': {'months': months, 'series': series}
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取折线图数据失败: {str(e)}',
                'data': None
            }), 500
    
    # 自动匹配
    @app.route('/api/auto_match', methods=['GET', 'POST'])
    def auto_match():
        try:
            # 模拟自动匹配数据
            results = []
            for i in range(1, random.randint(3, 8)):
                customer_id = random.randint(1, 10)
                manager_id = random.randint(1, 3)
                results.append({
                    'customer_id': customer_id,
                    'customer_name': f'客户{customer_id}',
                    'manager_id': manager_id,
                    'manager_name': f'客户经理{manager_id}',
                    'match_score': round(random.uniform(60, 95), 2),
                    'classification': random.choice(['A', 'B', 'C'])
                })
            
            return jsonify({
                'status': 'success',
                'message': f'自动匹配完成，成功匹配{len(results)}个客户',
                'data': {'matches': results}
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'自动匹配失败: {str(e)}',
                'data': None
            }), 500
    
    # 单个客户匹配
    @app.route('/api/customer/<int:customer_id>/match', methods=['GET'])
    def match_customer(customer_id):
        try:
            # 模拟客户匹配数据
            matches = []
            for i in range(1, 4):
                matches.append({
                    'manager_id': i,
                    'manager_name': f'客户经理{i}',
                    'score': round(random.uniform(60, 95), 2),
                    'demands_match': round(random.uniform(0.5, 0.9), 2),
                    'hobbies_match': round(random.uniform(0.3, 0.8), 2)
                })
            
            # 按匹配分数排序
            matches.sort(key=lambda x: x['score'], reverse=True)
            
            return jsonify({
                'status': 'success',
                'message': '获取客户匹配数据成功',
                'data': {'matches': matches}
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取客户匹配数据失败: {str(e)}',
                'data': None
            }), 500
    
    # 分配客户
    @app.route('/api/customer/<int:customer_id>/assign', methods=['POST'])
    def assign_customer(customer_id):
        try:
            data = request.get_json()
            manager_id = data.get('manager_id')
            
            if not manager_id:
                return jsonify({
                    'status': 'error',
                    'message': '客户经理ID不能为空',
                    'data': None
                }), 400
            
            score = round(random.uniform(60, 95), 2)
            classification = 'A' if score > 85 else 'B' if score > 70 else 'C'
            
            return jsonify({
                'status': 'success',
                'message': '分配成功',
                'data': {
                    'classification': classification,
                    'match_score': score
                }
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'分配客户失败: {str(e)}',
                'data': None
            }), 500
    
    # 设置密码
    @app.route('/api/setpwd', methods=['POST'])
    def setpwd():
        try:
            data = request.get_json()
            return jsonify({
                'status': 'success',
                'message': '密码设置成功',
                'data': None
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'密码设置失败: {str(e)}',
                'data': None
            }), 500
    
    # 用户管理相关API
    @app.route('/api/users/listpage', methods=['GET'])
    def get_user_list_page():
        try:
            # 模拟用户列表数据
            users = []
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
            
            for i in range((page-1)*limit+1, page*limit+1):
                if i > 30:  # 最多30个用户
                    break
                    
                role = 'customer'
                if i % 10 == 0:
                    role = 'admin'
                elif i % 5 == 0:
                    role = 'manager'
                    
                users.append({
                    'id': i,
                    'username': f'user{i}',
                    'email': f'user{i}@example.com',
                    'role': role,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return jsonify({
                'status': 'success',
                'message': '获取用户列表成功',
                'data': {
                    'total': 30,
                    'users': users
                }
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取用户列表失败: {str(e)}',
                'data': None
            }), 500
    
    # 删除用户
    @app.route('/api/user/remove', methods=['GET'])
    def remove_user():
        try:
            user_id = request.args.get('id')
            
            if not user_id:
                return jsonify({
                    'status': 'error',
                    'message': '用户ID不能为空',
                    'data': None
                }), 400
            
            return jsonify({
                'status': 'success',
                'message': f'用户{user_id}删除成功',
                'data': None
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'删除用户失败: {str(e)}',
                'data': None
            }), 500
    
    # 批量删除用户
    @app.route('/api/user/bathremove', methods=['GET'])
    def batch_remove_user():
        try:
            ids = request.args.get('ids')
            
            if not ids:
                return jsonify({
                    'status': 'error',
                    'message': '用户ID不能为空',
                    'data': None
                }), 400
            
            return jsonify({
                'status': 'success',
                'message': f'批量删除成功，共删除{len(ids.split(","))}个用户',
                'data': None
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'批量删除用户失败: {str(e)}',
                'data': None
            }), 500
    
    # 角色相关API
    @app.route('/api/role/check', methods=['GET'])
    def check_role():
        try:
            role = request.args.get('role', '')
            token = request.headers.get('Authorization', '')
            
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            
            # 从token中提取用户信息（模拟）
            username = token.replace('mock-token-', '') if token.startswith('mock-token-') else ''
            
            # 确定用户角色
            user_role = 'guest'
            if username:
                if username == 'admin':
                    user_role = 'admin'
                elif username.startswith('manager'):
                    user_role = 'manager'
                elif username.startswith('customer'):
                    user_role = 'customer'
            
            # 检查角色是否匹配
            has_role = (role == user_role) or (user_role == 'admin')  # 管理员有所有角色权限
            
            return jsonify({
                'status': 'success',
                'data': {
                    'hasRole': has_role,
                    'role': user_role
                }
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'角色检查失败: {str(e)}',
                'data': None
            }), 500

    # 错误处理
    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({'status': 'error', 'message': '请求的资源不存在', 'data': None}), 404
    
    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({'status': 'error', 'message': '服务器内部错误', 'data': None}), 500
    
    # 接口调试端点
    @app.route('/api/debug', methods=['GET'])
    def debug_api():
        """调试API接口，返回所有路由信息"""
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
                'path': str(rule)
            })
        return jsonify({
            'status': 'success',
            'message': '获取API路由信息成功',
            'data': {
                'routes': routes,
                'env': os.environ.get('FLASK_ENV', 'development')
            }
        })

    return app 