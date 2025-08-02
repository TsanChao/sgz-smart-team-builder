# 数据管理器

class DataManager:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.data = self._load_data()
    
    def _load_data(self):
        """加载游戏数据"""
        # 实现数据加载逻辑
        pass
    
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