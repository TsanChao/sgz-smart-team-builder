# 游戏公告监控模块

import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class SGZAnnouncementMonitor:
    def __init__(self, data_file_path: str):
        self.base_url = "https://galaxias-api.lingxigames.com/ds/ajax/endpoint.json"
        self.game_id = 10000100
        self.collection_id = 128
        self.checkpoint_file = "last_processed_announcement.json"
        self.data_file_path = data_file_path
        self.data = self._load_game_data()
        
    def _load_game_data(self) -> Dict[str, Any]:
        """加载游戏数据"""
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"数据文件 {self.data_file_path} 未找到")
            return {}
        except Exception as e:
            print(f"加载数据文件时出错: {e}")
            return {}
    
    def _save_game_data(self):
        """保存游戏数据"""
        try:
            with open(self.data_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据文件时出错: {e}")
    
    def get_announcement_list(self, page=0, size=20):
        """获取公告列表，从第0页开始"""
        payload = {
            "api": "/api/l/owresource/getListRecommend",
            "params": {
                "gameId": self.game_id,
                "collectionIds": self.collection_id,
                "orderCode": 1,
                "orderDesc": True,
                "page": page,
                "size": size
            }
        }
        
        try:
            response = requests.post(self.base_url, json=payload, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取公告列表失败，状态码: {response.status_code}")
                return None
        except requests.exceptions.Timeout:
            print("请求超时")
            return None
        except Exception as e:
            print(f"请求公告列表时出错: {e}")
            return None
    
    def get_announcement_detail(self, announcement_id):
        """获取公告详情"""
        payload = {
            "api": "/api/l/owresource/getInfoDetail",
            "params": {
                "gameId": self.game_id,
                "id": str(announcement_id)
            }
        }
        
        try:
            response = requests.post(self.base_url, json=payload, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取公告详情失败，状态码: {response.status_code}")
                return None
        except requests.exceptions.Timeout:
            print("请求超时")
            return None
        except Exception as e:
            print(f"请求公告详情时出错: {e}")
            return None
    
    def filter_maintenance_announcements(self, announcements):
        """筛选维护更新公告"""
        maintenance_announcements = []
        for item in announcements.get("data", {}).get("list", []):
            title = item.get("title", "")
            if "维护更新公告" in title:
                maintenance_announcements.append(item)
        return maintenance_announcements
    
    def load_checkpoint(self):
        """加载检查点"""
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_checkpoint(self, data):
        """保存检查点"""
        with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def check_for_updates(self):
        """检查是否有新的维护更新公告"""
        # 获取最新的公告列表（从第0页开始）
        announcement_list = self.get_announcement_list(page=0)
        if not announcement_list:
            return False
            
        # 筛选维护更新公告
        maintenance_announcements = self.filter_maintenance_announcements(announcement_list)
        if not maintenance_announcements:
            print("未找到新的维护更新公告")
            return False
            
        # 获取最新的维护更新公告
        latest_announcement = maintenance_announcements[0]
        latest_id = latest_announcement.get("id")
        latest_title = latest_announcement.get("title")
        latest_time = latest_announcement.get("publishTime")
        
        print(f"最新的维护更新公告: {latest_title} (ID: {latest_id})")
        
        # 验证7月30日的公告(id=15874)
        if str(latest_id) == "15874":
            print("成功验证7月30日的公告!")
        
        # 加载检查点
        checkpoint = self.load_checkpoint()
        last_processed_id = checkpoint.get("last_processed_id")
        
        # 检查是否是新公告
        if str(latest_id) != str(last_processed_id):
            print("发现新的维护更新公告!")
            # 获取公告详情
            detail = self.get_announcement_detail(latest_id)
            if detail:
                # 保存检查点
                checkpoint_data = {
                    "last_processed_id": latest_id,
                    "title": latest_title,
                    "publish_time": latest_time,
                    "processed_time": datetime.now().isoformat()
                }
                self.save_checkpoint(checkpoint_data)
                
                # 处理更新公告
                self.process_update_announcement(detail)
                return True
        else:
            print("没有新的维护更新公告")
            
        return False
    
    def parse_hero_updates(self, content: str) -> List[Dict[str, Any]]:
        """解析武将更新信息"""
        hero_updates = []
        
        # 匹配新增武将
        new_hero_pattern = r"新增武将：([^，。]+)"
        new_hero_matches = re.findall(new_hero_pattern, content)
        for match in new_hero_matches:
            heroes = [hero.strip() for hero in match.split("、") if hero.strip()]
            for hero in heroes:
                hero_updates.append({
                    "type": "new_hero",
                    "name": hero,
                    "details": {}
                })
        
        # 匹配武将属性调整
        attr_update_pattern = r"([^，。]+)：([\s\S]*?)(?=(?:\n\n)|$)"
        attr_updates = re.findall(attr_update_pattern, content)
        for hero_name, update_details in attr_updates:
            if "属性" in update_details or "成长" in update_details:
                hero_updates.append({
                    "type": "hero_attribute_update",
                    "name": hero_name,
                    "details": update_details
                })
        
        return hero_updates
    
    def parse_skill_updates(self, content: str) -> List[Dict[str, Any]]:
        """解析战法更新信息"""
        skill_updates = []
        
        # 匹配新增战法
        new_skill_pattern = r"新增战法：([^，。]+)"
        new_skill_matches = re.findall(new_skill_pattern, content)
        for match in new_skill_matches:
            skills = [skill.strip() for skill in match.split("、") if skill.strip()]
            for skill in skills:
                skill_updates.append({
                    "type": "new_skill",
                    "name": skill,
                    "details": {}
                })
        
        # 匹配战法调整
        skill_update_pattern = r"([^，。]+)战法(?:效果)?(?:调整|优化)：([\s\S]*?)(?=(?:\n\n)|$)"
        skill_updates_matches = re.findall(skill_update_pattern, content)
        for skill_name, update_details in skill_updates_matches:
            skill_updates.append({
                "type": "skill_update",
                "name": skill_name,
                "details": update_details
            })
        
        return skill_updates
    
    def process_update_announcement(self, announcement_detail):
        """处理更新公告"""
        print("开始处理更新公告...")
        
        # 获取公告内容
        content = announcement_detail.get("data", {}).get("infoDetail", {}).get("content", "")
        title = announcement_detail.get("data", {}).get("infoDetail", {}).get("title", "")
        
        print(f"公告标题: {title}")
        
        # 解析武将更新
        hero_updates = self.parse_hero_updates(content)
        print(f"检测到 {len(hero_updates)} 个武将更新项")
        
        # 解析战法更新
        skill_updates = self.parse_skill_updates(content)
        print(f"检测到 {len(skill_updates)} 个战法更新项")
        
        # 应用更新
        update_log = []
        for hero_update in hero_updates:
            result = self.apply_hero_update(hero_update)
            update_log.append(result)
            
        for skill_update in skill_updates:
            result = self.apply_skill_update(skill_update)
            update_log.append(result)
        
        # 保存更新后的数据
        self._save_game_data()
        
        # 记录更新日志
        self.log_updates(update_log, title)
        
        print("公告处理完成")
    
    def apply_hero_update(self, hero_update: Dict[str, Any]) -> Dict[str, Any]:
        """应用武将更新"""
        update_type = hero_update["type"]
        hero_name = hero_update["name"]
        
        if update_type == "new_hero":
            # 新增武将的处理逻辑
            print(f"新增武将: {hero_name}")
            return {
                "type": "hero_add",
                "name": hero_name,
                "status": "pending",  # 需要手动添加完整数据
                "message": "需要手动添加完整武将数据"
            }
        elif update_type == "hero_attribute_update":
            # 武将属性调整的处理逻辑
            print(f"武将属性调整: {hero_name}")
            return {
                "type": "hero_update",
                "name": hero_name,
                "status": "processed",
                "message": f"已记录{hero_name}的属性调整信息"
            }
        
        return {
            "type": "unknown",
            "name": hero_name,
            "status": "skipped",
            "message": "未知的武将更新类型"
        }
    
    def apply_skill_update(self, skill_update: Dict[str, Any]) -> Dict[str, Any]:
        """应用战法更新"""
        update_type = skill_update["type"]
        skill_name = skill_update["name"]
        
        if update_type == "new_skill":
            # 新增战法的处理逻辑
            print(f"新增战法: {skill_name}")
            return {
                "type": "skill_add",
                "name": skill_name,
                "status": "pending",  # 需要手动添加完整数据
                "message": "需要手动添加完整战法数据"
            }
        elif update_type == "skill_update":
            # 战法调整的处理逻辑
            print(f"战法调整: {skill_name}")
            return {
                "type": "skill_update",
                "name": skill_name,
                "status": "processed",
                "message": f"已记录{skill_name}的调整信息"
            }
        
        return {
            "type": "unknown",
            "name": skill_name,
            "status": "skipped",
            "message": "未知的战法更新类型"
        }
    
    def log_updates(self, update_log: List[Dict[str, Any]], announcement_title: str):
        """记录更新日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "announcement_title": announcement_title,
            "updates": update_log
        }
        
        # 读取现有日志
        log_file = "update_log.json"
        logs = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except Exception as e:
                print(f"读取更新日志时出错: {e}")
        
        # 添加新日志
        logs.append(log_entry)
        
        # 保存日志
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存更新日志时出错: {e}")

# 测试代码
if __name__ == "__main__":
    monitor = SGZAnnouncementMonitor("/Users/zhaocan/Develop/sgz/sgz-smart-team-builder/data/consolidated_ocr_data.json")
    monitor.check_for_updates()