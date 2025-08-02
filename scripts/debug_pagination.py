#!/usr/bin/env python3
# 调试公告获取功能

import requests
import json

# API URL和参数
api_url = "https://galaxias-api.lingxigames.com/ds/ajax/endpoint.json"

def get_page_of_announcements(page: int, size: int = 20):
    """获取公告列表的一页"""
    payload = {
        "api": "/api/l/owresource/getListRecommend",
        "params": {
            "gameId": 10000100,
            "collectionIds": 128,
            "orderCode": 1,
            "orderDesc": True,
            "page": page,
            "size": size
        }
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"请求出错: {e}")
        return None

def test_announcement_pagination():
    """测试公告分页功能"""
    print("=== 测试公告分页功能 ===")
    
    # 获取第一页
    page_1 = get_page_of_announcements(1, 20)
    if not page_1:
        print("无法获取第一页公告")
        return
    
    print(f"第一页响应: {json.dumps(page_1, ensure_ascii=False, indent=2)[:200]}...")
    
    # 获取总数量
    data = page_1.get("data", {})
    total = data.get("total", 0)
    items = data.get("list", [])
    
    print(f"总公告数: {total}")
    print(f"第一页有 {len(items)} 条公告")
    
    # 计算总页数
    pages = (total + 20 - 1) // 20  # 向上取整
    print(f"总共 {pages} 页")
    
    # 测试获取第二页
    print("\n=== 测试获取第二页 ===")
    page_2 = get_page_of_announcements(2, 20)
    if page_2:
        data = page_2.get("data", {})
        items = data.get("list", [])
        print(f"第二页有 {len(items)} 条公告")
        if items:
            print(f"第二页第一条公告标题: {items[0].get('title', '')}")

if __name__ == "__main__":
    test_announcement_pagination()
