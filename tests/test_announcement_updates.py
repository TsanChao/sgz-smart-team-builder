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
    announcements = data_manager.get_announcement_list(page=0, size=5)
    if announcements:
        result = announcements.get("result", {})
        items = result.get("list", [])
        print(f"成功获取到 {len(items)} 条公告")
        
        if items:
            # 测试筛选维护更新公告
            maintenance_announcements = data_manager.filter_maintenance_announcements([announcements])
            print(f"筛选出 {len(maintenance_announcements)} 条维护更新公告")
            
            if maintenance_announcements:
                # 显示最新的维护更新公告
                latest = maintenance_announcements[0]
                print(f"最新的维护更新公告: {latest.get('title')} (ID: {latest.get('id')})")
                
                # 测试获取公告详情
                print("\n=== 测试获取公告详情 ===")
                detail = data_manager.get_announcement_detail(latest.get('id'))
                if detail:
                    result = detail.get("result", {})
                    content = result.get("content", "")
                    title = result.get("title", "")
                    print(f"公告标题: {title}")
                    print(f"内容长度: {len(content) if content else 0}")
                    
                    # 测试解析更新内容
                    if content:
                        print("\n=== 测试解析更新内容 ===")
                        updates = data_manager.parse_update_content(content)
                        print(f"新增武将: {len(updates['new_heroes'])}")
                        print(f"武将更新: {len(updates['hero_updates'])}")
                        print(f"新增战法: {len(updates['new_skills'])}")
                        print(f"战法更新: {len(updates['skill_updates'])}")
                else:
                    print("获取公告详情失败")
            else:
                print("未找到维护更新公告")
        else:
            print("未获取到公告")
    else:
        print("获取公告列表失败")
    
    # 测试获取所有公告
    print("\n=== 测试获取所有公告 ===")
    all_announcements = data_manager.get_all_announcements(size=5)
    print(f"总共获取到 {len(all_announcements)} 页公告")
    
    # 测试筛选维护更新公告（空列表）
    print("\n=== 测试筛选维护更新公告（空列表） ===")
    empty_maintenance = data_manager.filter_maintenance_announcements([])
    print(f"空列表筛选结果: {len(empty_maintenance)}")
    
    # 测试解析空内容
    print("\n=== 测试解析空内容 ===")
    empty_updates = data_manager.parse_update_content("")
    print(f"空内容解析结果 - 新增武将: {len(empty_updates['new_heroes'])}, 武将更新: {len(empty_updates['hero_updates'])}")
    
    # 测试检查更新功能
    print("\n=== 测试检查更新功能 ===")
    try:
        has_updates = data_manager.check_for_updates()
        print(f"检查更新结果: {has_updates}")
    except Exception as e:
        print(f"检查更新时出错: {e}")
    
    # 测试获取不存在的公告详情
    print("\n=== 测试获取不存在的公告详情 ===")
    non_existent_detail = data_manager.get_announcement_detail("不存在的ID")
    if non_existent_detail is None:
        print("正确处理了不存在的公告详情查询")

if __name__ == "__main__":
    test_announcement_features()