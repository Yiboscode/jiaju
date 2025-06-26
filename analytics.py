from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from datetime import datetime, timedelta
from typing import List, Dict, Any
import pandas as pd
import database
import models



class SmartHomeAnalytics:
    def __init__(self, db: Session):
        self.db = db
    
    def analyze_device_usage_frequency(self) -> List[models.DeviceUsageAnalysis]:
        """分析不同设备的使用频率和使用时间段"""
        # 查询设备使用数据
        query = self.db.query(
            database.Device.device_name,
            database.DeviceType.type_name,
            func.count(database.UsageRecord.record_id).label('usage_frequency'),
            func.sum(database.UsageRecord.duration_minutes).label('total_minutes'),
            func.avg(database.UsageRecord.duration_minutes).label('avg_duration')
        ).join(
            database.UsageRecord, database.Device.device_id == database.UsageRecord.device_id
        ).join(
            database.DeviceType, database.Device.device_type_id == database.DeviceType.type_id
        ).group_by(
            database.Device.device_id, database.Device.device_name, database.DeviceType.type_name
        ).all()
        
        results = []
        for row in query:
            # 计算高峰使用时间
            peak_hours = self._get_peak_usage_hours(row.device_name)
            
            analysis = models.DeviceUsageAnalysis(
                device_name=row.device_name,
                device_type=row.type_name,
                total_usage_hours=round((row.total_minutes or 0) / 60, 2),
                usage_frequency=row.usage_frequency,
                avg_session_duration=round(row.avg_duration or 0, 2),
                peak_usage_hours=peak_hours
            )
            results.append(analysis)
        
        return results
    
    def _get_peak_usage_hours(self, device_name: str) -> List[int]:
        """获取设备的高峰使用时间段"""
        query = self.db.query(
            extract('hour', database.UsageRecord.start_time).label('hour'),
            func.count().label('count')
        ).join(
            database.Device, database.UsageRecord.device_id == database.Device.device_id
        ).filter(
            database.Device.device_name == device_name
        ).group_by(
            extract('hour', database.UsageRecord.start_time)
        ).order_by(
            func.count().desc()
        ).limit(3).all()
        
        return [int(row.hour) for row in query if row.hour is not None]
    
    def analyze_user_habits(self) -> List[models.UserHabitAnalysis]:
        """找出用户的使用习惯（如哪些设备经常同时使用）"""
        users = self.db.query(database.User).all()
        results = []
        
        for user in users:
            # 分析用户的设备使用习惯
            user_records = self.db.query(database.UsageRecord).filter(
                database.UsageRecord.user_id == user.user_id
            ).all()
            
            # 找出经常同时使用的设备
            frequently_used_together = self._find_concurrent_device_usage(user.user_id)
            
            # 找出用户的活跃时间段
            peak_hours = self._get_user_peak_hours(user.user_id)
            
            # 找出用户最常用的设备
            favorite_devices = self._get_user_favorite_devices(user.user_id)
            
            analysis = models.UserHabitAnalysis(
                user_id=user.user_id,
                username=user.username,
                frequently_used_together=frequently_used_together,
                peak_activity_hours=peak_hours,
                favorite_devices=favorite_devices
            )
            results.append(analysis)
        
        return results
    
    def _find_concurrent_device_usage(self, user_id: int) -> List[List[str]]:
        """查找同时使用的设备组合"""
        # 查询用户的使用记录
        records = self.db.query(
            database.UsageRecord.start_time,
            database.UsageRecord.end_time,
            database.Device.device_name
        ).join(
            database.Device, database.UsageRecord.device_id == database.Device.device_id
        ).filter(
            database.UsageRecord.user_id == user_id,
            database.UsageRecord.end_time.isnot(None)
        ).all()
        
        # 找出时间重叠的设备使用记录
        concurrent_pairs = []
        for i, record1 in enumerate(records):
            for record2 in records[i+1:]:
                # 检查时间是否重叠
                if (record1.start_time <= record2.end_time and 
                    record1.end_time >= record2.start_time):
                    pair = sorted([record1.device_name, record2.device_name])
                    concurrent_pairs.append(pair)
        
        # 统计并返回最常见的组合
        from collections import Counter
        pair_counts = Counter(tuple(pair) for pair in concurrent_pairs)
        top_pairs = [list(pair) for pair, count in pair_counts.most_common(5)]
        
        return top_pairs
    
    def _get_user_peak_hours(self, user_id: int) -> List[int]:
        """获取用户的活跃时间段"""
        query = self.db.query(
            extract('hour', database.UsageRecord.start_time).label('hour'),
            func.count().label('count')
        ).filter(
            database.UsageRecord.user_id == user_id
        ).group_by(
            extract('hour', database.UsageRecord.start_time)
        ).order_by(
            func.count().desc()
        ).limit(3).all()
        
        return [int(row.hour) for row in query if row.hour is not None]
    
    def _get_user_favorite_devices(self, user_id: int) -> List[str]:
        """获取用户最常用的设备"""
        query = self.db.query(
            database.Device.device_name,
            func.count(database.UsageRecord.record_id).label('usage_count')
        ).join(
            database.UsageRecord, database.Device.device_id == database.UsageRecord.device_id
        ).filter(
            database.UsageRecord.user_id == user_id
        ).group_by(
            database.Device.device_name
        ).order_by(
            func.count(database.UsageRecord.record_id).desc()
        ).limit(5).all()
        
        return [row.device_name for row in query]
    
    def analyze_house_area_impact(self) -> List[models.HouseAreaAnalysis]:
        """分析房屋面积对设备使用行为的影响"""
        # 定义面积区间
        area_ranges = [
            (0, 50, "小户型(≤50㎡)"),
            (50, 100, "中户型(50-100㎡)"),
            (100, 150, "大户型(100-150㎡)"),
            (150, float('inf'), "超大户型(>150㎡)")
        ]
        
        results = []
        for min_area, max_area, range_name in area_ranges:
            # 筛选该面积范围的用户
            if max_area == float('inf'):
                users_in_range = self.db.query(database.User).filter(
                    database.User.house_area >= min_area
                ).all()
            else:
                users_in_range = self.db.query(database.User).filter(
                    and_(database.User.house_area >= min_area,
                         database.User.house_area < max_area)
                ).all()
            
            if not users_in_range:
                continue
            
            user_ids = [user.user_id for user in users_in_range]
            
            # 计算平均设备数量 - 分两步进行
            if user_ids:
                # 先获取每个用户的设备数量
                device_counts = self.db.query(
                    func.count(database.Device.device_id).label('device_count')
                ).filter(
                    database.Device.user_id.in_(user_ids)
                ).group_by(
                    database.Device.user_id
                ).all()
                
                # 然后计算平均值
                if device_counts:
                    avg_devices = sum(count.device_count for count in device_counts) / len(device_counts)
                else:
                    avg_devices = 0
            else:
                avg_devices = 0
            
            # 计算平均使用时长
            if user_ids:
                avg_usage_minutes = self.db.query(
                    func.avg(database.UsageRecord.duration_minutes)
                ).filter(
                    database.UsageRecord.user_id.in_(user_ids)
                ).scalar() or 0
                avg_usage_hours = avg_usage_minutes / 60 if avg_usage_minutes else 0
            else:
                avg_usage_hours = 0
            
            # 获取最受欢迎的设备类型
            if user_ids:
                popular_types = self.db.query(
                    database.DeviceType.type_name,
                    func.count(database.Device.device_id).label('count')
                ).join(
                    database.Device, database.DeviceType.type_id == database.Device.device_type_id
                ).filter(
                    database.Device.user_id.in_(user_ids)
                ).group_by(
                    database.DeviceType.type_name
                ).order_by(
                    func.count(database.Device.device_id).desc()
                ).limit(3).all()
            else:
                popular_types = []
            
            analysis = models.HouseAreaAnalysis(
                area_range=range_name,
                avg_devices_count=round(avg_devices, 2),
                avg_usage_hours=round(avg_usage_hours, 2),
                popular_device_types=[row.type_name for row in popular_types]
            )
            results.append(analysis)
        
        return results
    
    def generate_energy_consumption_report(self) -> Dict[str, Any]:
        """生成能耗分析报告"""
        # 按设备类型统计能耗
        energy_by_type = self.db.query(
            database.DeviceType.type_name,
            func.sum(database.UsageRecord.energy_consumed).label('total_energy')
        ).join(
            database.Device, database.DeviceType.type_id == database.Device.device_type_id
        ).join(
            database.UsageRecord, database.Device.device_id == database.UsageRecord.device_id
        ).group_by(
            database.DeviceType.type_name
        ).all()
        
        # 按用户统计能耗
        energy_by_user = self.db.query(
            database.User.username,
            func.sum(database.UsageRecord.energy_consumed).label('total_energy')
        ).join(
            database.UsageRecord, database.User.user_id == database.UsageRecord.user_id
        ).group_by(
            database.User.username
        ).order_by(
            func.sum(database.UsageRecord.energy_consumed).desc()
        ).limit(10).all()
        
        return {
            'energy_by_device_type': [
                {'type_name': row.type_name, 'total_energy': float(row.total_energy or 0)}
                for row in energy_by_type
            ],
            'top_energy_users': [
                {'username': row.username, 'total_energy': float(row.total_energy or 0)}
                for row in energy_by_user
            ]
        } 