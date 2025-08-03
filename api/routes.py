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
    """获取所有武将（支持分页和搜索）"""
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 20, type=int)
    search = request.args.get('search', '', type=str)
    
    # 获取所有武将数据
    all_heroes = data_manager.get_heroes()
    
    # 如果有搜索关键字，进行过滤
    if search:
        filtered_heroes = {}
        for name, info in all_heroes.items():
            if search.lower() in name.lower() or search.lower() in str(info).lower():
                filtered_heroes[name] = info
        all_heroes = filtered_heroes
    
    # 计算分页信息
    total = len(all_heroes)
    start = (page - 1) * size
    end = start + size
    
    # 获取当前页的武将数据
    hero_items = list(all_heroes.items())
    paginated_heroes = dict(hero_items[start:end])
    
    return jsonify({
        "count": total,
        "page": page,
        "size": size,
        "total_pages": (total + size - 1) // size,
        "heroes": paginated_heroes
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
    """获取所有战法（支持分页和搜索）"""
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 20, type=int)
    search = request.args.get('search', '', type=str)
    
    # 获取所有战法数据
    all_skills = data_manager.get_skills()
    
    # 如果有搜索关键字，进行过滤
    if search:
        filtered_skills = {}
        for name, info in all_skills.items():
            if search.lower() in name.lower() or search.lower() in str(info).lower():
                filtered_skills[name] = info
        all_skills = filtered_skills
    
    # 计算分页信息
    total = len(all_skills)
    start = (page - 1) * size
    end = start + size
    
    # 获取当前页的战法数据
    skill_items = list(all_skills.items())
    paginated_skills = dict(skill_items[start:end])
    
    return jsonify({
        "count": total,
        "page": page,
        "size": size,
        "total_pages": (total + size - 1) // size,
        "skills": paginated_skills
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
    """推荐队伍组合（支持更多自定义参数）"""
    # 获取请求参数
    data = request.get_json()
    count = data.get('count', 10)
    required_hero = data.get('required_hero')
    excluded_heroes = data.get('excluded_heroes', [])
    required_camp = data.get('required_camp')
    required_tags = data.get('required_tags', [])
    strategy = data.get('strategy', 'balanced')  # balanced, high_synergy, diverse
    
    # 调用推荐引擎
    recommendations = recommender.recommend_teams(
        count=count,
        required_hero=required_hero,
        excluded_heroes=excluded_heroes,
        required_camp=required_camp,
        required_tags=required_tags,
        strategy=strategy
    )
    
    return jsonify({
        "count": len(recommendations),
        "teams": recommendations
    })

@api_bp.route('/synergy', methods=['POST'])
def analyze_synergy():
    """分析队伍协同效应（支持详细分析）"""
    # 获取请求参数
    data = request.get_json()
    team_heroes = data.get('heroes', [])
    detailed = data.get('detailed', False)
    
    if not team_heroes:
        return jsonify({
            "error": "必须提供武将名单"
        }), 400
    
    # 调用协同分析器
    if detailed:
        # 获取详细分析结果
        synergy_analysis = synergy_analyzer.analyze_synergy_detailed(team_heroes)
    else:
        # 获取基础分析结果
        synergy_analysis = synergy_analyzer.analyze_synergy(team_heroes)
    
    synergy_score = synergy_analyzer.calculate_synergy_score(team_heroes)
    
    return jsonify({
        "team": team_heroes,
        "synergy_analysis": synergy_analysis,
        "synergy_score": synergy_score
    })

@api_bp.route('/announcements', methods=['GET'])
def get_announcements():
    """获取游戏公告列表（支持分页和搜索）"""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 20, type=int)
    search = request.args.get('search', '', type=str)
    
    # 获取公告列表
    announcements = data_manager.get_announcement_list(page=page-1, size=size)  # API使用从0开始的页码
    if announcements:
        # 解析公告数据
        result = announcements.get("result", {})
        total = result.get("totalCount", 0)
        items = result.get("list", [])
        
        # 如果有搜索关键字，进行过滤
        if search:
            filtered_items = []
            for item in items:
                title = item.get("title", "")
                content = item.get("content", "")
                if search.lower() in title.lower() or search.lower() in content.lower():
                    filtered_items.append(item)
            items = filtered_items
            total = len(items)
        
        return jsonify({
            "count": total,
            "page": page,
            "size": size,
            "total_pages": (total + size - 1) // size if total > 0 else 1,
            "announcements": items
        })
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


@api_bp.route('/metadata', methods=['GET'])
def get_metadata():
    """获取元数据（阵营、标签等）"""
    # 获取所有武将数据
    heroes = data_manager.get_heroes()
    
    # 收集所有阵营和标签
    camps = set()
    tags = set()
    
    for hero_info in heroes.values():
        # 收集阵营
        camp = hero_info.get("阵营", "")
        if camp:
            camps.add(camp)
        
        # 收集标签
        hero_tags = hero_info.get("标签", [])
        tags.update(hero_tags)
    
    return jsonify({
        "camps": sorted(list(camps)),
        "tags": sorted(list(tags))
    })

@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "ok",
        "message": "API服务运行正常"
    })