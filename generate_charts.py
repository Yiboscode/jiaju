#!/usr/bin/env python3
"""
智能家居数据可视化图表生成代码

使用matplotlib生成各种数据分析图表，包括：
1. 设备使用分析
2. 用户活动模式
3. 用户使用习惯
4. 房屋面积影响分析

用法：
    python generate_charts.py [--chart-type device|activity|habits|area|all]
"""

import argparse
import sys
from sqlalchemy.orm import Session
import database
from visual import SmartHomeVisualizer

def main():
    parser = argparse.ArgumentParser(description='生成智能家居数据分析图表')
    parser.add_argument(
        '--chart-type', 
        choices=['device', 'activity', 'habits', 'area', 'all'],
        default='all',
        help='选择要生成的图表类型 (默认: all)'
    )
    parser.add_argument(
        '--output-dir',
        default='visualizations',
        help='图表输出目录 (默认: visualizations)'
    )
    
    args = parser.parse_args()
    
    # 初始化数据库连接
    try:
        engine = database.engine
        with Session(engine) as db:
            visualizer = SmartHomeVisualizer(db)
            visualizer.output_dir = args.output_dir
            
            print("🎨 智能家居数据可视化图表生成器")
            print("=" * 50)
            print("📱 注意：图表将显示在新窗口中，请关闭窗口后继续")
            print()
            
            if args.chart_type == 'all':
                print("📊 生成所有图表...")
                results = visualizer.generate_all_visualizations()
                
                print("\n生成结果:")
                for chart_type, result in results.items():
                    status = "✅" if result else "❌"
                    print(f"{status} {chart_type}: {result if result else '生成失败'}")
                    
            elif args.chart_type == 'device':
                print("📱 生成设备使用分析图表...")
                result = visualizer.plot_device_usage_analysis()
                print(f"✅ 设备使用分析: {result}")
                
            elif args.chart_type == 'activity':
                print("🕐 生成用户活动模式图表...")
                result = visualizer.plot_user_activity_patterns()
                print(f"✅ 用户活动模式: {result}")
                
            elif args.chart_type == 'habits':
                print("💡 生成用户习惯分析图表...")
                result = visualizer.plot_user_habits_analysis()
                print(f"✅ 用户习惯分析: {result}")
                
            elif args.chart_type == 'area':
                print("🏠 生成房屋面积影响分析图表...")
                result = visualizer.plot_house_area_impact()
                print(f"✅ 房屋面积影响: {result}")
            
            print(f"\n📁 图表已保存到目录: {args.output_dir}")
            print("🎉 图表生成完成!")
            
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        print("请确保数据库服务正在运行且配置正确")
        sys.exit(1)

if __name__ == "__main__":
    main() 