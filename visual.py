import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import database
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.max_open_warning'] = 0

class SmartHomeVisualizer:
    """智能家居数据可视化类"""
    
    def __init__(self, db: Session):
        self.db = db
        self.output_dir = "visualizations"
        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def plot_device_usage_analysis(self, save_path: str = None):
        """绘制设备使用分析图表"""
        # 获取设备使用数据
        query = self.db.query(
            database.Device.device_name,
            database.DeviceType.type_name,
            func.count(database.UsageRecord.record_id).label('usage_count'),
            func.sum(database.UsageRecord.duration_minutes).label('total_minutes'),
            func.avg(database.UsageRecord.duration_minutes).label('avg_duration')
        ).join(
            database.DeviceType, database.Device.device_type_id == database.DeviceType.type_id
        ).outerjoin(
            database.UsageRecord, database.Device.device_id == database.UsageRecord.device_id
        ).group_by(database.Device.device_id).all()
        
        if not query:
            return None
        
        # 数据处理
        devices = [row.device_name for row in query]
        usage_counts = [row.usage_count or 0 for row in query]
        total_hours = [round(float(row.total_minutes or 0) / 60, 2) for row in query]
        avg_durations = [round(float(row.avg_duration or 0) / 60, 2) for row in query]
        
        # 创建子图
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('设备使用分析报告', fontsize=16, fontweight='bold')
        
        # 1. 设备使用频次柱状图
        ax1.bar(devices, usage_counts, color='skyblue', alpha=0.7)
        ax1.set_title('设备使用频次', fontsize=14)
        ax1.set_xlabel('设备名称')
        ax1.set_ylabel('使用次数')
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. 设备总使用时长
        ax2.barh(devices, total_hours, color='lightgreen', alpha=0.7)
        ax2.set_title('设备总使用时长', fontsize=14)
        ax2.set_xlabel('使用时长 (小时)')
        ax2.set_ylabel('设备名称')
        
        # 3. 平均使用时长
        colors = plt.cm.viridis(np.linspace(0, 1, len(devices)))
        ax3.scatter(range(len(devices)), avg_durations, c=colors, s=100, alpha=0.7)
        ax3.set_title('平均使用时长', fontsize=14)
        ax3.set_xlabel('设备序号')
        ax3.set_ylabel('平均时长 (小时)')
        ax3.set_xticks(range(len(devices)))
        ax3.set_xticklabels([f'设备{i+1}' for i in range(len(devices))])
        
        # 4. 使用时长分布饼图
        if sum(total_hours) > 0:
            ax4.pie(total_hours, labels=devices, autopct='%1.1f%%', startangle=90)
            ax4.set_title('设备使用时长分布', fontsize=14)
        else:
            ax4.text(0.5, 0.5, '暂无使用数据', ha='center', va='center', transform=ax4.transAxes)
        
        plt.tight_layout()
        
        # 先保存图表
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            saved_path = save_path
        else:
            saved_path = f'{self.output_dir}/device_usage_analysis.png'
            plt.savefig(saved_path, dpi=300, bbox_inches='tight')
        
        # 显示图表
        plt.show()
        
        plt.close()
        return saved_path
    
    def plot_user_activity_patterns(self, save_path: str = None):
        """绘制用户活动模式图表"""
        # 获取24小时活动数据
        query = self.db.query(
            func.hour(database.UsageRecord.start_time).label('hour'),
            func.count(database.UsageRecord.record_id).label('activity_count'),
            database.User.username
        ).join(
            database.User, database.UsageRecord.user_id == database.User.user_id
        ).group_by(
            func.hour(database.UsageRecord.start_time),
            database.User.user_id
        ).all()
        
        if not query:
            return None
        
        # 数据整理
        activity_data = {}
        for row in query:
            username = row.username
            hour = row.hour
            count = row.activity_count
            
            if username not in activity_data:
                activity_data[username] = [0] * 24
            activity_data[username][hour] = count
        
        # 创建图表
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        fig.suptitle('用户活动模式分析', fontsize=16, fontweight='bold')
        
        # 1. 24小时活动热力图
        if activity_data:
            users = list(activity_data.keys())
            hours_data = np.array([activity_data[user] for user in users])
            
            im = ax1.imshow(hours_data, cmap='Blues', aspect='auto')
            ax1.set_title('用户24小时活动热力图', fontsize=14)
            ax1.set_xlabel('小时')
            ax1.set_ylabel('用户')
            ax1.set_xticks(range(24))
            ax1.set_xticklabels([f'{i:02d}:00' for i in range(24)])
            ax1.set_yticks(range(len(users)))
            ax1.set_yticklabels(users)
            
            # 添加颜色条
            cbar = plt.colorbar(im, ax=ax1)
            cbar.set_label('活动次数')
        
        # 2. 整体活动趋势
        total_activity = [0] * 24
        for user_data in activity_data.values():
            for i, count in enumerate(user_data):
                total_activity[i] += count
        
        ax2.plot(range(24), total_activity, marker='o', linewidth=2, markersize=6)
        ax2.fill_between(range(24), total_activity, alpha=0.3)
        ax2.set_title('整体24小时活动趋势', fontsize=14)
        ax2.set_xlabel('小时')
        ax2.set_ylabel('总活动次数')
        ax2.set_xticks(range(0, 24, 2))
        ax2.set_xticklabels([f'{i:02d}:00' for i in range(0, 24, 2)])
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 先保存图表
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            saved_path = save_path
        else:
            saved_path = f'{self.output_dir}/user_activity_patterns.png'
            plt.savefig(saved_path, dpi=300, bbox_inches='tight')
        
        # 显示图表
        plt.show()
        
        plt.close()
        return saved_path
    
    def plot_user_habits_analysis(self, save_path: str = None):
        """绘制用户使用习惯分析图表"""
        # 获取用户设备使用数据
        query = self.db.query(
            database.User.username,
            database.Device.device_name,
            func.count(database.UsageRecord.record_id).label('usage_count'),
            func.sum(database.UsageRecord.duration_minutes).label('total_minutes')
        ).join(
            database.UsageRecord, database.User.user_id == database.UsageRecord.user_id
        ).join(
            database.Device, database.UsageRecord.device_id == database.Device.device_id
        ).group_by(
            database.User.user_id, database.Device.device_id
        ).all()
        
        if not query:
            return None
        
        # 数据整理
        user_device_usage = {}
        for row in query:
            username = row.username
            device = row.device_name
            usage_count = row.usage_count
            total_hours = round(float(row.total_minutes or 0) / 60, 2)
            
            if username not in user_device_usage:
                user_device_usage[username] = {}
            user_device_usage[username][device] = {
                'count': usage_count,
                'hours': total_hours
            }
        
        # 创建图表
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('用户使用习惯分析', fontsize=16, fontweight='bold')
        
        # 1. 用户设备使用频次对比
        if user_device_usage:
            users = list(user_device_usage.keys())[:5]  # 取前5个用户
            all_devices = set()
            for user_data in user_device_usage.values():
                all_devices.update(user_data.keys())
            devices = list(all_devices)[:8]  # 取前8个设备
            
            # 创建使用频次矩阵
            usage_matrix = []
            for user in users:
                user_usage = []
                for device in devices:
                    count = user_device_usage.get(user, {}).get(device, {}).get('count', 0)
                    user_usage.append(count)
                usage_matrix.append(user_usage)
            
            # 绘制热力图
            im1 = ax1.imshow(usage_matrix, cmap='YlOrRd', aspect='auto')
            ax1.set_title('用户设备使用频次热力图', fontsize=12)
            ax1.set_xlabel('设备')
            ax1.set_ylabel('用户')
            ax1.set_xticks(range(len(devices)))
            ax1.set_xticklabels(devices, rotation=45)
            ax1.set_yticks(range(len(users)))
            ax1.set_yticklabels(users)
            
            # 2. 用户最常用设备排行
            if users:
                user = users[0]  # 选择第一个用户
                user_devices = user_device_usage[user]
                sorted_devices = sorted(user_devices.items(), 
                                      key=lambda x: x[1]['count'], reverse=True)[:6]
                
                device_names = [item[0] for item in sorted_devices]
                counts = [item[1]['count'] for item in sorted_devices]
                
                ax2.bar(range(len(device_names)), counts, color='lightcoral', alpha=0.7)
                ax2.set_title(f'{user} 最常用设备排行', fontsize=12)
                ax2.set_xlabel('设备排名')
                ax2.set_ylabel('使用次数')
                ax2.set_xticks(range(len(device_names)))
                ax2.set_xticklabels([f'第{i+1}名' for i in range(len(device_names))])
                
                # 添加设备名称标签
                for i, (name, count) in enumerate(zip(device_names, counts)):
                    ax2.text(i, count + 0.5, name, ha='center', va='bottom', 
                            rotation=45, fontsize=8)
            
            # 3. 用户使用时长分布
            total_hours_by_user = {}
            for user, devices_data in user_device_usage.items():
                total_hours = sum(data['hours'] for data in devices_data.values())
                total_hours_by_user[user] = total_hours
            
            if total_hours_by_user:
                users_sorted = sorted(total_hours_by_user.items(), 
                                    key=lambda x: x[1], reverse=True)[:6]
                user_names = [item[0] for item in users_sorted]
                hours = [item[1] for item in users_sorted]
                
                ax3.pie(hours, labels=user_names, autopct='%1.1f%%', startangle=90)
                ax3.set_title('用户使用时长分布', fontsize=12)
            
            # 4. 设备使用时段偏好
            hour_usage = [0] * 24
            hour_query = self.db.query(
                func.hour(database.UsageRecord.start_time).label('hour'),
                func.count(database.UsageRecord.record_id).label('count')
            ).group_by(func.hour(database.UsageRecord.start_time)).all()
            
            for row in hour_query:
                if row.hour is not None:
                    hour_usage[row.hour] = row.count
            
            ax4.plot(range(24), hour_usage, marker='s', linewidth=2, 
                    color='green', markersize=4)
            ax4.fill_between(range(24), hour_usage, alpha=0.3, color='green')
            ax4.set_title('设备使用时段偏好', fontsize=12)
            ax4.set_xlabel('小时')
            ax4.set_ylabel('使用次数')
            ax4.set_xticks(range(0, 24, 3))
            ax4.set_xticklabels([f'{i:02d}:00' for i in range(0, 24, 3)])
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 先保存图表
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            saved_path = save_path
        else:
            saved_path = f'{self.output_dir}/user_habits_analysis.png'
            plt.savefig(saved_path, dpi=300, bbox_inches='tight')
        
        # 显示图表
        plt.show()
        
        plt.close()
        return saved_path
    
    def plot_house_area_impact(self, save_path: str = None):
        """绘制房屋面积影响分析图表"""
        # 获取房屋面积和设备使用数据
        query = self.db.query(
            database.User.house_area,
            func.count(database.Device.device_id).label('device_count'),
            func.sum(database.UsageRecord.duration_minutes).label('total_usage_minutes')
        ).outerjoin(
            database.Device, database.User.user_id == database.Device.user_id
        ).outerjoin(
            database.UsageRecord, database.Device.device_id == database.UsageRecord.device_id
        ).filter(
            database.User.house_area.isnot(None)
        ).group_by(database.User.user_id).all()
        
        if not query:
            return None
        
        # 数据处理
        areas = [float(row.house_area) for row in query if row.house_area]
        device_counts = [row.device_count or 0 for row in query]
        usage_hours = [round(float(row.total_usage_minutes or 0) / 60, 2) for row in query]
        
        # 创建面积区间
        area_ranges = ['小户型(<50㎡)', '中户型(50-100㎡)', '大户型(100-150㎡)', '超大户型(>150㎡)']
        area_stats = {range_name: {'count': 0, 'avg_devices': 0, 'avg_usage': 0} 
                     for range_name in area_ranges}
        
        for area, device_count, usage_hour in zip(areas, device_counts, usage_hours):
            if area < 50:
                range_key = '小户型(<50㎡)'
            elif area < 100:
                range_key = '中户型(50-100㎡)'
            elif area < 150:
                range_key = '大户型(100-150㎡)'
            else:
                range_key = '超大户型(>150㎡)'
            
            area_stats[range_key]['count'] += 1
            area_stats[range_key]['avg_devices'] += float(device_count)
            area_stats[range_key]['avg_usage'] += float(usage_hour)
        
        # 计算平均值
        for range_name in area_ranges:
            if area_stats[range_name]['count'] > 0:
                area_stats[range_name]['avg_devices'] /= area_stats[range_name]['count']
                area_stats[range_name]['avg_usage'] /= area_stats[range_name]['count']
        
        # 创建图表
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('房屋面积影响分析', fontsize=16, fontweight='bold')
        
        # 1. 面积与设备数量散点图
        ax1.scatter(areas, device_counts, alpha=0.6, s=60, c='blue')
        ax1.set_title('房屋面积 vs 设备数量', fontsize=14)
        ax1.set_xlabel('房屋面积 (㎡)')
        ax1.set_ylabel('设备数量')
        ax1.grid(True, alpha=0.3)
        
        # 添加趋势线
        if len(areas) > 1:
            z = np.polyfit(areas, device_counts, 1)
            p = np.poly1d(z)
            ax1.plot(areas, p(areas), "r--", alpha=0.8)
        
        # 2. 面积与使用时长散点图
        ax2.scatter(areas, usage_hours, alpha=0.6, s=60, c='green')
        ax2.set_title('房屋面积 vs 使用时长', fontsize=14)
        ax2.set_xlabel('房屋面积 (㎡)')
        ax2.set_ylabel('总使用时长 (小时)')
        ax2.grid(True, alpha=0.3)
        
        # 添加趋势线
        if len(areas) > 1:
            z = np.polyfit(areas, usage_hours, 1)
            p = np.poly1d(z)
            ax2.plot(areas, p(areas), "r--", alpha=0.8)
        
        # 3. 不同面积区间的平均设备数量
        ranges = [name for name in area_ranges if area_stats[name]['count'] > 0]
        avg_devices = [area_stats[name]['avg_devices'] for name in ranges]
        
        ax3.bar(ranges, avg_devices, color='orange', alpha=0.7)
        ax3.set_title('不同面积区间的平均设备数量', fontsize=14)
        ax3.set_xlabel('面积区间')
        ax3.set_ylabel('平均设备数量')
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. 不同面积区间的平均使用时长
        avg_usage = [area_stats[name]['avg_usage'] for name in ranges]
        
        ax4.bar(ranges, avg_usage, color='purple', alpha=0.7)
        ax4.set_title('不同面积区间的平均使用时长', fontsize=14)
        ax4.set_xlabel('面积区间')
        ax4.set_ylabel('平均使用时长 (小时)')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # 先保存图表
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            saved_path = save_path
        else:
            saved_path = f'{self.output_dir}/house_area_impact.png'
            plt.savefig(saved_path, dpi=300, bbox_inches='tight')
        
        # 显示图表
        plt.show()
        
        plt.close()
        return saved_path
    
    def generate_all_visualizations(self):
        """生成所有可视化图表"""
        results = {}
        
        try:
            results['device_usage'] = self.plot_device_usage_analysis()
            print("设备使用分析图表生成完成")
        except Exception as e:
            print(f"设备使用分析图表生成失败: {e}")
            results['device_usage'] = None
        
        try:
            results['user_activity'] = self.plot_user_activity_patterns()
            print("用户活动模式图表生成完成")
        except Exception as e:
            print(f"用户活动模式图表生成失败: {e}")
            results['user_activity'] = None
        
        try:
            results['user_habits'] = self.plot_user_habits_analysis()
            print("用户习惯分析图表生成完成")
        except Exception as e:
            print(f"用户习惯分析图表生成失败: {e}")
            results['user_habits'] = None
        
        try:
            results['house_area'] = self.plot_house_area_impact()
            print("房屋面积影响图表生成完成")
        except Exception as e:
            print(f"房屋面积影响图表生成失败: {e}")
            results['house_area'] = None
        
        return results 