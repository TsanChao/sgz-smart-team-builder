#!/usr/bin/env python3
# 测试API接口

import requests
import json
import time

BASE_URL = "http://localhost:5001/api"

def test_health_check():
    """测试健康检查接口"""
    print("=== 测试健康检查接口 ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"测试健康检查接口时出错: {e}")

def test_get_heroes():
    """测试获取所有武将接口"""
    print("\n=== 测试获取所有武将接口 ===")
    try:
        response = requests.get(f"{BASE_URL}/heroes")
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"武将总数: {data.get('count', 0)}")
        print(f"前3个武将: {list(data.get('heroes', {}).keys())[:3]}")
    except Exception as e:
        print(f"测试获取所有武将接口时出错: {e}")

def test_get_hero():
    """测试获取指定武将接口"""
    print("\n=== 测试获取指定武将接口 ===")
    try:
        hero_name = "曹操"
        response = requests.get(f"{BASE_URL}/heroes/{hero_name}")
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"武将信息: {data}")
    except Exception as e:
        print(f"测试获取指定武将接口时出错: {e}")

def test_get_skills():
    """测试获取所有战法接口"""
    print("\n=== 测试获取所有战法接口 ===")
    try:
        response = requests.get(f"{BASE_URL}/skills")
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"战法总数: {data.get('count', 0)}")
        print(f"前3个战法: {list(data.get('skills', {}).keys())[:3]}")
    except Exception as e:
        print(f"测试获取所有战法接口时出错: {e}")

def test_recommend_teams():
    """测试队伍推荐接口"""
    print("\n=== 测试队伍推荐接口 ===")
    try:
        payload = {
            "count": 5,
            "required_hero": "曹操"
        }
        response = requests.post(f"{BASE_URL}/recommend", json=payload)
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"推荐队伍数量: {data.get('count', 0)}")
        for i, team in enumerate(data.get('teams', [])[:3], 1):
            print(f"  {i}. {team['队伍']} - 评分: {team['评分']}")
    except Exception as e:
        print(f"测试队伍推荐接口时出错: {e}")

def test_analyze_synergy():
    """测试协同分析接口"""
    print("\n=== 测试协同分析接口 ===")
    try:
        payload = {
            "heroes": ["曹操", "夏侯惇", "荀彧"]
        }
        response = requests.post(f"{BASE_URL}/synergy", json=payload)
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"队伍: {data.get('team', [])}")
        print(f"协同评分: {data.get('synergy_score', 0)}")
    except Exception as e:
        print(f"测试协同分析接口时出错: {e}")

def run_all_tests():
    """运行所有API测试"""
    print("请确保API服务正在运行 (python app.py)")
    print("等待2秒...")
    time.sleep(2)
    
    # 运行所有测试
    test_health_check()
    test_get_heroes()
    test_get_hero()
    test_get_skills()
    test_recommend_teams()
    test_analyze_synergy()
    print("\n=== 所有API测试完成 ===")

if __name__ == "__main__":
    run_all_tests()