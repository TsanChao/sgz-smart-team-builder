#!/usr/bin/env python3
# 调试公告API返回格式

import requests
import json

# API URL和参数
api_url = "https://galaxias-api.lingxigames.com/ds/ajax/endpoint.json"

# 测试获取公告列表
payload = {
    "api": "/api/l/owresource/getListRecommend",
    "params": {
        "gameId": 10000100,
        "collectionIds": 128,
        "orderCode": 1,
        "orderDesc": True,
        "page": 1,
        "size": 20
    }
}

try:
    response = requests.post(api_url, json=payload, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print("API响应格式:")
        print(json.dumps(data, ensure_ascii=False, indent=2)[:1000] + "...")
        
        # 获取数据结构的详细信息
        result = data.get("result", {})
        print(f"\nResult对象结构:")
        print(f"  totalCount: {result.get('totalCount')}")
        print(f"  list length: {len(result.get('list', []))}")
        if result.get("list"):
            item = result["list"][0]
            print(f"  list item keys: {list(item.keys())}")
            print(f"  示例公告 - ID: {item.get('id')}, 标题: {item.get('title')}")
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(response.text[:200])
except Exception as e:
    print(f"请求出错: {e}")