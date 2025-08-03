# 推荐引擎
import itertools
from typing import List, Optional, Dict, Any

class Recommender:
    def __init__(self, data_manager, synergy_analyzer):
        self.data_manager = data_manager
        self.synergy_analyzer = synergy_analyzer
    
    def recommend_teams(self, count=10, required_hero=None, excluded_heroes=None, required_camp=None, required_tags=None, strategy="balanced"):
        """推荐最佳队伍组合 - 改进版"""
        # 获取所有可用武将
        all_heroes = self.data_manager.get_all_hero_names()
        
        # 处理必需阵营筛选
        if required_camp:
            filtered_heroes = []
            for hero_name in all_heroes:
                hero_info = self.data_manager.get_hero_by_name(hero_name)
                if hero_info and hero_info.get("阵营") == required_camp:
                    filtered_heroes.append(hero_name)
            all_heroes = filtered_heroes
        
        # 处理必需标签筛选
        if required_tags:
            filtered_heroes = []
            for hero_name in all_heroes:
                hero_info = self.data_manager.get_hero_by_name(hero_name)
                if hero_info:
                    hero_tags = hero_info.get("标签", [])
                    # 检查是否包含所有必需标签
                    if all(tag in hero_tags for tag in required_tags):
                        filtered_heroes.append(hero_name)
            all_heroes = filtered_heroes
        
        # 处理排除的武将
        if excluded_heroes:
            all_heroes = [hero for hero in all_heroes if hero not in excluded_heroes]
        
        # 生成队伍组合
        combinations = []
        if required_hero:
            # 如果指定了必须包含的武将
            if required_hero not in all_heroes:
                return {"error": f"必须包含的武将 {required_hero} 不在可用武将列表中"}
            
            # 从其他武将中选择2个与指定武将组合
            other_heroes = [hero for hero in all_heroes if hero != required_hero]
            combinations = []
            for combo in itertools.combinations(other_heroes, 2):
                combinations.append((required_hero,) + combo)
        else:
            # 根据不同策略生成队伍组合
            if strategy == "balanced":
                # 平衡策略：优先选择标签多样化的队伍
                combinations = self._generate_balanced_teams(all_heroes)
            elif strategy == "high_synergy":
                # 高协同策略：优先选择协同评分高的队伍
                combinations = self._generate_high_synergy_teams(all_heroes)
            else:
                # 默认策略：生成所有三人组合
                combinations = list(itertools.combinations(all_heroes, 3))
        
        # 计算每个组合的协同评分和详细分析
        team_scores = []
        for combo in combinations:
            # 计算协同评分
            score = self.synergy_analyzer.calculate_synergy_score(list(combo))
            
            team_scores.append({
                "队伍": list(combo),
                "评分": score
            })
        
        # 按评分排序并返回前N个
        team_scores.sort(key=lambda x: x["评分"], reverse=True)
        return team_scores[:count]
    
    def _generate_balanced_teams(self, all_heroes):
        """生成平衡策略的队伍组合"""
        # 按标签分组武将
        hero_groups = {}
        for hero_name in all_heroes:
            hero_info = self.data_manager.get_hero_by_name(hero_name)
            if hero_info:
                tags = hero_info.get("标签", [])
                # 使用主要标签分组
                main_tag = tags[0] if tags else "其他"
                if main_tag not in hero_groups:
                    hero_groups[main_tag] = []
                hero_groups[main_tag].append(hero_name)
        
        # 生成标签多样化的队伍组合
        combinations = []
        tags = list(hero_groups.keys())
        
        # 尝试从不同标签组中选择武将
        for i in range(len(tags)):
            for j in range(i+1, len(tags)):
                for k in range(j+1, len(tags)):
                    tag1_heroes = hero_groups[tags[i]]
                    tag2_heroes = hero_groups[tags[j]]
                    tag3_heroes = hero_groups[tags[k]]
                    
                    # 从每个标签组中选择一个武将
                    for hero1 in tag1_heroes[:5]:  # 限制每个标签组最多选择5个武将
                        for hero2 in tag2_heroes[:5]:
                            for hero3 in tag3_heroes[:5]:
                                combinations.append((hero1, hero2, hero3))
        
        # 补充同标签组的组合
        for tag, heroes in hero_groups.items():
            if len(heroes) >= 3:
                tag_combinations = list(itertools.combinations(heroes[:10], 3))  # 限制同标签组合数量
                combinations.extend(tag_combinations)
        
        # 去重并限制总数
        unique_combinations = list(set(combinations))
        return unique_combinations[:500]  # 限制组合数量以提高性能
    
    def _generate_high_synergy_teams(self, all_heroes):
        """生成高协同策略的队伍组合"""
        # 先计算所有武将两两间的协同评分
        hero_pairs = list(itertools.combinations(all_heroes, 2))
        pair_scores = []
        
        for pair in hero_pairs:
            score = self.synergy_analyzer.calculate_synergy_score(list(pair))
            pair_scores.append((pair, score))
        
        # 按协同评分排序
        pair_scores.sort(key=lambda x: x[1], reverse=True)
        
        # 选择协同评分高的武将对作为基础
        top_pairs = pair_scores[:50]  # 选择前50个高协同武将对
        
        # 为每个武将对添加第三个武将
        combinations = []
        for pair, score in top_pairs:
            # 为当前武将对寻找最佳的第三个武将
            best_third_hero = None
            best_total_score = 0
            
            for hero in all_heroes:
                if hero not in pair:
                    team = list(pair) + [hero]
                    total_score = self.synergy_analyzer.calculate_synergy_score(team)
                    if total_score > best_total_score:
                        best_total_score = total_score
                        best_third_hero = hero
            
            if best_third_hero:
                combinations.append(tuple(list(pair) + [best_third_hero]))
        
        return combinations
    
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
    
    def recommend_teams_explained(self, count=10, required_hero=None, excluded_heroes=None):
        """推荐最佳队伍组合并提供详细解释"""
        # 获取推荐结果
        recommendations = self.recommend_teams(count, required_hero, excluded_heroes)
        
        # 为每个推荐结果添加详细解释
        explained_recommendations = []
        
        for rec in recommendations:
            if "error" in rec:
                explained_recommendations.append(rec)
                continue
                
            team = rec["队伍"]
            score = rec["评分"]
            
            # 获取详细协同分析
            detailed_analysis = self.synergy_analyzer.analyze_synergy_detailed(team)
            
            # 生成推荐理由
            reasons = self._generate_recommendation_reasons(detailed_analysis)
            
            explained_rec = {
                "队伍": team,
                "评分": score,
                "推荐理由": reasons,
                "详细分析": detailed_analysis
            }
            
            explained_recommendations.append(explained_rec)
        
        return explained_recommendations
    
    def _generate_recommendation_reasons(self, detailed_analysis):
        """生成推荐理由"""
        reasons = []
        
        # 高分理由
        score = detailed_analysis.get("评分", 0)
        if score >= 90:
            reasons.append("综合协同评分极高，是非常优秀的队伍组合")
        elif score >= 80:
            reasons.append("综合协同评分很高，是优秀的队伍组合")
        elif score >= 70:
            reasons.append("综合协同评分良好，是不错的队伍组合")
        
        # 标签协同理由
        tag_analysis = detailed_analysis.get("标签分析", {})
        tag_synergies = tag_analysis.get("标签协同", {})
        if tag_synergies:
            synergy_count = len(tag_synergies)
            reasons.append(f"存在{synergy_count}个高价值标签协同组合")
        
        # 兵种克制理由
        troop_analysis = detailed_analysis.get("兵种分析", {})
        advantages = troop_analysis.get("兵种克制关系", [])
        if advantages:
            advantage_count = len(advantages)
            reasons.append(f"存在{advantage_count}个兵种克制关系，在对抗相应兵种时有优势")
        
        # 阵营加成理由
        camp_analysis = detailed_analysis.get("阵营分析", {})
        camp_bonus = camp_analysis.get("阵营加成", "未激活")
        if camp_bonus == "激活":
            reasons.append("激活了阵营加成，获得额外属性提升")
        
        # 战法协同理由
        skill_analysis = detailed_analysis.get("战法分析", {})
        synergy_potential = skill_analysis.get("协同潜力分析", {})
        potential_combinations = synergy_potential.get("潜在协同组合", [])
        if potential_combinations:
            reasons.append("存在战法协同潜力，能够形成良好的战法配合")
        
        return reasons if reasons else ["该队伍组合具有良好的平衡性"]