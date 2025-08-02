# 数据管理器
import json
import os

class DataManager:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.data = self._load_data()
    
    def _load_data(self):
        """加载游戏数据"""
        try:
            # 检查文件是否存在
            if not os.path.exists(self.data_file_path):
                # 如果文件不存在，尝试在项目根目录查找
                root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                data_file_path = os.path.join(root_dir, "data", "consolidated_ocr_data.json")
                if not os.path.exists(data_file_path):
                    raise FileNotFoundError(f"数据文件未找到: {self.data_file_path} 或 {data_file_path}")
                self.data_file_path = data_file_path
            
            # 读取JSON数据
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"加载数据文件时出错: {e}")
            return {}
    
    def get_heroes(self):
        """获取所有武将"""
        return self.data.get('武将', {})
    
    def get_skills(self):
        """获取所有战法"""
        return self.data.get('战法', {})
    
    def get_hero_by_name(self, name):
        """根据名称获取武将信息"""
        return self.data.get('武将', {}).get(name)
    
    def get_skill_by_name(self, name):
        """根据名称获取战法信息"""
        return self.data.get('战法', {}).get(name)
    
    def get_all_hero_names(self):
        """获取所有武将名称列表"""
        return list(self.data.get('武将', {}).keys())
    
    def get_all_skill_names(self):
        """获取所有战法名称列表"""
        return list(self.data.get('战法', {}).keys())
    
    def get_hero_attribute(self, hero_name, attribute):
        """获取武将指定属性值"""
        hero = self.get_hero_by_name(hero_name)
        if hero and '属性' in hero:
            return hero['属性'].get(attribute, {})
        return {}
    
    def get_hero_troop_fitness(self, hero_name, troop_type):
        """获取武将指定兵种适性"""
        hero = self.get_hero_by_name(hero_name)
        if hero and '兵种' in hero:
            return hero['兵种'].get(troop_type, '')
        return ''
    
    def search_heroes(self, keyword):
        """根据关键字搜索武将"""
        heroes = self.get_heroes()
        result = {}
        for name, info in heroes.items():
            if keyword.lower() in name.lower() or keyword.lower() in str(info).lower():
                result[name] = info
        return result
    
    def search_skills(self, keyword):
        """根据关键字搜索战法"""
        skills = self.get_skills()
        result = {}
        for name, info in skills.items():
            if keyword.lower() in name.lower() or keyword.lower() in str(info).lower():
                result[name] = info
        return result