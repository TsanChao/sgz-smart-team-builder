#!/usr/bin/env python3
# 测试公告更新功能

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data_manager import DataManager

def test_announcement_features():
    """测试公告相关功能"""
    # 创建数据管理器实例
    data_manager = DataManager("data/consolidated_ocr_data.json")
    
    print("=== 测试获取公告列表 ===")
    # 获取公告列表
    announcements = data_manager.get_announcement_list(page=1, size=10)
    if announcements:
        result = announcements.get("result", {})
        items = result.get("list", [])
        print(f"成功获取到 {len(items)} 条公告")
        
        # 筛选维护更新公告
        maintenance_announcements = data_manager.filter_maintenance_announcements([announcements])
        print(f"筛选出 {len(maintenance_announcements)} 条维护更新公告")
        
        if maintenance_announcements:
            # 显示最新的维护更新公告
            latest = maintenance_announcements[0]
            print(f"最新的维护更新公告: {latest.get('title')} (ID: {latest.get('id')})")
        else:
            print("未找到维护更新公告")
    else:
        print("获取公告列表失败")

if __name__ == "__main__":
    test_announcement_features()