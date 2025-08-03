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
    
    def get_announcement_list(self, page: int = 0, size: int = 20) -> Optional[Dict[str, Any]]:
        """
        获取游戏公告列表
        
        Args:
            page: 页码（从0开始）
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
    
    def get_all_announcements(self, size: int = 20) -> List[Dict[str, Any]]:
        """
        获取所有公告列表（不限制页数）
        
        Args:
            size: 每页数量
            
        Returns:
            所有公告列表数据
        """
        all_announcements = []
        page = 0  # 从第0页开始
        
        # 先获取第一页，获取总数
        print(f"正在获取第 {page} 页公告...")
        first_page = self.get_announcement_list(page=page, size=size)
        if not first_page:
            print(f"获取第 {page} 页公告失败，停止获取")
            return []
        
        # 解析第一页数据
        result = first_page.get("result", {})
        total = result.get("totalCount", 0)
        items = result.get("list", [])
        
        all_announcements.append(first_page)
        print(f"第{page}页获取到 {len(items)} 条公告")
        
        # 计算总页数
        total_pages = (total + size - 1) // size if total > 0 else 1
        print(f"总共有 {total} 条公告, {total_pages} 页")
        
        # 获取后续页面
        for page in range(1, min(total_pages, 100)):  # 限制最多获取100页
            print(f"正在获取第 {page} 页公告...")
            page_data = self.get_announcement_list(page=page, size=size)
            if page_data:
                all_announcements.append(page_data)
                result = page_data.get("result", {})
                items = result.get("list", [])
                print(f"第{page}页获取到 {len(items)} 条公告")
            else:
                print(f"获取第 {page} 页公告失败，停止获取")
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
        从所有公告中筛选维护更新公告
        
        Args:
            announcements: 所有公告列表数据
            
        Returns:
            维护更新公告列表
        """
        maintenance_announcements = []
        for page_announcements in announcements:
            # 根据API的正确格式解析数据
            result = page_announcements.get("result", {})
            items = result.get("list", [])
            
            for item in items:
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
        
        # 如果内容为空，直接返回空的更新信息
        if not content:
            return updates
        
        # 清理HTML标签
        clean_content = re.sub(r'<[^>]+>', '', content)
        
        # 匹配新增武将
        new_hero_sections = re.findall(r"新增武将[：:]\s*([^\n]+)", clean_content)
        for section in new_hero_sections:
            # 分割并清理武将名
            heroes = [hero.strip() for hero in re.split(r"[、,、]", section) if hero.strip()]
            for hero in heroes:
                # 进一步清理武将名
                hero = re.sub(r"[，。\n\r]", "", hero).strip()
                if hero:
                    updates["new_heroes"].append({
                        "name": hero,
                        "details": {}
                    })
        
        # 匹配新增战法
        new_skill_sections = re.findall(r"新增战法[：:]\s*([^\n]+)", clean_content)
        for section in new_skill_sections:
            # 分割并清理战法名
            skills = [skill.strip() for skill in re.split(r"[、,、]", section) if skill.strip()]
            for skill in skills:
                # 进一步清理战法名
                skill = re.sub(r"[，。\n\r]", "", skill).strip()
                if skill:
                    updates["new_skills"].append({
                        "name": skill,
                        "details": {}
                    })
        
        # 匹配武将调整 - 更智能的匹配
        # 寻找包含"属性"或"成长"或适性调整的段落
        lines = clean_content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # 如果这一行包含武将名特征（通常以人名开头）并且下一行包含属性信息
            if re.search(r'^[\u4e00-\u9fff]{2,5}[：:]', line) and i + 1 < len(lines):
                hero_match = re.search(r'^([\u4e00-\u9fff]{2,5})[：:]', line)
                if hero_match:
                    hero_name = hero_match.group(1)
                    # 确保这个是武将而不是场景名
                    if hero_name not in ["长安之乱", "龙争虎斗"]:
                        # 收集接下来几行的属性信息
                        details = line + "\n"
                        j = i + 1
                        while j < len(lines) and not re.search(r'^[\u4e00-\u9fff]{2,5}[：:]|^新增|===|---', lines[j].strip()):
                            if lines[j].strip():
                                details += lines[j] + "\n"
                            j += 1
                        
                        # 检查details中是否包含属性调整关键词
                        if any(keyword in details for keyword in ["属性", "成长", "适性", "兵力"]):
                            updates["hero_updates"].append({
                                "name": hero_name,
                                "details": details.strip()
                            })
                        i = j  # 跳过已处理的行
                        continue
            i += 1
        
        # 匹配战法调整
        skill_update_sections = re.findall(r"([^\n]*)战法[^\n]*?(?:调整|优化|改动)[^\n]*", clean_content)
        for section in skill_update_sections:
            # 提取战法名
            skill_match = re.search(r'^([^\n：:]+?)[：:]', section)
            if skill_match:
                skill_name = skill_match.group(1).strip()
                # 确保这个是战法而不是场景名
                if skill_name not in ["长安之乱", "龙争虎斗"]:
                    updates["skill_updates"].append({
                        "name": skill_name,
                        "details": section.strip()
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
            # 获取公告内容和标题 - 处理不同的API响应格式
            content = ""
            title = ""
            
            # 尝试第一种格式 (infoDetail)
            result = announcement_detail.get("result", {})
            data = result.get("data", {})
            info_detail = data.get("infoDetail", {})
            content = info_detail.get("content", "")
            title = info_detail.get("title", "")
            
            # 如果content为空，尝试第二种格式 (直接在result中)
            if not content:
                content = result.get("content", "")
                title = result.get("title", "")
            
            # 如果content为空，尝试其他可能的字段
            if not content:
                content = info_detail.get("textContent", "")
            if not content:
                content = info_detail.get("htmlContent", "")
            
            print(f"处理公告: {title}")
            print(f"内容长度: {len(content) if content else 0}")
            
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
            if updates['new_heroes']:
                for hero in updates['new_heroes']:
                    print(f"  - {hero['name']}")
                    
            print(f"检测到 {len(updates['hero_updates'])} 个武将更新")
            if updates['hero_updates']:
                for hero in updates['hero_updates']:
                    print(f"  - {hero['name']}: {hero['details'][:100]}...")
                    
            print(f"检测到 {len(updates['new_skills'])} 个新增战法")
            if updates['new_skills']:
                for skill in updates['new_skills']:
                    print(f"  - {skill['name']}")
                    
            print(f"检测到 {len(updates['skill_updates'])} 个战法更新")
            if updates['skill_updates']:
                for skill in updates['skill_updates']:
                    print(f"  - {skill['name']}: {skill['details'][:100]}...")
            
            # 注意：这里我们仅记录更新信息，实际的数据更新需要手动完成
            # 因为我们没有完整的武将/战法数据结构定义
            print("请手动更新数据文件以应用这些变更")
            
            return True
        except Exception as e:
            print(f"更新本地数据时出错: {e}")
            import traceback
            traceback.print_exc()
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
    
    def check_for_updates(self) -> bool:
        """
        检查是否有新的维护更新公告
        
        Returns:
            是否有新的更新
        """
        # 获取所有公告列表
        print("正在获取所有公告...")
        all_announcements = self.get_all_announcements(size=20)
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
        
        # 加载已处理的公告ID列表
        processed_ids = self._load_processed_announcement_ids()
        
        # 检查每条公告是否已处理过
        for announcement in maintenance_announcements:
            announcement_id = announcement.get("id")
            announcement_title = announcement.get("title")
            announcement_time = announcement.get("publishTime")
            
            print(f"检查公告: {announcement_title} (ID: {announcement_id})")
            
            # 检查是否已处理过此公告
            if str(announcement_id) in processed_ids:
                print("此公告已处理过")
                continue
            
            # 获取公告详情
            print("获取公告详情...")
            detail = self.get_announcement_detail(announcement_id)
            if detail:
                # 处理更新公告
                success = self.update_local_data_with_announcement(detail)
                if success:
                    # 标记公告为已处理
                    self._mark_announcement_as_processed(announcement_id, announcement_title, announcement_time)
                    return True
            else:
                print("获取公告详情失败")
        
        print("没有新的未处理公告")
        return False
    
    def _load_processed_announcement_ids(self) -> set:
        """
        加载已处理的公告ID列表
        
        Returns:
            已处理的公告ID集合
        """
        checkpoint_file = "processed_announcements.json"
        if os.path.exists(checkpoint_file):
            try:
                with open(checkpoint_file, 'r', encoding='utf-8') as f:
                    checkpoints = json.load(f)
                return set(str(cp.get("id")) for cp in checkpoints)
            except Exception as e:
                print(f"读取检查点文件时出错: {e}")
        return set()
    
    def _mark_announcement_as_processed(self, announcement_id: str, title: str, publish_time: str) -> None:
        """
        标记公告为已处理
        
        Args:
            announcement_id: 公告ID
            title: 公告标题
            publish_time: 发布时间
        """
        # 加载现有检查点
        checkpoint_file = "processed_announcements.json"
        checkpoints = []
        if os.path.exists(checkpoint_file):
            try:
                with open(checkpoint_file, 'r', encoding='utf-8') as f:
                    checkpoints = json.load(f)
            except Exception as e:
                print(f"读取检查点文件时出错: {e}")
        
        # 添加新检查点
        new_checkpoint = {
            "id": announcement_id,
            "title": title,
            "publish_time": publish_time,
            "processed_time": datetime.now().isoformat()
        }
        checkpoints.append(new_checkpoint)
        
        # 保存检查点
        try:
            with open(checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(checkpoints, f, ensure_ascii=False, indent=2)
            print(f"已标记公告 {announcement_id} 为已处理")
        except Exception as e:
            print(f"保存检查点文件时出错: {e}")