# 战法协同分析器

import hashlib
import json

class SynergyAnalyzer:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        # 定义协同规则
        self.synergy_rules = {
            "control_damage": 90,    # 控制+输出协同
            "debuff_damage": 85,    # 状态+输出协同
            "buff_damage": 80,      # 增益+输出协同
            "control_debuff": 75,    # 控制+状态协同
            "heal_buff": 75,        # 治疗+增益协同
            "same_type": 60         # 同类效果协同
        }
        # 协同评分缓存
        self._score_cache = {}
        self._cache_max_size = 10000
    
    def analyze_synergy(self, team_heroes):
        """分析队伍中武将的协同效应"""
        if not team_heroes or len(team_heroes) == 0:
            return {"error": "队伍不能为空"}
        
        # 获取队伍中每个武将的信息
        heroes_info = {}
        for hero_name in team_heroes:
            hero_info = self.data_manager.get_hero_by_name(hero_name)
            if hero_info:
                heroes_info[hero_name] = hero_info
            else:
                return {"error": f"未找到武将 {hero_name} 的信息"}
        
        # 分析队伍标签组合
        tags_analysis = self._analyze_tags(heroes_info)
        
        # 分析兵种搭配
        troops_analysis = self._analyze_troops(heroes_info)
        
        # 分析阵营加成
        camp_analysis = self._analyze_camp(heroes_info)
        
        # 分析战法协同
        skills_analysis = self._analyze_skills(heroes_info)
        
        return {
            "队伍构成": team_heroes,
            "标签分析": tags_analysis,
            "兵种分析": troops_analysis,
            "阵营分析": camp_analysis,
            "战法分析": skills_analysis
        }
    
    def analyze_synergy_detailed(self, team_heroes):
        """详细分析队伍中武将的协同效应"""
        if not team_heroes or len(team_heroes) == 0:
            return {"error": "队伍不能为空"}
        
        # 获取队伍中每个武将的信息
        heroes_info = {}
        for hero_name in team_heroes:
            hero_info = self.data_manager.get_hero_by_name(hero_name)
            if hero_info:
                heroes_info[hero_name] = hero_info
            else:
                return {"error": f"未找到武将 {hero_name} 的信息"}
        
        # 分析各项协同效应
        tags_analysis = self._analyze_tags_detailed(heroes_info)
        troops_analysis = self._analyze_troops_detailed(heroes_info)
        camp_analysis = self._analyze_camp_detailed(heroes_info)
        skills_analysis = self._analyze_skills_detailed(heroes_info)
        
        # 生成综合建议
        recommendations = self._generate_recommendations(
            tags_analysis, troops_analysis, camp_analysis, skills_analysis)
        
        return {
            "队伍构成": team_heroes,
            "标签分析": tags_analysis,
            "兵种分析": troops_analysis,
            "阵营分析": camp_analysis,
            "战法分析": skills_analysis,
            "综合建议": recommendations
        }
    
    def calculate_synergy_score(self, hero_team):
        """计算队伍协同评分 - 带缓存优化"""
        # 生成缓存键
        cache_key = self._generate_cache_key(hero_team)
        
        # 检查缓存
        if cache_key in self._score_cache:
            return self._score_cache[cache_key]
        
        # 计算协同评分
        score = self._calculate_synergy_score_internal(hero_team)
        
        # 更新缓存
        self._update_cache(cache_key, score)
        
        return score
    
    def _generate_cache_key(self, hero_team):
        """生成缓存键"""
        # 对武将列表排序以确保相同队伍的不同顺序使用同一缓存
        sorted_team = sorted(hero_team)
        team_str = json.dumps(sorted_team, ensure_ascii=False)
        # 使用MD5生成固定长度的键
        return hashlib.md5(team_str.encode('utf-8')).hexdigest()
    
    def _update_cache(self, cache_key, score):
        """更新缓存"""
        # 如果缓存已满，删除一部分旧缓存
        if len(self._score_cache) >= self._cache_max_size:
            # 删除10%最旧的缓存项
            keys_to_remove = list(self._score_cache.keys())[:self._cache_max_size // 10]
            for key in keys_to_remove:
                del self._score_cache[key]
        
        self._score_cache[cache_key] = score
    
    def _calculate_synergy_score_internal(self, hero_team):
        """内部计算协同评分的方法"""
        if not hero_team or len(hero_team) == 0:
            return 0
        
        # 获取队伍中每个武将的信息
        heroes_info = {}
        for hero_name in hero_team:
            hero_info = self.data_manager.get_hero_by_name(hero_name)
            if hero_info:
                heroes_info[hero_name] = hero_info
            else:
                return 0  # 如果找不到武将信息，返回0分
        
        # 计算各项协同得分
        tag_score = self._calculate_tag_synergy(heroes_info)
        troop_score = self._calculate_troop_synergy(heroes_info)
        camp_score = self._calculate_camp_synergy(heroes_info)
        skill_score = self._calculate_skill_synergy(heroes_info)
        
        # 根据游戏机制调整权重
        # 战法协同最重要(35%)，其次是标签协同(25%)，兵种协同(25%)，阵营协同(15%)
        total_score = (
            tag_score * 0.25 +
            troop_score * 0.25 +
            camp_score * 0.15 +
            skill_score * 0.35
        )
        
        return round(total_score, 2)
    
    def _analyze_tags_detailed(self, heroes_info):
        """详细分析队伍标签组合"""
        all_tags = []
        hero_tags = {}
        
        for hero_name, hero_info in heroes_info.items():
            tags = hero_info.get("标签", [])
            hero_tags[hero_name] = tags
            all_tags.extend(tags)
        
        # 统计标签频率
        tag_count = {}
        for tag in all_tags:
            tag_count[tag] = tag_count.get(tag, 0) + 1
        
        # 分析标签协同效应
        tag_synergies = []
        tag_combinations = {}
        
        # 定义标签协同价值
        tag_synergy_values = {
            ("控制", "输出"): "控制+输出组合，能够有效限制敌方并造成伤害",
            ("控制", "谋略"): "控制+谋略组合，适合策略性战斗",
            ("输出", "谋略"): "物理+谋略双输出，伤害类型多样化",
            ("治疗", "增益"): "治疗+增益组合，提供持续战力支持",
            ("防御", "辅助"): "防御+辅助组合，提高队伍生存能力"
        }
        
        hero_names = list(hero_tags.keys())
        for i in range(len(hero_names)):
            for j in range(i+1, len(hero_names)):
                hero1, hero2 = hero_names[i], hero_names[j]
                tags1, tags2 = hero_tags[hero1], hero_tags[hero2]
                
                # 检查是否有高价值标签组合
                for tag1 in tags1:
                    for tag2 in tags2:
                        if (tag1, tag2) in tag_synergy_values:
                            tag_combinations[f"{hero1}+{hero2}"] = {
                                "标签组合": f"{tag1}+{tag2}",
                                "说明": tag_synergy_values[(tag1, tag2)]
                            }
                        elif (tag2, tag1) in tag_synergy_values:
                            tag_combinations[f"{hero1}+{hero2}"] = {
                                "标签组合": f"{tag2}+{tag1}",
                                "说明": tag_synergy_values[(tag2, tag1)]
                            }
        
        return {
            "标签列表": list(set(all_tags)),
            "标签统计": tag_count,
            "标签协同": tag_combinations,
            "分析": f"队伍中共有{len(set(all_tags))}种不同标签，{len([t for t in tag_count.values() if t > 1])}个重复标签"
        }
    
    def _analyze_troops_detailed(self, heroes_info):
        """详细分析兵种搭配"""
        all_troops = {}
        hero_troops = {}
        
        for hero_name, hero_info in heroes_info.items():
            troops = hero_info.get("兵种", {})
            hero_troops[hero_name] = troops
            for troop_type, fitness in troops.items():
                if troop_type not in all_troops:
                    all_troops[troop_type] = []
                all_troops[troop_type].append({"武将": hero_name, "适性": fitness})
        
        # 分析兵种相克关系
        troop_advantages = {
            "骑兵": "盾兵",
            "盾兵": "弓兵", 
            "弓兵": "枪兵",
            "枪兵": "骑兵"
        }
        
        advantages_found = []
        for troop_type, advantage in troop_advantages.items():
            if troop_type in all_troops and advantage in all_troops:
                troop_list = [t["武将"] for t in all_troops[troop_type]]
                advantage_list = [t["武将"] for t in all_troops[advantage]]
                advantages_found.append({
                    "克制关系": f"{troop_type}克制{advantage}",
                    "拥有兵种武将": troop_list,
                    "被克制兵种武将": advantage_list
                })
        
        # 分析兵种适性分布
        fitness_analysis = {}
        fitness_values = {"S": 5, "A": 4, "B": 3, "C": 2}
        
        for troop_type, troop_info_list in all_troops.items():
            total_fitness = 0
            count = 0
            for troop_info in troop_info_list:
                fitness = troop_info["适性"]
                if fitness in fitness_values:
                    total_fitness += fitness_values[fitness]
                    count += 1
            
            avg_fitness_value = total_fitness / count if count > 0 else 0
            if avg_fitness_value >= 4.5:
                avg_fitness = "S"
            elif avg_fitness_value >= 3.5:
                avg_fitness = "A"
            elif avg_fitness_value >= 2.5:
                avg_fitness = "B"
            else:
                avg_fitness = "C"
            
            fitness_analysis[troop_type] = {
                "适性列表": [t["适性"] for t in troop_info_list],
                "平均适性": avg_fitness,
                "武将列表": troop_info_list
            }
        
        return {
            "兵种分布": all_troops,
            "兵种适性分析": fitness_analysis,
            "兵种克制关系": advantages_found,
            "分析": f"队伍共包含{len(all_troops)}种兵种，其中{len(advantages_found)}个兵种克制关系"
        }
    
    def _analyze_camp_detailed(self, heroes_info):
        """详细分析阵营加成"""
        camps = []
        hero_camps = {}
        
        for hero_name, hero_info in heroes_info.items():
            camp = hero_info.get("阵营", "")
            hero_camps[hero_name] = camp
            camps.append(camp)
        
        # 统计阵营分布
        camp_count = {}
        for camp in camps:
            camp_count[camp] = camp_count.get(camp, 0) + 1
        
        # 阵营加成分析
        camp_bonus = "未激活"
        bonus_description = "队伍中武将来自不同阵营，无法获得阵营加成"
        
        if len(set(camps)) == 1 and camps[0] != "":
            camp_bonus = "激活"
            bonus_description = f"所有武将均为{camps[0]}阵营，获得阵营加成"
        
        return {
            "阵营列表": camps,
            "阵营统计": camp_count,
            "阵营加成": camp_bonus,
            "加成说明": bonus_description,
            "武将阵营分布": hero_camps
        }
    
    def _analyze_skills_detailed(self, heroes_info):
        """详细分析战法协同"""
        skills_info = []
        hero_skills = {}
        
        for hero_name, hero_info in heroes_info.items():
            own_skill = hero_info.get("自带战法", "")
            inherit_skill = hero_info.get("传承战法", "")
            hero_skills[hero_name] = {"自带战法": own_skill, "传承战法": inherit_skill}
            
            if own_skill:
                skill_detail = self.data_manager.get_skill_by_name(own_skill)
                if skill_detail:
                    skills_info.append({
                        "武将": hero_name,
                        "战法": own_skill,
                        "详情": skill_detail,
                        "类型": "自带"
                    })
            
            if inherit_skill:
                skill_detail = self.data_manager.get_skill_by_name(inherit_skill)
                if skill_detail:
                    skills_info.append({
                        "武将": hero_name,
                        "战法": inherit_skill,
                        "详情": skill_detail,
                        "类型": "传承"
                    })
        
        # 分析战法类型分布
        skill_types = {}
        skill_quality = {}
        
        for skill in skills_info:
            skill_detail = skill["详情"]
            skill_type = skill_detail.get("类型", "未知")
            quality = skill_detail.get("品质", "未知")
            
            if skill_type not in skill_types:
                skill_types[skill_type] = []
            skill_types[skill_type].append(skill)
            
            if quality not in skill_quality:
                skill_quality[quality] = []
            skill_quality[quality].append(skill)
        
        # 分析战法协同潜力
        synergy_potential = self._analyze_skill_synergy_potential(skills_info)
        
        return {
            "涉及战法": [skill["战法"] for skill in skills_info],
            "武将战法对应": hero_skills,
            "战法详情": skills_info,
            "战法类型分布": skill_types,
            "战法品质分布": skill_quality,
            "协同潜力分析": synergy_potential
        }
    
    def _analyze_skill_synergy_potential(self, skills_info):
        """分析战法协同潜力"""
        # 定义战法协同规则
        synergy_rules = {
            ("主动", "被动"): "主动+被动战法组合，能够形成良好的攻防配合",
            ("指挥", "主动"): "指挥+主动战法组合，前期和中后期都有发挥",
            ("追击", "输出"): "追击+输出战法组合，能够形成连续伤害",
            ("控制", "输出"): "控制+输出战法组合，先控后输出效果显著"
        }
        
        potential_combinations = []
        for i in range(len(skills_info)):
            for j in range(i+1, len(skills_info)):
                skill1 = skills_info[i]
                skill2 = skills_info[j]
                
                type1 = skill1["详情"].get("类型", "未知")
                type2 = skill2["详情"].get("类型", "未知")
                
                if (type1, type2) in synergy_rules:
                    potential_combinations.append({
                        "战法组合": f"{skill1['战法']}+{skill2['战法']}",
                        "组合类型": f"{type1}+{type2}",
                        "说明": synergy_rules[(type1, type2)],
                        "涉及武将": [skill1["武将"], skill2["武将"]]
                    })
                elif (type2, type1) in synergy_rules:
                    potential_combinations.append({
                        "战法组合": f"{skill1['战法']}+{skill2['战法']}",
                        "组合类型": f"{type2}+{type1}",
                        "说明": synergy_rules[(type2, type1)],
                        "涉及武将": [skill1["武将"], skill2["武将"]]
                    })
        
        return {
            "潜在协同组合": potential_combinations,
            "分析": f"发现{len(potential_combinations)}个潜在协同组合"
        }
    
    def _generate_recommendations(self, tags_analysis, troops_analysis, camp_analysis, skills_analysis):
        """生成个性化建议"""
        recommendations = []
        
        # 标签建议
        tag_stats = tags_analysis.get("标签统计", {})
        repeated_tags = [tag for tag, count in tag_stats.items() if count > 1]
        if repeated_tags:
            recommendations.append({
                "类型": "标签协同",
                "建议": f"队伍中存在重复标签 {', '.join(repeated_tags)}，可考虑利用标签协同效应"
            })
        else:
            recommendations.append({
                "类型": "标签搭配",
                "建议": "队伍标签类型丰富，建议保持标签多样性以适应不同战斗场景"
            })
        
        # 兵种建议
        advantages = troops_analysis.get("兵种克制关系", [])
        if advantages:
            advantage_desc = ", ".join([a["克制关系"] for a in advantages])
            recommendations.append({
                "类型": "兵种克制",
                "建议": f"队伍中存在兵种克制关系: {advantage_desc}，在对抗相应兵种时有优势"
            })
        
        # 阵营建议
        camp_bonus = camp_analysis.get("阵营加成", "未激活")
        if camp_bonus == "激活":
            recommendations.append({
                "类型": "阵营加成",
                "建议": "队伍已激活阵营加成，可考虑围绕阵营特色构建更完整的阵容"
            })
        else:
            recommendations.append({
                "类型": "阵营搭配",
                "建议": "队伍来自不同阵营，建议考虑选择同一阵营武将以获得阵营加成"
            })
        
        # 战法建议
        synergy_potential = skills_analysis.get("协同潜力分析", {})
        potential_combinations = synergy_potential.get("潜在协同组合", [])
        if potential_combinations:
            combo_desc = ", ".join([c["战法组合"] for c in potential_combinations[:2]])
            recommendations.append({
                "类型": "战法协同",
                "建议": f"存在战法协同潜力: {combo_desc}，建议在战斗中注意战法发动时机"
            })
        
        return recommendations
    
    def _analyze_troops(self, heroes_info):
        """分析兵种搭配"""
        all_troops = {}
        for hero_name, hero_info in heroes_info.items():
            troops = hero_info.get("兵种", {})
            for troop_type, fitness in troops.items():
                if troop_type not in all_troops:
                    all_troops[troop_type] = []
                all_troops[troop_type].append(fitness)
        
        # 分析每个兵种的适性分布
        analysis = {}
        for troop_type, fitness_list in all_troops.items():
            analysis[troop_type] = {
                "适性列表": fitness_list,
                "平均适性": self._average_fitness(fitness_list)
            }
        
        return analysis
    
    def _analyze_camp(self, heroes_info):
        """分析阵营加成"""
        camps = []
        for hero_name, hero_info in heroes_info.items():
            camp = hero_info.get("阵营", "")
            camps.append(camp)
        
        # 统计阵营分布
        camp_count = {}
        for camp in camps:
            camp_count[camp] = camp_count.get(camp, 0) + 1
        
        return {
            "阵营列表": camps,
            "阵营统计": camp_count,
            "阵营加成": "激活" if len(set(camps)) == 1 else "未激活"
        }
    
    def _analyze_skills(self, heroes_info):
        """分析战法协同"""
        skills = []
        for hero_name, hero_info in heroes_info.items():
            own_skill = hero_info.get("自带战法", "")
            inherit_skill = hero_info.get("传承战法", "")
            if own_skill:
                skills.append(own_skill)
            if inherit_skill:
                skills.append(inherit_skill)
        
        return {
            "涉及战法": skills
        }
    
    def _calculate_tag_synergy(self, heroes_info):
        """计算标签协同得分 - 改进版"""
        # 定义标签协同价值矩阵
        tag_synergy_values = {
            ("控制", "输出"): 90,
            ("控制", "谋略"): 85,
            ("输出", "谋略"): 80,
            ("治疗", "增益"): 75,
            ("控制", "辅助"): 70,
            ("防御", "辅助"): 65
        }
        
        # 获取所有武将的标签
        hero_tags = {}
        all_tags = []
        for hero_name, hero_info in heroes_info.items():
            tags = hero_info.get("标签", [])
            hero_tags[hero_name] = tags
            all_tags.extend(tags)
        
        # 计算标签协同值
        total_synergy = 0
        tag_combinations = 0
        
        # 遍历武将组合，分析标签协同
        hero_names = list(hero_tags.keys())
        for i in range(len(hero_names)):
            for j in range(i+1, len(hero_names)):
                hero1_tags = hero_tags[hero_names[i]]
                hero2_tags = hero_tags[hero_names[j]]
                
                # 计算两个武将间的标签协同
                synergy = self._calculate_two_heroes_tag_synergy(
                    hero1_tags, hero2_tags, tag_synergy_values)
                total_synergy += synergy
                if synergy > 0:
                    tag_combinations += 1
        
        # 计算平均协同值
        if tag_combinations > 0:
            avg_synergy = total_synergy / tag_combinations
            # 考虑协同组合数量的加成
            count_bonus = min(tag_combinations * 10, 50)  # 最多50分加成
            return min(avg_synergy + count_bonus, 100)
        
        # 回退到基础实现
        tag_count = {}
        for tag in all_tags:
            tag_count[tag] = tag_count.get(tag, 0) + 1
        
        score = 0
        for count in tag_count.values():
            if count > 1:
                score += (count - 1) * 15  # 提高单个重复标签的价值
        
        return min(score, 100)
    
    def _calculate_two_heroes_tag_synergy(self, tags1, tags2, synergy_values):
        """计算两个武将间的标签协同值"""
        max_synergy = 0
        
        for tag1 in tags1:
            for tag2 in tags2:
                # 检查正向组合
                if (tag1, tag2) in synergy_values:
                    synergy = synergy_values[(tag1, tag2)]
                    max_synergy = max(max_synergy, synergy)
                # 检查反向组合
                elif (tag2, tag1) in synergy_values:
                    synergy = synergy_values[(tag2, tag1)]
                    max_synergy = max(max_synergy, synergy)
        
        return max_synergy
    
    def _calculate_troop_synergy(self, heroes_info):
        """计算兵种协同得分 - 改进版"""
        # 兵种相克关系：骑兵→盾兵→弓兵→枪兵→骑兵
        troop_advantage = {
            "骑兵": "盾兵",
            "盾兵": "弓兵", 
            "弓兵": "枪兵",
            "枪兵": "骑兵"
        }
        
        # 获取队伍中所有武将的兵种信息
        hero_troops = {}
        for hero_name, hero_info in heroes_info.items():
            troops = hero_info.get("兵种", {})
            hero_troops[hero_name] = troops
        
        # 兵种适性等级值
        fitness_values = {"S": 5, "A": 4, "B": 3, "C": 2}
        
        # 计算兵种协同得分
        total_score = 0
        
        # 1. 兵种适性得分
        fitness_score = 0
        for hero_troops_info in hero_troops.values():
            hero_fitness_score = 0
            for fitness in hero_troops_info.values():
                if fitness in fitness_values:
                    hero_fitness_score += fitness_values[fitness]
            fitness_score += hero_fitness_score / len(hero_troops_info) if hero_troops_info else 0
        
        # 平均适性得分（最高25分）
        avg_fitness_score = (fitness_score / len(hero_troops)) * 5 if hero_troops else 0
        total_score += min(avg_fitness_score, 25)
        
        # 2. 兵种搭配得分
        # 统计队伍中各兵种的适性分布
        troop_distribution = {}
        for hero_troops_info in hero_troops.values():
            for troop_type, fitness in hero_troops_info.items():
                if troop_type not in troop_distribution:
                    troop_distribution[troop_type] = []
                troop_distribution[troop_type].append(fitness)
        
        # 计算兵种搭配多样性得分（最多25分）
        diversity_score = min(len(troop_distribution) * 8, 25)
        total_score += diversity_score
        
        # 3. 兵种相克得分
        advantage_score = 0
        hero_names = list(hero_troops.keys())
        for i in range(len(hero_names)):
            for j in range(i+1, len(hero_names)):
                hero1_troops = hero_troops[hero_names[i]]
                hero2_troops = hero_troops[hero_names[j]]
                
                # 检查是否存在兵种相克关系
                for troop1, fitness1 in hero1_troops.items():
                    if troop1 in troop_advantage:
                        advantage_troop = troop_advantage[troop1]
                        if advantage_troop in hero2_troops:
                            # 存在相克关系，加分
                            advantage_score += 5
        
        total_score += min(advantage_score, 25)
        
        # 4. S级兵种加成
        s_troop_bonus = 0
        for hero_troops_info in hero_troops.values():
            for fitness in hero_troops_info.values():
                if fitness == "S":
                    s_troop_bonus += 5
        
        total_score += min(s_troop_bonus, 25)
        
        return min(total_score, 100)
    
    def _calculate_camp_synergy(self, heroes_info):
        """计算阵营协同得分"""
        # 获取所有武将的阵营
        camps = []
        for hero_info in heroes_info.values():
            camp = hero_info.get("阵营", "")
            camps.append(camp)
        
        # 如果所有武将属于同一阵营，获得阵营加成
        if len(set(camps)) == 1 and camps[0] != "":
            return 100
        return 0
    
    def _calculate_skill_synergy(self, heroes_info):
        """计算战法协同得分 - 改进版"""
        # 获取队伍中所有武将的战法信息
        skills_info = []
        for hero_name, hero_info in heroes_info.items():
            own_skill = hero_info.get("自带战法", "")
            inherit_skill = hero_info.get("传承战法", "")
            if own_skill:
                skill_detail = self.data_manager.get_skill_by_name(own_skill)
                if skill_detail:
                    skills_info.append({
                        "hero": hero_name,
                        "skill": own_skill,
                        "detail": skill_detail,
                        "type": "own"
                    })
            if inherit_skill:
                skill_detail = self.data_manager.get_skill_by_name(inherit_skill)
                if skill_detail:
                    skills_info.append({
                        "hero": hero_name,
                        "skill": inherit_skill,
                        "detail": skill_detail,
                        "type": "inherit"
                    })
        
        # 分析战法间协同关系
        total_synergy = 0
        synergy_pairs = 0
        
        # 遍历战法组合，分析协同效应
        for i in range(len(skills_info)):
            for j in range(i+1, len(skills_info)):
                skill1 = skills_info[i]
                skill2 = skills_info[j]
                
                # 计算两个战法间的协同值
                synergy = self._calculate_two_skills_synergy(skill1, skill2)
                total_synergy += synergy
                synergy_pairs += 1
        
        # 计算平均协同值
        if synergy_pairs > 0:
            avg_synergy = total_synergy / synergy_pairs
            # 考虑协同关系数量的加成
            count_bonus = min(synergy_pairs * 5, 50)  # 最多50分加成
            return min(avg_synergy + count_bonus, 100)
        
        # 默认基础分
        hero_count = len(heroes_info)
        return min(hero_count * 20, 100)
    
    def _calculate_two_skills_synergy(self, skill1, skill2):
        """计算两个战法间的协同值"""
        # 获取战法详情
        detail1 = skill1["detail"]
        detail2 = skill2["detail"]
        
        # 战法协同规则
        synergy_rules = {
            ("主动", "被动"): 90,
            ("指挥", "主动"): 85,
            ("追击", "输出"): 80,
            ("控制", "输出"): 75,
            ("治疗", "增益"): 70
        }
        
        # 获取战法类型
        type1 = detail1.get("类型", "未知")
        type2 = detail2.get("类型", "未知")
        
        # 检查协同规则
        if (type1, type2) in synergy_rules:
            return synergy_rules[(type1, type2)]
        elif (type2, type1) in synergy_rules:
            return synergy_rules[(type2, type1)]
        
        # 默认协同值
        return 30
    
    def _analyze_tags(self, heroes_info):
        """分析队伍标签组合"""
        all_tags = []
        for hero_name, hero_info in heroes_info.items():
            tags = hero_info.get("标签", [])
            all_tags.extend(tags)
        
        # 统计标签频率
        tag_count = {}
        for tag in all_tags:
            tag_count[tag] = tag_count.get(tag, 0) + 1
        
        return {
            "标签列表": list(set(all_tags)),
            "标签统计": tag_count
        }
    
    def _analyze_troops(self, heroes_info):
        """分析兵种搭配"""
        all_troops = {}
        for hero_name, hero_info in heroes_info.items():
            troops = hero_info.get("兵种", {})
            for troop_type, fitness in troops.items():
                if troop_type not in all_troops:
                    all_troops[troop_type] = []
                all_troops[troop_type].append(fitness)
        
        # 分析每个兵种的适性分布
        analysis = {}
        for troop_type, fitness_list in all_troops.items():
            analysis[troop_type] = {
                "适性列表": fitness_list,
                "平均适性": self._average_fitness(fitness_list)
            }
        
        return analysis
    
    def _analyze_camp(self, heroes_info):
        """分析阵营加成"""
        camps = []
        for hero_name, hero_info in heroes_info.items():
            camp = hero_info.get("阵营", "")
            camps.append(camp)
        
        # 统计阵营分布
        camp_count = {}
        for camp in camps:
            camp_count[camp] = camp_count.get(camp, 0) + 1
        
        return {
            "阵营列表": camps,
            "阵营统计": camp_count,
            "阵营加成": "激活" if len(set(camps)) == 1 else "未激活"
        }
    
    def _analyze_skills(self, heroes_info):
        """分析战法协同"""
        skills = []
        for hero_name, hero_info in heroes_info.items():
            own_skill = hero_info.get("自带战法", "")
            inherit_skill = hero_info.get("传承战法", "")
            if own_skill:
                skills.append(own_skill)
            if inherit_skill:
                skills.append(inherit_skill)
        
        return {
            "涉及战法": skills
        }
    
    def _average_fitness(self, fitness_list):
        """计算兵种适性的平均值"""
        if not fitness_list:
            return ""
        
        # 定义适性等级值
        fitness_values = {"S": 5, "A": 4, "B": 3, "C": 2}
        
        # 计算总分
        total = 0
        count = 0
        for fitness in fitness_list:
            if fitness in fitness_values:
                total += fitness_values[fitness]
                count += 1
        
        if count == 0:
            return ""
        
        # 计算平均值并转换回等级
        avg_value = total / count
        if avg_value >= 4.5:
            return "S"
        elif avg_value >= 3.5:
            return "A"
        elif avg_value >= 2.5:
            return "B"
        else:
            return "C"