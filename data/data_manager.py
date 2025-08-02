# 数据管理器
import json
import os
import requests
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

class DataManager:
    def __init__(self, data_file_path: str):
        self.data_file_path = data_file_path
        self.data = self._load_data()
        self.announcement_api_url = "https://galaxias-api.lingxigames.com/ds/ajax/endpoint.json"
    
    def _load_data(self) -> Dict[str, Any]:
        """加载游戏数据"""
        try:
            # 检查文件是否存在
            if not os.path.exists(self.data_file_path):
                # 如果文件不存在，尝试在项目根目录查找
                root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                data_file_path = os.path.join(root_dir, "data", "consolidated_ocr_data.json")
                if not os.path.exists(data_file_path):
                    raise FileNotFoundError(f"数据文件未找到: {self.data_file_path} 或 {data_file_path}")
                self.data_file_path = data_file_path
            
            # 读取JSON数据
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"加载数据文件时出错: {e}")
            return {}
    
    def _save_data(self) -> None:
        """保存游戏数据到文件"""
        try:
            with open(self.data_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print("数据已成功保存到文件")
        except Exception as e:
            print(f"保存数据文件时出错: {e}")
    
    def get_heroes(self) -> Dict[str, Any]:
        """获取所有武将"""
        return self.data.get('武将', {})
    
    def get_skills(self) -> Dict[str, Any]:
        """获取所有战法"""
        return self.data.get('战法', {})
    
    def get_hero_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """根据名称获取武将信息"""
        return self.data.get('武将', {}).get(name)
    
    def get_skill_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """根据名称获取战法信息"""
        return self.data.get('战法', {}).get(name)
    
    def get_all_hero_names(self) -> List[str]:
        """获取所有武将名称列表"""
        return list(self.data.get('武将', {}).keys())
    
    def get_all_skill_names(self) -> List[str]:
        """获取所有战法名称列表"""
        return list(self.data.get('战法', {}).keys())
    
    def get_hero_attribute(self, hero_name: str, attribute: str) -> Dict[str, float]:
        """获取武将指定属性值"""
        hero = self.get_hero_by_name(hero_name)
        if hero and '属性' in hero:
            return hero['属性'].get(attribute, {})
        return {}
    
    def get_hero_troop_fitness(self, hero_name: str, troop_type: str) -> str:
        """获取武将指定兵种适性"""
        hero = self.get_hero_by_name(hero_name)
        if hero and '兵种' in hero:
            return hero['兵种'].get(troop_type, '')
        return ''
    
    def search_heroes(self, keyword: str) -> Dict[str, Any]:
        """根据关键字搜索武将"""
        heroes = self.get_heroes()
        result = {}
        for name, info in heroes.items():
            if keyword.lower() in name.lower() or keyword.lower() in str(info).lower():
                result[name] = info
        return result
    
    def search_skills(self, keyword: str) -> Dict[str, Any]:
        """根据关键字搜索战法"""
        skills = self.get_skills()
        result = {}
        for name, info in skills.items():
            if keyword.lower() in name.lower() or keyword.lower() in str(info).lower():
                result[name] = info
        return result
    
    def get_announcement_list(self, page: int = 1, size: int = 20) -> Optional[Dict[str, Any]]:
        """
        获取游戏公告列表
        
        Args:
            page: 页码
            size: 每页数量
            
        Returns:
            公告列表数据或None
        """
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
            response = requests.post(self.announcement_api_url, json=payload, timeout=10)
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
    
    def get_multiple_announcement_pages(self, max_pages: int = 5, size: int = 20) -> List[Dict[str, Any]]:
        """
        获取多页公告列表
        
        Args:
            max_pages: 最大页数
            size: 每页数量
            
        Returns:
            公告列表数据列表
        """
        all_announcements = []
        for page in range(1, max_pages + 1):
            print(f"获取第 {page} 页公告...")
            announcements = self.get_announcement_list(page=page, size=size)
            if announcements:
                all_announcements.append(announcements)
                # 检查是否还有更多页面
                data = announcements.get("data", {})
                total = data.get("total", 0)
                current_size = len(data.get("list", []))
                if page * size >= total or current_size < size:
                    # 已经获取了所有公告
                    break
            else:
                # 获取失败，停止获取
                print(f"获取第 {page} 页公告失败，停止获取更多页面")
                break
        return all_announcements
    
    def get_announcement_detail(self, announcement_id: str) -> Optional[Dict[str, Any]]:
        """
        获取公告详情
        
        Args:
            announcement_id: 公告ID
            
        Returns:
            公告详情数据或None
        """
        payload = {
            "api": "/api/l/owresource/getInfoDetail",
            "params": {
                "gameId": 10000100,
                "id": str(announcement_id)
            }
        }
        
        try:
            response = requests.post(self.announcement_api_url, json=payload, timeout=10)
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
    
    def filter_maintenance_announcements(self, announcements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        从多页公告中筛选维护更新公告
        
        Args:
            announcements: 多页公告列表数据
            
        Returns:
            维护更新公告列表
        """
        maintenance_announcements = []
        for page_announcements in announcements:
            for item in page_announcements.get("data", {}).get("list", []):
                title = item.get("title", "")
                if "维护更新公告" in title:
                    maintenance_announcements.append(item)
        return maintenance_announcements
    
    def parse_update_content(self, content: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        解析更新公告内容，提取更新信息
        
        Args:
            content: 公告内容文本
            
        Returns:
            解析后的更新信息
        """
        updates = {
            "new_heroes": [],
            "hero_updates": [],
            "new_skills": [],
            "skill_updates": []
        }
        
        # 匹配新增武将
        new_hero_pattern = r"新增武将：([^，。]+)"
        new_hero_matches = re.findall(new_hero_pattern, content)
        for match in new_hero_matches:
            heroes = [hero.strip() for hero in match.split("、") if hero.strip()]
            for hero in heroes:
                updates["new_heroes"].append({
                    "name": hero,
                    "details": {}
                })
        
        # 匹配武将属性调整
        hero_attr_pattern = r"([^，。]+)：([\s\S]*?)(?=(?:\n\n)|$)"
        hero_attr_updates = re.findall(hero_attr_pattern, content)
        for hero_name, update_details in hero_attr_updates:
            if ("属性" in update_details or "成长" in update_details) and "武将" not in hero_name:
                updates["hero_updates"].append({
                    "name": hero_name,
                    "details": update_details
                })
        
        # 匹配新增战法
        new_skill_pattern = r"新增战法：([^，。]+)"
        new_skill_matches = re.findall(new_skill_pattern, content)
        for match in new_skill_matches:
            skills = [skill.strip() for skill in match.split("、") if skill.strip()]
            for skill in skills:
                updates["new_skills"].append({
                    "name": skill,
                    "details": {}
                })
        
        # 匹配战法调整
        skill_update_pattern = r"([^，。]+)战法(?:效果)?(?:调整|优化)：([\s\S]*?)(?=(?:\n\n)|$)"
        skill_updates_matches = re.findall(skill_update_pattern, content)
        for skill_name, update_details in skill_updates_matches:
            updates["skill_updates"].append({
                "name": skill_name,
                "details": update_details
            })
        
        return updates
    
    def update_local_data_with_announcement(self, announcement_detail: Dict[str, Any]) -> bool:
        """
        根据公告详情更新本地数据
        
        Args:
            announcement_detail: 公告详情数据
            
        Returns:
            更新是否成功
        """
        try:
            # 获取公告内容
            content = announcement_detail.get("data", {}).get("infoDetail", {}).get("content", "")
            title = announcement_detail.get("data", {}).get("infoDetail", {}).get("title", "")
            
            print(f"处理公告: {title}")
            
            # 解析更新内容
            updates = self.parse_update_content(content)
            
            # 记录更新日志
            update_log = {
                "timestamp": datetime.now().isoformat(),
                "announcement_title": title,
                "updates": updates
            }
            
            # 保存更新日志
            self._save_update_log(update_log)
            
            # 显示解析结果
            print(f"检测到 {len(updates['new_heroes'])} 个新增武将")
            print(f"检测到 {len(updates['hero_updates'])} 个武将更新")
            print(f"检测到 {len(updates['new_skills'])} 个新增战法")
            print(f"检测到 {len(updates['skill_updates'])} 个战法更新")
            
            # 注意：这里我们仅记录更新信息，实际的数据更新需要手动完成
            # 因为我们没有完整的武将/战法数据结构定义
            print("请手动更新数据文件以应用这些变更")
            
            return True
        except Exception as e:
            print(f"更新本地数据时出错: {e}")
            return False
    
    def _save_update_log(self, update_log: Dict[str, Any]) -> None:
        """
        保存更新日志
        
        Args:
            update_log: 更新日志数据
        """
        log_file = "update_log.json"
        logs = []
        
        # 读取现有日志
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except Exception as e:
                print(f"读取更新日志时出错: {e}")
        
        # 添加新日志
        logs.append(update_log)
        
        # 保存日志
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存更新日志时出错: {e}")
    
    def check_for_updates(self, max_pages: int = 5) -> bool:
        """
        检查是否有新的维护更新公告
        
        Args:
            max_pages: 检查的最大页数
            
        Returns:
            是否有新的更新
        """
        # 获取多页公告列表
        print(f"正在获取最多 {max_pages} 页的公告...")
        all_announcements = self.get_multiple_announcement_pages(max_pages=max_pages)
        if not all_announcements:
            print("获取公告列表失败")
            return False
            
        # 筛选维护更新公告
        maintenance_announcements = self.filter_maintenance_announcements(all_announcements)
        if not maintenance_announcements:
            print("未找到新的维护更新公告")
            return False
        
        print(f"找到 {len(maintenance_announcements)} 条维护更新公告")
        
        # 按发布时间排序，最新的在前面
        maintenance_announcements.sort(key=lambda x: x.get("publishTime", ""), reverse=True)
        
        # 检查每条公告是否已处理过
        for announcement in maintenance_announcements:
            announcement_id = announcement.get("id")
            announcement_title = announcement.get("title")
            announcement_time = announcement.get("publishTime")
            
            print(f"检查公告: {announcement_title} (ID: {announcement_id})")
            
            # 检查是否已处理过此公告
            if self._is_announcement_processed(announcement_id):
                print("此公告已处理过")
                continue
            
            # 获取公告详情
            print("获取公告详情...")
            detail = self.get_announcement_detail(announcement_id)
            if detail:
                # 标记公告为已处理
                self._mark_announcement_as_processed(announcement_id, announcement_title, announcement_time)
                
                # 处理更新公告
                success = self.update_local_data_with_announcement(detail)
                if success:
                    return True
            else:
                print("获取公告详情失败")
        
        print("没有新的未处理公告")
        return False
    
    def _is_announcement_processed(self, announcement_id: str) -> bool:
        """
        检查公告是否已处理过
        
        Args:
            announcement_id: 公告ID
            
        Returns:
            是否已处理
        """
        checkpoint_file = "last_processed_announcement.json"
        if os.path.exists(checkpoint_file):
            try:
                with open(checkpoint_file, 'r', encoding='utf-8') as f:
                    checkpoint = json.load(f)
                return str(checkpoint.get("last_processed_id")) == str(announcement_id)
            except Exception as e:
                print(f"读取检查点文件时出错: {e}")
        return False
    
    def _mark_announcement_as_processed(self, announcement_id: str, title: str, publish_time: str) -> None:
        """
        标记公告为已处理
        
        Args:
            announcement_id: 公告ID
            title: 公告标题
            publish_time: 发布时间
        """
        checkpoint_data = {
            "last_processed_id": announcement_id,
            "title": title,
            "publish_time": publish_time,
            "processed_time": datetime.now().isoformat()
        }
        
        checkpoint_file = "last_processed_announcement.json"
        try:
            with open(checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存检查点文件时出错: {e}")