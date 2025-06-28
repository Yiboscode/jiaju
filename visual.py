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
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']  # 支持中文显示
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

class SmartHomeVisualizer:
    """智能家居数据可视化类"""
    
    def __init__(self, db: Session):
        self.db = db
        self.output_dir = "visualizations"
        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def plot_device_usage_analysis(self, save_path: str = None):
        """绘制设备使用分析图表 - 基于API数据"""
        from analytics import SmartHomeAnalytics
        
        print("开始获取设备使用分析数据 (来自API)...")
        
        # 使用API数据源
        analytics = SmartHomeAnalytics(self.db)
        api_data = analytics.analyze_device_usage_frequency()
        
        # 打印设备使用分析数据
        print("\n" + "="*60)
        print("设备使用分析数据详情 (API数据源)")
        print("="*60)
        
        print("\n1. 设备使用详细统计:")
        print("-" * 50)
        if api_data:
            for i, device in enumerate(api_data, 1):
                print(f"  {i}. 设备: {device.device_name}")
                print(f"     类型: {device.device_type}")
                print(f"     总使用时长: {device.total_usage_hours} 小时")
                print(f"     使用频次: {device.usage_frequency} 次")
                print(f"     平均单次时长: {device.avg_session_duration} 分钟")
                print(f"     高峰使用时段: {device.peak_usage_hours}")
                print()
        else:
            print("  暂无设备使用数据")
        
        print(f"总计统计设备数: {len(api_data)}")
        total_hours = sum(device.total_usage_hours for device in api_data)
        total_frequency = sum(device.usage_frequency for device in api_data)
        print(f"所有设备总使用时长: {total_hours:.2f} 小时")
        print(f"所有设备总使用频次: {total_frequency} 次")
        print("="*60)
        
        if not api_data:
            print("没有足够的数据生成设备使用分析图表")
            return None
        
        # 数据处理
        devices = [device.device_name for device in api_data]
        usage_counts = [device.usage_frequency for device in api_data]
        total_hours = [device.total_usage_hours for device in api_data]
        avg_durations = [device.avg_session_duration / 60 for device in api_data]  # 转换为小时
        
        # 创建子图
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('设备使用分析报告 (API数据源)', fontsize=16, fontweight='bold')
        
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
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.savefig(f'{self.output_dir}/device_usage_analysis.png', dpi=300, bbox_inches='tight')
        
        plt.close()
        print(f"设备使用分析图表已保存: {self.output_dir}/device_usage_analysis.png")
        return f'{self.output_dir}/device_usage_analysis.png'
    
    def plot_user_activity_patterns(self, save_path: str = None):
        """绘制用户活动模式图表 - 直接数据库查询（无对应API）"""
        print("开始获取用户活动模式数据 (直接数据库查询)...")
        
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
        
        # 打印用户活动模式数据
        print("\n" + "="*60)
        print("用户活动模式数据详情 (直接数据库查询)")
        print("="*60)
        
        if not query:
            print("没有足够的数据生成用户活动模式图表")
            return None
        
        # 数据整理
        activity_data = {}
        hourly_summary = {}
        
        for row in query:
            username = row.username
            hour = row.hour
            count = row.activity_count
            
            if username not in activity_data:
                activity_data[username] = [0] * 24
            activity_data[username][hour] = count
            
            # 按小时汇总
            if hour not in hourly_summary:
                hourly_summary[hour] = 0
            hourly_summary[hour] += count
        
        print("\n1. 用户活动分布:")
        print("-" * 40)
        for username, hours_data in activity_data.items():
            total_activity = sum(hours_data)
            active_hours = [i for i, count in enumerate(hours_data) if count > 0]
            print(f"  用户: {username}")
            print(f"    总活动次数: {total_activity}")
            print(f"    活跃时段: {active_hours}")
            print()
        
        print("\n2. 24小时活动汇总:")
        print("-" * 40)
        for hour in sorted(hourly_summary.keys()):
            print(f"  {hour:02d}:00 - {hour+1:02d}:00: {hourly_summary[hour]} 次活动")
        
        total_activities = sum(hourly_summary.values())
        peak_hour = max(hourly_summary.keys(), key=lambda x: hourly_summary[x])
        print(f"\n总活动次数: {total_activities}")
        print(f"最活跃时段: {peak_hour:02d}:00-{peak_hour+1:02d}:00 ({hourly_summary[peak_hour]}次)")
        print(f"统计用户数: {len(activity_data)}")
        print("="*60)
        
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
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.savefig(f'{self.output_dir}/user_activity_patterns.png', dpi=300, bbox_inches='tight')
        
        plt.close()
        print(f"用户活动模式图表已保存: {self.output_dir}/user_activity_patterns.png")
        return f'{self.output_dir}/user_activity_patterns.png'
    
    def plot_user_habits_analysis(self, save_path: str = None):
        """绘制用户使用习惯分析图表 - 基于API数据"""
        from analytics import SmartHomeAnalytics
        
        print("开始获取用户使用习惯数据 (来自API)...")
        
        # 使用API数据源
        analytics = SmartHomeAnalytics(self.db)
        api_data = analytics.analyze_user_habits()
        
        # 打印用户习惯分析数据
        print("\n" + "="*60)
        print("用户使用习惯数据详情 (API数据源)")
        print("="*60)
        
        print("\n1. 用户习惯详细分析:")
        print("-" * 50)
        if api_data:
            for i, user_habit in enumerate(api_data, 1):
                print(f"  {i}. 用户: {user_habit.username} (ID: {user_habit.user_id})")
                print(f"     常用设备组合: {user_habit.frequently_used_together}")
                print(f"     活跃时段: {user_habit.peak_activity_hours}")
                print(f"     最爱设备: {user_habit.favorite_devices}")
                print()
        else:
            print("  暂无用户习惯数据")
        
        # 统计汇总
        total_users = len(api_data)
        users_with_combinations = len([u for u in api_data if u.frequently_used_together])
        users_with_peaks = len([u for u in api_data if u.peak_activity_hours])
        
        print(f"总用户数: {total_users}")
        print(f"有设备组合习惯的用户: {users_with_combinations}")
        print(f"有明显活跃时段的用户: {users_with_peaks}")
        print("="*60)
        
        if not api_data:
            print("没有足够的数据生成用户习惯分析图表")
            return None
        
        # 辅助数据查询（用于可视化图表）
        user_device_query = self.db.query(
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
        
        # 数据整理
        user_device_usage = {}
        for row in user_device_query:
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
        fig.suptitle('用户使用习惯分析 (API数据源)', fontsize=16, fontweight='bold')
        
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
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.savefig(f'{self.output_dir}/user_habits_analysis.png', dpi=300, bbox_inches='tight')
        
        plt.close()
        print(f"用户习惯分析图表已保存: {self.output_dir}/user_habits_analysis.png")
        return f'{self.output_dir}/user_habits_analysis.png'
    
    def plot_house_area_impact(self, save_path: str = None):
        """绘制房屋面积影响分析图表 - 基于API数据"""
        from analytics import SmartHomeAnalytics
        
        print("开始获取房屋面积影响数据 (来自API)...")
        
        # 使用API数据源
        analytics = SmartHomeAnalytics(self.db)
        api_data = analytics.analyze_house_area_impact()
        
        # 打印房屋面积影响分析数据
        print("\n" + "="*60)
        print("房屋面积影响分析数据详情 (API数据源)")
        print("="*60)
        
        print("\n1. 不同面积区间分析:")
        print("-" * 50)
        if api_data:
            for i, area_analysis in enumerate(api_data, 1):
                print(f"  {i}. 面积区间: {area_analysis.area_range}")
                print(f"     平均设备数量: {area_analysis.avg_devices_count}")
                print(f"     平均使用时长: {area_analysis.avg_usage_hours} 小时")
                print(f"     热门设备类型: {area_analysis.popular_device_types}")
                print()
        else:
            print("  暂无房屋面积数据")
        
        print(f"统计面积区间数: {len(api_data)}")
        total_avg_devices = sum(area.avg_devices_count for area in api_data)
        total_avg_usage = sum(area.avg_usage_hours for area in api_data)
        print(f"所有区间平均设备数: {total_avg_devices / len(api_data):.2f}" if api_data else "0")
        print(f"所有区间平均使用时长: {total_avg_usage / len(api_data):.2f} 小时" if api_data else "0")
        print("="*60)
        
        if not api_data:
            print("没有足够的数据生成房屋面积影响图表")
            return None
        
        # 辅助数据查询（用于散点图）
        scatter_query = self.db.query(
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
        
        # 数据处理
        areas = [float(row.house_area) for row in scatter_query if row.house_area]
        device_counts = [row.device_count or 0 for row in scatter_query]
        usage_hours = [round(float(row.total_usage_minutes or 0) / 60, 2) for row in scatter_query]
        
        # 创建图表
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('房屋面积影响分析 (API数据源)', fontsize=16, fontweight='bold')
        
        # 1. 面积与设备数量散点图
        if areas:
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
        if areas:
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
        
        # 3. 不同面积区间的平均设备数量（基于API数据）
        ranges = [area.area_range for area in api_data]
        avg_devices = [area.avg_devices_count for area in api_data]
        
        ax3.bar(ranges, avg_devices, color='orange', alpha=0.7)
        ax3.set_title('不同面积区间的平均设备数量', fontsize=14)
        ax3.set_xlabel('面积区间')
        ax3.set_ylabel('平均设备数量')
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. 不同面积区间的平均使用时长（基于API数据）
        avg_usage = [area.avg_usage_hours for area in api_data]
        
        ax4.bar(ranges, avg_usage, color='purple', alpha=0.7)
        ax4.set_title('不同面积区间的平均使用时长', fontsize=14)
        ax4.set_xlabel('面积区间')
        ax4.set_ylabel('平均使用时长 (小时)')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.savefig(f'{self.output_dir}/house_area_impact.png', dpi=300, bbox_inches='tight')
        
        plt.close()
        print(f"房屋面积影响图表已保存: {self.output_dir}/house_area_impact.png")
        return f'{self.output_dir}/house_area_impact.png'
    
    def plot_energy_consumption_analysis(self, save_path: str = None):
        """绘制能耗分析图表 - 基于API数据"""
        from analytics import SmartHomeAnalytics
        
        print("开始获取能耗分析数据 (来自API)...")
        
        # 使用API数据源
        analytics = SmartHomeAnalytics(self.db)
        api_data = analytics.generate_energy_consumption_report()
        
        # 打印能耗分析数据
        print("\n" + "="*60)
        print("能耗分析数据详情 (API数据源)")
        print("="*60)
        
        print("\n1. 按设备类型统计能耗 (来自API):")
        print("-" * 50)
        if api_data['energy_by_device_type']:
            for i, item in enumerate(api_data['energy_by_device_type'], 1):
                print(f"  {i}. {item['type_name']}: {item['total_energy']:.3f} 千瓦时")
        else:
            print("  暂无设备类型能耗数据")
        
        print("\n2. 按用户统计能耗 (来自API):")
        print("-" * 50)
        if api_data['top_energy_users']:
            for i, item in enumerate(api_data['top_energy_users'], 1):
                print(f"  {i}. {item['username']}: {item['total_energy']:.3f} 千瓦时")
        else:
            print("  暂无用户能耗数据")
        
        # 获取设备功耗效率数据（直接查询，因为API中没有）
        efficiency_data = self.db.query(
            database.Device.device_name,
            database.DeviceType.type_name,
            database.DeviceType.avg_power_consumption.label('rated_power'),
            database.Device.actual_power_consumption.label('actual_power')
        ).join(
            database.DeviceType, database.Device.device_type_id == database.DeviceType.type_id
        ).filter(
            database.Device.actual_power_consumption.isnot(None),
            database.DeviceType.avg_power_consumption.isnot(None)
        ).limit(10).all()
        
        print("\n3. 设备功耗效率对比 (补充数据):")
        print("-" * 50)
        if efficiency_data:
            print("  设备名称 | 设备类型 | 额定功耗(W) | 实际功耗(W) | 效率比")
            print("  " + "-" * 60)
            for row in efficiency_data:
                rated = float(row.rated_power or 0)
                actual = float(row.actual_power or 0)
                efficiency = (actual / rated * 100) if rated > 0 else 0
                print(f"  {row.device_name} | {row.type_name} | {rated:.1f} | {actual:.1f} | {efficiency:.1f}%")
        else:
            print("  暂无功耗效率数据")
        
        # 计算总体统计
        total_by_type = sum(item['total_energy'] for item in api_data['energy_by_device_type'])
        total_by_user = sum(item['total_energy'] for item in api_data['top_energy_users'])
        
        print("\n4. 总体统计 (API数据):")
        print("-" * 50)
        print(f"  设备类型总能耗: {total_by_type:.3f} 千瓦时")
        print(f"  用户总能耗: {total_by_user:.3f} 千瓦时")
        print(f"  统计设备类型数: {len(api_data['energy_by_device_type'])}")
        print(f"  统计用户数: {len(api_data['top_energy_users'])}")
        print(f"  功耗效率统计设备数: {len(efficiency_data) if efficiency_data else 0}")
        print("="*60)
        
        if not api_data['energy_by_device_type'] and not api_data['top_energy_users']:
            print("API返回数据不足，无法生成图表")
            return None
        
        # 创建子图
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('能耗分析报告 (API数据源)', fontsize=16, fontweight='bold')
        
        # 1. 设备类型能耗对比柱状图（基于API数据）
        if api_data['energy_by_device_type']:
            type_names = [item['type_name'] for item in api_data['energy_by_device_type']]
            type_energies = [item['total_energy'] for item in api_data['energy_by_device_type']]
            
            bars = ax1.bar(range(len(type_names)), type_energies,
                          color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'])
            ax1.set_title('设备类型能耗对比 (API数据)', fontsize=14)
            ax1.set_xlabel('设备类型')
            ax1.set_ylabel('总能耗 (千瓦时)')
            ax1.set_xticks(range(len(type_names)))
            ax1.set_xticklabels(type_names, rotation=45, ha='right')
            
            # 在柱子上显示数值
            for bar, energy in zip(bars, type_energies):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        f'{energy:.2f}', ha='center', va='bottom')
        
        # 2. 设备类型能耗饼图（基于API数据）
        if api_data['energy_by_device_type']:
            ax2.pie(type_energies, labels=type_names, autopct='%1.1f%%', startangle=90,
                    colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'])
            ax2.set_title('设备类型能耗占比 (API数据)', fontsize=14)
        
        # 3. 用户能耗排行榜（基于API数据）
        if api_data['top_energy_users']:
            usernames = [item['username'] for item in api_data['top_energy_users']]
            user_energies = [item['total_energy'] for item in api_data['top_energy_users']]
            
            bars = ax3.barh(range(len(usernames)), user_energies, color='lightcoral')
            ax3.set_title('用户能耗排行榜 (API数据)', fontsize=14)
            ax3.set_xlabel('总能耗 (千瓦时)')
            ax3.set_ylabel('用户')
            ax3.set_yticks(range(len(usernames)))
            ax3.set_yticklabels(usernames)
            
            # 在柱子上显示数值
            for bar, energy in zip(bars, user_energies):
                ax3.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                        f'{energy:.2f}', ha='left', va='center')
        
        # 4. 能耗效率分析（实际功耗 vs 额定功耗）
        if efficiency_data:
            device_names = [row.device_name for row in efficiency_data]
            rated_powers = [float(row.rated_power or 0) for row in efficiency_data]
            actual_powers = [float(row.actual_power or 0) for row in efficiency_data]
            
            x = np.arange(len(device_names))
            width = 0.35
            
            ax4.bar(x - width/2, rated_powers, width, label='额定功耗', alpha=0.8, color='skyblue')
            ax4.bar(x + width/2, actual_powers, width, label='实际功耗', alpha=0.8, color='orange')
            
            ax4.set_title('设备功耗效率对比', fontsize=14)
            ax4.set_xlabel('设备')
            ax4.set_ylabel('功耗 (瓦)')
            ax4.set_xticks(x)
            ax4.set_xticklabels([f'设备{i+1}' for i in range(len(device_names))], rotation=45)
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        else:
            ax4.text(0.5, 0.5, '暂无功耗效率数据', ha='center', va='center',
                    transform=ax4.transAxes, fontsize=14)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.savefig(f'{self.output_dir}/energy_consumption_analysis.png', dpi=300, bbox_inches='tight')
        
        plt.close()
        print(f"能耗分析图表已保存: {self.output_dir}/energy_consumption_analysis.png")
        return f'{self.output_dir}/energy_consumption_analysis.png'
    
    def generate_all_visualizations(self):
        """生成所有可视化图表 - 基于API数据源"""
        results = {}
        
        print("开始生成所有可视化图表 (基于API数据源)")
        print("="*60)
        
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
        
        try:
            results['energy_consumption'] = self.plot_energy_consumption_analysis()
            print("能耗分析图表生成完成")
        except Exception as e:
            print(f"能耗分析图表生成失败: {e}")
            results['energy_consumption'] = None
        
        print("="*60)
        print("所有图表生成完成!")
        
        return results