#!/usr/bin/env python3
# 测试推荐引擎

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.data_manager import DataManager
from core.synergy_analyzer import SynergyAnalyzer
from core.recommender import Recommender

def test_recommender():
    """测试推荐引擎"""
    # 创建数据管理器实例
    data_manager = DataManager("data/consolidated_ocr_data.json")
    
    # 创建协同分析器实例
    synergy_analyzer = SynergyAnalyzer(data_manager)
    
    # 创建推荐引擎实例
    recommender = Recommender(data_manager, synergy_analyzer)
    
    # 测试推荐最佳队伍组合
    print("=== 推荐最佳队伍组合 ===")
    best_teams = recommender.recommend_teams(count=5)
    for i, team in enumerate(best_teams, 1):
        print(f"{i}. 队伍: {team['队伍']}, 评分: {team['评分']}")
    
    print("\n=== 为曹操推荐副将组合 ===")
    cao_cao_teams = recommender.recommend_single_hero_team("曹操", count=5)
    for i, team in enumerate(cao_cao_teams, 1):
        print(f"{i}. 队伍: {team['队伍']}, 评分: {team['评分']}")
    
    print("\n=== 推荐魏国阵营队伍 ===")
    wei_teams = recommender.recommend_teams_by_camp("魏", count=5)
    for i, team in enumerate(wei_teams, 1):
        print(f"{i}. 队伍: {team['队伍']}, 评分: {team['评分']}")
    
    print("\n=== 推荐包含'辅'标签的队伍 ===")
    fu_teams = recommender.recommend_teams_by_tag("辅", count=5)
    for i, team in enumerate(fu_teams, 1):
        print(f"{i}. 队伍: {team['队伍']}, 评分: {team['评分']}")

if __name__ == "__main__":
    test_recommender()