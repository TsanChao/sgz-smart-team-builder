# API路由定义

from flask import Blueprint, jsonify, request
from data.data_manager import DataManager
from core.synergy_analyzer import SynergyAnalyzer
from core.recommender import Recommender

# 初始化数据管理器和分析器
data_manager = DataManager("data/consolidated_ocr_data.json")
synergy_analyzer = SynergyAnalyzer(data_manager)
recommender = Recommender(data_manager, synergy_analyzer)

api_bp = Blueprint('api', __name__)

@api_bp.route('/heroes', methods=['GET'])
def get_heroes():
    """获取所有武将"""
    heroes = data_manager.get_heroes()
    return jsonify({
        "count": len(heroes),
        "heroes": heroes
    })

@api_bp.route('/heroes/<hero_name>', methods=['GET'])
def get_hero(hero_name):
    """获取指定武将的详细信息"""
    hero = data_manager.get_hero_by_name(hero_name)
    if hero:
        return jsonify({
            "name": hero_name,
            "info": hero
        })
    else:
        return jsonify({
            "error": f"未找到武将 {hero_name}"
        }), 404

@api_bp.route('/skills', methods=['GET'])
def get_skills():
    """获取所有战法"""
    skills = data_manager.get_skills()
    return jsonify({
        "count": len(skills),
        "skills": skills
    })

@api_bp.route('/skills/<skill_name>', methods=['GET'])
def get_skill(skill_name):
    """获取指定战法的详细信息"""
    skill = data_manager.get_skill_by_name(skill_name)
    if skill:
        return jsonify({
            "name": skill_name,
            "info": skill
        })
    else:
        return jsonify({
            "error": f"未找到战法 {skill_name}"
        }), 404

@api_bp.route('/recommend', methods=['POST'])
def recommend_teams():
    """推荐队伍组合"""
    # 获取请求参数
    data = request.get_json()
    count = data.get('count', 10)
    required_hero = data.get('required_hero')
    excluded_heroes = data.get('excluded_heroes', [])
    
    # 调用推荐引擎
    recommendations = recommender.recommend_teams(
        count=count,
        required_hero=required_hero,
        excluded_heroes=excluded_heroes
    )
    
    return jsonify({
        "count": len(recommendations),
        "teams": recommendations
    })

@api_bp.route('/synergy', methods=['POST'])
def analyze_synergy():
    """分析队伍协同效应"""
    # 获取请求参数
    data = request.get_json()
    team_heroes = data.get('heroes', [])
    
    if not team_heroes:
        return jsonify({
            "error": "必须提供武将名单"
        }), 400
    
    # 调用协同分析器
    synergy_analysis = synergy_analyzer.analyze_synergy(team_heroes)
    synergy_score = synergy_analyzer.calculate_synergy_score(team_heroes)
    
    return jsonify({
        "team": team_heroes,
        "synergy_analysis": synergy_analysis,
        "synergy_score": synergy_score
    })

@api_bp.route('/announcements', methods=['GET'])
def get_announcements():
    """获取游戏公告列表"""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 20, type=int)
    
    # 获取公告列表
    announcements = data_manager.get_announcement_list(page=page, size=size)
    if announcements:
        return jsonify(announcements)
    else:
        return jsonify({
            "error": "获取公告列表失败"
        }), 500

@api_bp.route('/announcements/<announcement_id>', methods=['GET'])
def get_announcement(announcement_id):
    """获取公告详情"""
    # 获取公告详情
    detail = data_manager.get_announcement_detail(announcement_id)
    if detail:
        return jsonify(detail)
    else:
        return jsonify({
            "error": "获取公告详情失败"
        }), 500

@api_bp.route('/announcements/check-updates', methods=['POST'])
def check_updates():
    """检查是否有新的维护更新公告"""
    has_updates = data_manager.check_for_updates()
    return jsonify({
        "has_updates": has_updates
    })

@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "ok",
        "message": "API服务运行正常"
    })