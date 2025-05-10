import os
import sys
import logging
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 导入修复函数
from fix_api import fix_api_routes

def create_app():
    """创建并配置一个Flask应用实例"""
    app = Flask(__name__, static_folder='dist', static_url_path='')
    
    # 设置配置
    app.config['SECRET_KEY'] = 'bank-customer-portrait-system-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_AS_ASCII'] = False  # 确保JSON响应可以包含中文
    app.config['DEBUG'] = True
    
    # 启用CORS支持所有域名和路由
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    
    # 应用API修复
    app = fix_api_routes(app)
    
    # 首页路由
    @app.route('/')
    def index():
        try:
            return app.send_static_file('index.html')
        except Exception as e:
            logger.error(f"访问首页出错: {str(e)}")
            return jsonify({"status": "error", "message": "首页不存在，请确保前端已构建"}), 404
    
    # 处理所有前端路由
    @app.route('/<path:path>')
    def static_proxy(path):
        # 处理任何不匹配API的路由
        if path.startswith('api/'):
            logger.warning(f"尝试访问未定义的API路径: {path}")
            return jsonify({"status": "error", "message": "API不存在"}), 404
        try:
            return app.send_static_file(path)
        except Exception as e:
            logger.info(f"尝试访问静态文件失败: {path}, 回退到index.html: {str(e)}")
            try:
                return app.send_static_file('index.html')
            except Exception as e2:
                logger.error(f"回退到index.html失败: {str(e2)}")
                return jsonify({"status": "error", "message": "前端文件不存在"}), 404
    
    # 添加全局错误处理
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"status": "error", "message": "请求的资源不存在"}), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"status": "error", "message": "服务器内部错误"}), 500
    
    return app

if __name__ == "__main__":
    print("="*60)
    print("      银行客户画像系统API修复工具")
    print("="*60)
    print("\n正在应用API修复...")
    
    # 尝试导入现有应用
    try:
        from app import create_app as original_create_app
        print("检测到现有应用，将添加修复到现有应用")
        app = original_create_app()
        app = fix_api_routes(app)
    except ImportError:
        print("未检测到现有应用，创建新应用实例")
        app = create_app()
    
    # 检查flask-cors是否已安装
    try:
        import flask_cors
        print("检测到flask-cors")
    except ImportError:
        print("未检测到flask-cors，请先安装: pip install flask-cors")
        sys.exit(1)
    
    # 输出可用路由
    print("\n可用API路由:")
    for rule in app.url_map.iter_rules():
        if 'api' in str(rule):
            print(f"  {', '.join(rule.methods - {'HEAD', 'OPTIONS'})} {rule}")
    
    print("\n修复应用完成！")
    print("\n启动应用...")
    print("API服务将运行在 http://localhost:5000")
    print("确保前端已经正确配置API基础URL为 /api")
    print("如果您的前端在不同的端口运行(如http://localhost:5174)，已经配置了CORS允许跨域请求")
    print("您可以使用以下测试账号登录系统:")
    print("- 管理员: admin / admin123")
    print("- 客户经理: manager1 / 123456")
    print("- 客户: customer1 / 123456")
    print("\n按Ctrl+C可停止服务")
    print("="*60)
    
    # 启动应用
    app.run(debug=True, host='0.0.0.0', port=5000) 