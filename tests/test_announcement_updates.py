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
    
    print("=== 测试获取多页公告列表 ===")
    # 获取多页公告列表
    all_announcements = data_manager.get_multiple_announcement_pages(max_pages=3, size=20)
    print(f"成功获取 {len(all_announcements)} 页公告")
    
    if all_announcements:
        # 计算总公告数
        total_announcements = 0
        for page_announcements in all_announcements:
            total_announcements += len(page_announcements.get('data', {}).get('list', []))
        print(f"总共获取到 {total_announcements} 条公告")
        
        # 筛选维护更新公告
        maintenance_announcements = data_manager.filter_maintenance_announcements(all_announcements)
        print(f"筛选出 {len(maintenance_announcements)} 条维护更新公告")
        
        if maintenance_announcements:
            # 显示最新的几条维护更新公告
            print("\n最新的维护更新公告:")
            for i, announcement in enumerate(maintenance_announcements[:3]):
                print(f"{i+1}. {announcement.get('title')} (ID: {announcement.get('id')})")
            
            # 获取第一条公告的详情
            print("\n=== 测试获取公告详情 ===")
            first_announcement = maintenance_announcements[0]
            detail = data_manager.get_announcement_detail(first_announcement.get('id'))
            if detail:
                title = detail.get('data', {}).get('infoDetail', {}).get('title', '')
                print(f"成功获取公告详情: {title}")
                
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
    has_updates = data_manager.check_for_updates(max_pages=3)
    print(f"是否有新的更新: {has_updates}")

if __name__ == "__main__":
    test_announcement_features()