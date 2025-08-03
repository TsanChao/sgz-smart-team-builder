#!/usr/bin/env python3
# 测试推荐引擎

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    
    # 测试不存在的主将推荐
    print("\n=== 为不存在的武将推荐副将组合 ===")
    invalid_hero_teams = recommender.recommend_single_hero_team("不存在的武将", count=5)
    print(f"错误结果: {invalid_hero_teams}")
    
    # 测试不存在的阵营推荐
    print("\n=== 推荐不存在的阵营队伍 ===")
    invalid_camp_teams = recommender.recommend_teams_by_camp("不存在的阵营", count=5)
    print(f"不存在阵营的推荐结果数量: {len(invalid_camp_teams)}")
    
    # 测试不存在的标签推荐
    print("\n=== 推荐包含不存在标签的队伍 ===")
    invalid_tag_teams = recommender.recommend_teams_by_tag("不存在的标签", count=5)
    print(f"不存在标签的推荐结果数量: {len(invalid_tag_teams)}")
    
    # 测试指定必须包含的武将
    print("\n=== 推荐必须包含曹操的队伍 ===")
    teams_with_cao_cao = recommender.recommend_teams(count=5, required_hero="曹操")
    for i, team in enumerate(teams_with_cao_cao, 1):
        print(f"{i}. 队伍: {team['队伍']}, 评分: {team['评分']}")
    
    # 测试排除某些武将
    print("\n=== 推荐排除曹操的队伍 ===")
    teams_without_cao_cao = recommender.recommend_teams(count=5, excluded_heroes=["曹操"])
    for i, team in enumerate(teams_without_cao_cao, 1):
        print(f"{i}. 队伍: {team['队伍']}, 评分: {team['评分']}")
    
    # 测试过滤功能
    print("\n=== 测试队伍过滤功能 ===")
    all_teams = recommender.recommend_teams(count=20)
    filtered_teams = recommender.filter_teams_by_criteria(all_teams, min_score=50.0)
    print(f"总推荐队伍数: {len(all_teams)}, 过滤后队伍数: {len(filtered_teams)}")
    
    # 测试必须包含的武将过滤
    filtered_teams = recommender.filter_teams_by_criteria(all_teams, required_heroes=["曹操"])
    print(f"必须包含曹操的队伍数: {len(filtered_teams)}")
    
    # 测试排除武将的过滤
    filtered_teams = recommender.filter_teams_by_criteria(all_teams, excluded_heroes=["曹操"])
    print(f"排除曹操的队伍数: {len(filtered_teams)}")

if __name__ == "__main__":
    test_recommender()