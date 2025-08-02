# 战法协同分析器

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
    
    def calculate_synergy_score(self, hero_team):
        """计算队伍协同评分"""
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
        
        # 综合评分（可根据需要调整权重）
        total_score = (
            tag_score * 0.25 +
            troop_score * 0.25 +
            camp_score * 0.25 +
            skill_score * 0.25
        )
        
        return round(total_score, 2)
    
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
    
    def _calculate_tag_synergy(self, heroes_info):
        """计算标签协同得分"""
        # 简单实现：根据相同标签数量计算得分
        all_tags = []
        for hero_info in heroes_info.values():
            tags = hero_info.get("标签", [])
            all_tags.extend(tags)
        
        # 计算重复标签的协同值
        tag_count = {}
        for tag in all_tags:
            tag_count[tag] = tag_count.get(tag, 0) + 1
        
        # 根据重复标签数量计算得分
        score = 0
        for count in tag_count.values():
            if count > 1:
                # 有重复标签，加分
                score += (count - 1) * 10
        
        # 最高不超过100分
        return min(score, 100)
    
    def _calculate_troop_synergy(self, heroes_info):
        """计算兵种协同得分"""
        # 简单实现：根据S级兵种数量计算得分
        s_troop_count = 0
        for hero_info in heroes_info.values():
            troops = hero_info.get("兵种", {})
            for fitness in troops.values():
                if fitness == "S":
                    s_troop_count += 1
                    break  # 每个武将只计算一次
        
        # 每有一个S级兵种加10分，最高100分
        return min(s_troop_count * 10, 100)
    
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
        """计算战法协同得分"""
        # 这里需要更复杂的逻辑来分析战法之间的协同效应
        # 简单实现：根据武将数量给基础分
        hero_count = len(heroes_info)
        return min(hero_count * 25, 100)
    
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