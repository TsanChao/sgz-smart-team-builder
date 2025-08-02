# 推荐引擎
import itertools
from typing import List, Optional, Dict, Any

class Recommender:
    def __init__(self, data_manager, synergy_analyzer):
        self.data_manager = data_manager
        self.synergy_analyzer = synergy_analyzer
    
    def recommend_teams(self, count=10, required_hero=None, excluded_heroes=None):
        """推荐最佳队伍组合"""
        # 获取所有可用武将
        all_heroes = self.data_manager.get_all_hero_names()
        
        # 处理排除的武将
        if excluded_heroes:
            all_heroes = [hero for hero in all_heroes if hero not in excluded_heroes]
        
        # 生成所有三人组合
        if required_hero:
            # 如果指定了必须包含的武将，生成包含该武将的组合
            if required_hero not in all_heroes:
                return {"error": f"必须包含的武将 {required_hero} 不在可用武将列表中"}
            
            # 从其他武将中选择2个与指定武将组合
            other_heroes = [hero for hero in all_heroes if hero != required_hero]
            combinations = []
            for combo in itertools.combinations(other_heroes, 2):
                combinations.append((required_hero,) + combo)
        else:
            # 生成所有三人组合
            combinations = list(itertools.combinations(all_heroes, 3))
        
        # 计算每个组合的协同评分
        team_scores = []
        for combo in combinations:
            score = self.synergy_analyzer.calculate_synergy_score(list(combo))
            team_scores.append({
                "队伍": list(combo),
                "评分": score
            })
        
        # 按评分排序并返回前N个
        team_scores.sort(key=lambda x: x["评分"], reverse=True)
        return team_scores[:count]
    
    def recommend_single_hero_team(self, main_hero: str, count: int = 10) -> List[Dict[str, Any]]:
        """为指定主将推荐最佳副将组合"""
        # 获取所有可用武将
        all_heroes = self.data_manager.get_all_hero_names()
        
        # 移除主将本身
        if main_hero in all_heroes:
            all_heroes.remove(main_hero)
        else:
            return [{"error": f"主将 {main_hero} 不存在"}]
        
        # 生成所有二人组合作为副将
        pairs = list(itertools.combinations(all_heroes, 2))
        
        # 为每个组合计算协同评分
        team_scores = []
        for pair in pairs:
            team = [main_hero] + list(pair)
            score = self.synergy_analyzer.calculate_synergy_score(team)
            team_scores.append({
                "队伍": team,
                "评分": score
            })
        
        # 按评分排序并返回前N个
        team_scores.sort(key=lambda x: x["评分"], reverse=True)
        return team_scores[:count]
    
    def recommend_teams_by_camp(self, camp: str, count: int = 10) -> List[Dict[str, Any]]:
        """推荐指定阵营的队伍"""
        # 获取指定阵营的所有武将
        all_heroes = []
        for hero_name in self.data_manager.get_all_hero_names():
            hero_info = self.data_manager.get_hero_by_name(hero_name)
            if hero_info and hero_info.get("阵营") == camp:
                all_heroes.append(hero_name)
        
        # 生成所有三人组合
        combinations = list(itertools.combinations(all_heroes, 3))
        
        # 计算每个组合的协同评分
        team_scores = []
        for combo in combinations:
            score = self.synergy_analyzer.calculate_synergy_score(list(combo))
            team_scores.append({
                "队伍": list(combo),
                "评分": score
            })
        
        # 按评分排序并返回前N个
        team_scores.sort(key=lambda x: x["评分"], reverse=True)
        return team_scores[:count]
    
    def recommend_teams_by_tag(self, tag: str, count: int = 10) -> List[Dict[str, Any]]:
        """推荐包含指定标签的队伍"""
        # 获取包含指定标签的所有武将
        tagged_heroes = []
        for hero_name in self.data_manager.get_all_hero_names():
            hero_info = self.data_manager.get_hero_by_name(hero_name)
            if hero_info and tag in hero_info.get("标签", []):
                tagged_heroes.append(hero_name)
        
        # 生成所有三人组合
        combinations = list(itertools.combinations(tagged_heroes, 3))
        
        # 计算每个组合的协同评分
        team_scores = []
        for combo in combinations:
            score = self.synergy_analyzer.calculate_synergy_score(list(combo))
            team_scores.append({
                "队伍": list(combo),
                "评分": score
            })
        
        # 按评分排序并返回前N个
        team_scores.sort(key=lambda x: x["评分"], reverse=True)
        return team_scores[:count]
    
    def filter_teams_by_criteria(
        self, 
        teams: List[Dict[str, Any]], 
        min_score: Optional[float] = None,
        required_heroes: Optional[List[str]] = None,
        excluded_heroes: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """根据指定条件过滤队伍推荐结果"""
        filtered_teams = []
        
        for team in teams:
            # 根据最低评分过滤
            if min_score and team["评分"] < min_score:
                continue
            
            # 根据必须包含的武将过滤
            if required_heroes:
                team_heroes = set(team["队伍"])
                required_set = set(required_heroes)
                if not required_set.issubset(team_heroes):
                    continue
            
            # 根据排除的武将过滤
            if excluded_heroes:
                team_heroes = set(team["队伍"])
                excluded_set = set(excluded_heroes)
                if team_heroes.intersection(excluded_set):
                    continue
            
            filtered_teams.append(team)
        
        return filtered_teams