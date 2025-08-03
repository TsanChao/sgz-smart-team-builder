#!/usr/bin/env python3
# 测试数据管理器

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data_manager import DataManager

def test_data_manager():
    """测试数据管理器"""
    # 创建数据管理器实例
    data_manager = DataManager("data/consolidated_ocr_data.json")
    
    # 测试获取所有武将
    heroes = data_manager.get_heroes()
    print(f"总共加载了 {len(heroes)} 个武将")
    
    # 测试获取所有战法
    skills = data_manager.get_skills()
    print(f"总共加载了 {len(skills)} 个战法")
    
    # 测试获取特定武将
    hero = data_manager.get_hero_by_name("曹操")
    if hero:
        print(f"曹操的信息: {hero}")
    else:
        print("未找到曹操的信息")
    
    # 测试获取不存在的武将
    hero = data_manager.get_hero_by_name("不存在的武将")
    if hero is None:
        print("正确处理了不存在的武将查询")
    else:
        print("错误：应该返回None")
    
    # 测试获取特定战法
    skill = data_manager.get_skill_by_name("挟天子以令诸侯")
    if skill:
        print(f"挟天子以令诸侯的信息: {skill}")
    else:
        print("未找到挟天子以令诸侯的信息")
    
    # 测试获取不存在的战法
    skill = data_manager.get_skill_by_name("不存在的战法")
    if skill is None:
        print("正确处理了不存在的战法查询")
    else:
        print("错误：应该返回None")
    
    # 测试获取武将属性
    force_attr = data_manager.get_hero_attribute("曹操", "武力")
    print(f"曹操的武力属性: {force_attr}")
    
    # 测试获取不存在武将的属性
    force_attr = data_manager.get_hero_attribute("不存在的武将", "武力")
    if not force_attr:
        print("正确处理了不存在武将的属性查询")
    
    # 测试获取武将兵种适性
    cavalry_fit = data_manager.get_hero_troop_fitness("曹操", "骑兵")
    print(f"曹操的骑兵适性: {cavalry_fit}")
    
    # 测试获取不存在武将的兵种适性
    cavalry_fit = data_manager.get_hero_troop_fitness("不存在的武将", "骑兵")
    if cavalry_fit == "":
        print("正确处理了不存在武将的兵种适性查询")
    
    # 测试搜索功能
    search_results = data_manager.search_heroes("魏")
    print(f"搜索包含'魏'的武将，找到 {len(search_results)} 个")
    
    search_results = data_manager.search_skills("主动")
    print(f"搜索包含'主动'的战法，找到 {len(search_results)} 个")
    
    # 测试空关键字搜索
    search_results = data_manager.search_heroes("")
    print(f"空关键字搜索武将，找到 {len(search_results)} 个")
    
    search_results = data_manager.search_skills("")
    print(f"空关键字搜索战法，找到 {len(search_results)} 个")
    
    # 测试获取所有武将名称
    hero_names = data_manager.get_all_hero_names()
    print(f"所有武将名称数量: {len(hero_names)}")
    
    # 测试获取所有战法名称
    skill_names = data_manager.get_all_skill_names()
    print(f"所有战法名称数量: {len(skill_names)}")

if __name__ == "__main__":
    test_data_manager()