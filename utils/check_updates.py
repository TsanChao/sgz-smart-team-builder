#!/usr/bin/env python3
# 公告更新检查工具

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data_manager import DataManager

def check_for_updates():
    """检查并处理最新的维护更新公告"""
    # 创建数据管理器实例
    data_manager = DataManager("data/consolidated_ocr_data.json")
    
    # 检查更新
    has_updates = data_manager.check_for_updates()
    
    if has_updates:
        print("检测到新的维护更新公告，并已处理")
        return 0
    else:
        print("没有检测到新的维护更新公告，或者公告已处理过")
        return 1

if __name__ == "__main__":
    exit_code = check_for_updates()
    sys.exit(exit_code)