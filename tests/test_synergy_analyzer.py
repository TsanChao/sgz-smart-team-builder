#!/usr/bin/env python3
# 测试协同分析器

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data_manager import DataManager
from core.synergy_analyzer import SynergyAnalyzer

def test_synergy_analyzer():
    """测试协同分析器"""
    # 创建数据管理器实例
    data_manager = DataManager("data/consolidated_ocr_data.json")
    
    # 创建协同分析器实例
    synergy_analyzer = SynergyAnalyzer(data_manager)
    
    # 测试分析协同效应
    team_heroes = ["曹操", "夏侯惇", "荀彧"]
    print(f"分析队伍 {team_heroes} 的协同效应:")
    synergy_result = synergy_analyzer.analyze_synergy(team_heroes)
    print(f"协同分析结果: {synergy_result}")
    
    # 测试计算协同评分
    synergy_score = synergy_analyzer.calculate_synergy_score(team_heroes)
    print(f"协同评分为: {synergy_score}")

if __name__ == "__main__":
    test_synergy_analyzer()