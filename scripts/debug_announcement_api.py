#!/usr/bin/env python3
# 调试公告API

import requests
import json

def debug_announcement_api():
    """调试公告API"""
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
    
    print("=== 请求参数 ===")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        print(f"\n=== 响应状态 ===")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n=== 响应数据 ===")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("请求失败")
            print(response.text)
    except Exception as e:
        print(f"请求出错: {e}")

if __name__ == "__main__":
    debug_announcement_api()
