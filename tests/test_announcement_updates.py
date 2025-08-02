#!/usr/bin/env python3
# 测试数据管理器的公告更新功能

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
        print(f"成功获取到 {len(announcements.get('data', {}).get('list', []))} 条公告")
        
        # 筛选维护更新公告
        maintenance_announcements = data_manager.filter_maintenance_announcements(announcements)
        print(f"筛选出 {len(maintenance_announcements)} 条维护更新公告")
        
        if maintenance_announcements:
            # 显示最新的维护更新公告
            latest = maintenance_announcements[0]
            print(f"最新的维护更新公告: {latest.get('title')} (ID: {latest.get('id')})")
            
            # 获取公告详情
            print("\n=== 测试获取公告详情 ===")
            detail = data_manager.get_announcement_detail(latest.get('id'))
            if detail:
                print(f"成功获取公告详情: {detail.get('data', {}).get('infoDetail', {}).get('title', '')}")
                
                # 测试解析更新内容
                content = detail.get('data', {}).get('infoDetail', {}).get('content', '')
                if content:
                    print("\n=== 测试解析更新内容 ===")
                    updates = data_manager.parse_update_content(content)
                    print(f"新增武将: {len(updates['new_heroes'])}")
                    print(f"武将更新: {len(updates['hero_updates'])}")
                    print(f"新增战法: {len(updates['new_skills'])}")
                    print(f"战法更新: {len(updates['skill_updates'])}")
                    
                    # 显示部分解析结果
                    if updates['new_heroes']:
                        print(f"示例新增武将: {updates['new_heroes'][0]['name']}")
                    if updates['hero_updates']:
                        print(f"示例武将更新: {updates['hero_updates'][0]['name']}")
                    if updates['new_skills']:
                        print(f"示例新增战法: {updates['new_skills'][0]['name']}")
                    if updates['skill_updates']:
                        print(f"示例战法更新: {updates['skill_updates'][0]['name']}")
            else:
                print("获取公告详情失败")
        else:
            print("未找到维护更新公告")
    else:
        print("获取公告列表失败")
    
    print("\n=== 测试检查更新 ===")
    # 测试检查更新功能
    has_updates = data_manager.check_for_updates()
    print(f"是否有新的更新: {has_updates}")

if __name__ == "__main__":
    test_announcement_features()