#!/usr/bin/env python3
# 处理7月30日更新公告

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data_manager import DataManager

def process_july_30_update():
    """处理7月30日更新公告"""
    # 创建数据管理器实例
    data_manager = DataManager("data/consolidated_ocr_data.json")
    
    print("=== 获取所有公告列表 ===")
    # 获取所有公告
    all_announcements = data_manager.get_all_announcements(size=20)
    print(f"总共获取到 {len(all_announcements)} 页公告")
    
    # 计算总公告数
    total_announcements = 0
    for page_announcements in all_announcements:
        total_announcements += len(page_announcements.get('data', {}).get('list', []))
    print(f"总共包含 {total_announcements} 条公告")
    
    # 筛选维护更新公告
    maintenance_announcements = data_manager.filter_maintenance_announcements(all_announcements)
    print(f"筛选出 {len(maintenance_announcements)} 条维护更新公告")
    
    # 按发布时间排序
    maintenance_announcements.sort(key=lambda x: x.get("publishTime", ""), reverse=True)
    
    # 查找7月30日的更新公告
    july_30_announcement = None
    for announcement in maintenance_announcements:
        title = announcement.get("title", "")
        publish_time = announcement.get("publishTime", "")
        if "7月30日" in title or "2025-07-30" in publish_time:
            july_30_announcement = announcement
            break
    
    if july_30_announcement:
        print(f"\n找到7月30日维护更新公告: {july_30_announcement.get('title')} (ID: {july_30_announcement.get('id')})")
        
        # 获取公告详情
        print("\n=== 获取公告详情 ===")
        detail = data_manager.get_announcement_detail(july_30_announcement.get('id'))
        if detail:
            title = detail.get('data', {}).get('infoDetail', {}).get('title', '')
            print(f"公告标题: {title}")
            
            # 处理更新公告
            print("\n=== 处理更新公告 ===")
            success = data_manager.update_local_data_with_announcement(detail)
            if success:
                # 标记公告为已处理
                announcement_id = july_30_announcement.get('id')
                announcement_title = july_30_announcement.get('title')
                announcement_time = july_30_announcement.get('publishTime')
                data_manager._mark_announcement_as_processed(announcement_id, announcement_title, announcement_time)
                print("\n已成功处理7月30日更新公告并记录消费位点")
            else:
                print("\n处理更新公告失败")
        else:
            print("获取公告详情失败")
    else:
        print("未找到7月30日维护更新公告")
        # 显示最近几条维护更新公告
        print("\n最近的维护更新公告:")
        for i, announcement in enumerate(maintenance_announcements[:5]):
            print(f"{i+1}. {announcement.get('title')} (发布时间: {announcement.get('publishTime')})")

if __name__ == "__main__":
    process_july_30_update()