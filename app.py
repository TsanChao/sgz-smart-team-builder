#!/usr/bin/env python3

# 三国志战略版智能配将与协同分析工具
# 主应用文件

import os
from flask import Flask, jsonify, render_template
from api.routes import api_bp

def create_app():
    # 获取项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # 配置模板和静态文件目录
    app = Flask(__name__, 
                template_folder=os.path.join(project_root, 'templates'),
                static_folder=os.path.join(project_root, 'static'))
    
    # 注册API蓝图
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/health')
    def health_check():
        return jsonify({"status": "ok", "message": "Application is running"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=7001)