#!/usr/bin/env python3

# 三国志战略版智能配将与协同分析工具
# 主应用文件

from flask import Flask, jsonify, render_template

def create_app():
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/health')
    def health_check():
        return jsonify({"status": "ok", "message": "Application is running"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)