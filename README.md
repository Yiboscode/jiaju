# 智能家居管理系统

基于 FastAPI 的智能家居设备管理和数据分析系统，提供完整的设备管理、使用记录追踪、安防事件监控和数据可视化分析功能。

## 📋 项目概述

智能家居管理系统是一个现代化的物联网设备管理平台，主要功能包括：

- 🏠 **用户与设备管理**：用户注册、设备添加、设备类型管理
- 📊 **使用记录追踪**：设备使用时间、能耗统计、操作记录
- 🔒 **安防事件监控**：安全事件记录、异常报警、事件处理
- 📝 **用户反馈系统**：用户体验收集、问题反馈处理
- 📈 **数据分析可视化**：使用模式分析、能耗报告、习惯洞察

## 🏗️ 系统架构

```
智能家居管理系统/
├── main.py              # FastAPI 主应用入口
├── models.py            # Pydantic 数据模型定义
├── database.py          # SQLAlchemy 数据库模型
├── crud.py              # 数据库 CRUD 操作
├── config.py            # 数据库和API配置
├── analytics.py         # 智能数据分析逻辑
├── visual.py            # 数据可视化组件
├── generate_charts.py   # 图表生成脚本
├── test.py              # API 接口自动化测试脚本
├── smart_home_db.sql    # 数据库结构和示例数据
├── requirements.txt     # 项目依赖
├── visualizations/      # 生成的可视化图表目录
└── README.md           # 项目文档
```

## 🛠️ 技术栈

- **后端框架**: FastAPI 0.104.1
- **数据库**: MySQL 8.0 + SQLAlchemy 2.0.23
- **数据分析**: Pandas 2.1.4 + NumPy
- **可视化**: Matplotlib 3.8.2 + Seaborn 0.13.0
- **数据库连接**: PyMySQL 1.1.0

## 📦 安装与配置

### 1. 环境要求

- Python 3.8+
- MySQL 8.0+
- Git

### 2. 克隆项目

```bash
git clone <your-repository-url>
cd jiaju
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 数据库配置

#### 方法一：导入现有数据库（推荐）

```bash
# 1. 创建数据库
mysql -u root -p -e "CREATE DATABASE smart_home_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"

# 2. 导入数据结构和示例数据
mysql -u root -p smart_home_db < smart_home_db.sql
```

#### 方法二：修改配置文件

编辑 `config.py` 文件，修改数据库连接信息：

```python
DATABASE_CONFIG = {
    'host': 'localhost',        # 数据库主机
    'port': 3306,              # 数据库端口
    'user': 'root',            # 数据库用户名
    'password': 'your_password', # 数据库密码
    'database': 'smart_home_db', # 数据库名称
    'charset': 'utf8mb4'
}
```

### 5. 启动应用

```bash
# 开发模式启动
python main.py

# 或使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

应用启动后访问：
- 健康检查：http://localhost:8000/health

## 🎯 API 接口说明



### 🔧 主要接口模块

#### 1. 用户管理 (`/users/`)

| 方法 | 端点 | 功能 | 描述 |
|------|------|------|------|
| POST | `/users/` | 创建用户 | 注册新用户 |
| GET | `/users/` | 用户列表 | 获取所有用户（支持分页） |
| GET | `/users/{user_id}` | 用户详情 | 获取指定用户信息 |
| PUT | `/users/{user_id}` | 更新用户 | 修改用户信息 |
| DELETE | `/users/{user_id}` | 删除用户 | 删除用户及关联数据 |

#### 2. 设备类型管理 (`/device-types/`)

| 方法 | 端点 | 功能 | 描述 |
|------|------|------|------|
| POST | `/device-types/` | 创建设备类型 | 添加新的设备类型 |
| GET | `/device-types/` | 设备类型列表 | 获取所有设备类型 |
| DELETE | `/device-types/{type_id}` | 删除设备类型 | 删除设备类型 |

#### 3. 设备管理 (`/devices/`)

| 方法 | 端点 | 功能 | 描述 |
|------|------|------|------|
| POST | `/devices/` | 创建设备 | 为用户添加新设备 |
| GET | `/devices/` | 设备列表 | 获取所有设备（支持分页） |
| GET | `/devices/{device_id}` | 设备详情 | 获取指定设备信息 |
| GET | `/users/{user_id}/devices` | 用户设备 | 获取用户的所有设备 |
| PUT | `/devices/{device_id}` | 更新设备 | 修改设备信息 |
| DELETE | `/devices/{device_id}` | 删除设备 | 删除设备及使用记录 |

#### 4. 使用记录管理 (`/usage-records/`)

| 方法 | 端点 | 功能 | 描述 |
|------|------|------|------|
| POST | `/usage-records/` | 创建使用记录 | 记录设备使用情况 |
| GET | `/usage-records/` | 使用记录列表 | 获取所有使用记录 |
| GET | `/users/{user_id}/usage-records` | 用户使用记录 | 获取用户的使用记录 |
| GET | `/devices/{device_id}/usage-records` | 设备使用记录 | 获取设备的使用记录 |
| DELETE | `/usage-records/{record_id}` | 删除使用记录 | 删除使用记录 |

#### 5. 安防事件管理 (`/security-events/`)

| 方法 | 端点 | 功能 | 描述 |
|------|------|------|------|
| POST | `/security-events/` | 创建安防事件 | 记录安全事件 |
| GET | `/security-events/` | 安防事件列表 | 获取所有安防事件 |
| GET | `/users/{user_id}/security-events` | 用户安防事件 | 获取用户的安防事件 |
| PUT | `/security-events/{event_id}` | 更新安防事件 | 修改事件状态 |
| DELETE | `/security-events/{event_id}` | 删除安防事件 | 删除安防事件 |

#### 6. 用户反馈管理 (`/user-feedbacks/`)

| 方法 | 端点 | 功能 | 描述 |
|------|------|------|------|
| POST | `/user-feedbacks/` | 创建用户反馈 | 提交用户反馈 |
| GET | `/user-feedbacks/` | 反馈列表 | 获取所有用户反馈 |
| GET | `/users/{user_id}/feedbacks` | 用户反馈 | 获取用户的反馈 |
| PUT | `/user-feedbacks/{feedback_id}` | 更新反馈状态 | 标记反馈处理状态 |
| DELETE | `/user-feedbacks/{feedback_id}` | 删除反馈 | 删除用户反馈 |

#### 7. 数据分析 (`/analytics/`)

| 方法 | 端点 | 功能 | 描述 |
|------|------|------|------|
| GET | `/analytics/device-usage` | 设备使用分析 | 获取设备使用频率和时长分析 |
| GET | `/analytics/user-habits` | 用户习惯分析 | 分析用户使用习惯和偏好 |
| GET | `/analytics/house-area-impact` | 房屋面积影响分析 | 分析房屋面积对设备使用的影响 |
| GET | `/analytics/energy-consumption` | 能耗报告 | 获取能耗分析报告 |

## 🧪 接口测试方法

### 1. 自动化测试脚本

项目提供了完整的自动化测试脚本 `test.py`，可以一键测试所有接口：

```bash
# 运行完整测试套件
python test.py

# 测试结果会显示每个接口的测试状态和响应数据
```

测试脚本功能：
- ✅ 自动创建测试数据
- ✅ 测试所有 CRUD 操作
- ✅ 测试数据分析接口
- ✅ 自动清理测试数据
- ✅ 生成详细的测试报告

### 2. 手动测试方法

#### 使用 curl 命令测试

**创建用户**：
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "张三",
    "email": "zhangsan@example.com",
    "phone": "13800138000",
    "house_area": 88.5
  }'
```

**获取用户列表**：
```bash
curl -X GET "http://localhost:8000/users/"
```

**创建设备类型**：
```bash
curl -X POST "http://localhost:8000/device-types/" \
  -H "Content-Type: application/json" \
  -d '{
    "type_name": "智能灯泡",
    "description": "可调光调色的智能LED灯泡"
  }'
```

**创建设备**：
```bash
curl -X POST "http://localhost:8000/devices/" \
  -H "Content-Type: application/json" \
  -d '{
    "device_name": "客厅主灯",
    "device_type_id": 1,
    "user_id": 1,
    "room_location": "客厅",
    "power_consumption": 9.5
  }'
```

**创建使用记录**：
```bash
curl -X POST "http://localhost:8000/usage-records/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "device_id": 1,
    "start_time": "2024-01-20T18:00:00",
    "end_time": "2024-01-20T22:00:00",
    "operation_type": "开灯"
  }'
```



### 3. 测试数据示例

#### 用户数据：
```json
{
  "username": "李四",
  "email": "lisi@example.com", 
  "phone": "13900139000",
  "house_area": 120.0
}
```

#### 设备数据：
```json
{
  "device_name": "卧室空调",
  "device_type_id": 2,
  "user_id": 1,
  "room_location": "主卧",
  "power_consumption": 800.0
}
```

#### 使用记录数据：
```json
{
  "user_id": 1,
  "device_id": 2,
  "start_time": "2024-01-20T14:00:00",
  "end_time": "2024-01-20T18:00:00",
  "operation_type": "制冷"
}
```

## 📊 数据可视化图表

### 1. 图表生成脚本

项目提供了便捷的图表生成脚本 `generate_charts.py`：

```bash
# 生成所有图表
python generate_charts.py

# 生成特定类型图表
python generate_charts.py --chart-type device      # 设备使用分析
python generate_charts.py --chart-type activity    # 用户活动模式
python generate_charts.py --chart-type habits      # 用户习惯分析  
python generate_charts.py --chart-type area        # 房屋面积影响
python generate_charts.py --chart-type energy      # 能耗分析

# 指定输出目录
python generate_charts.py --output-dir my_charts
```

### 2. 五大可视化分析

#### 📱 图表1：设备使用分析

- **设备使用频次柱状图** - 识别最常用设备
- **设备总使用时长横向柱状图** - 分析设备利用率
- **平均使用时长散点图** - 发现使用模式
- **使用时长分布饼图** - 直观对比设备占比

**核心发现**：空调设备是使用时长主力（18.5小时），电视设备使用频次高但时长适中（7小时）

#### 🕐 图表2：用户活动模式分析

- **24小时活动热力图** - 展示用户全天活动分布
- **整体活动趋势线图** - 识别活跃时间规律
- **用户活跃度对比图** - 分析个体差异

**核心发现**：设备使用集中在8-10点和19-20点，符合居家生活规律

#### 💡 图表3：用户习惯分析

- **用户设备使用频次热力图** - 发现使用偏好
- **最常用设备排行图** - 个性化使用分析
- **用户使用时长分布饼图** - 对比用户活跃度
- **设备使用时段偏好图** - 时间规律挖掘

**核心发现**：张伟倾向设备联动使用（空调+冰箱+电视），王芳使用更规律（空调+洗衣机）

#### 🏠 图表4：房屋面积影响分析

- **面积与设备数量散点图** - 分析配置关系
- **面积与使用时长散点图** - 发现使用强度规律
- **不同面积区间平均设备数量** - 横向对比分析
- **不同面积区间平均使用时长** - 深度洞察

**核心发现**：中户型（50-100㎡）设备利用率最高（10.19小时），超大户型使用强度反而最低

#### ⚡ 图表5：能耗分析

- **设备类型能耗对比柱状图** - 识别耗电大户
- **设备类型能耗占比饼图** - 能耗结构分析
- **用户能耗排行榜** - 用电行为对比
- **设备功耗效率对比图** - 节能潜力评估

**核心发现**：变频空调占总能耗87%（30.17度），LED灯具最节能（0.077度），部分设备存在节能优化空间

### 3. 图表文件输出

所有生成的图表会保存在 `visualizations/` 目录下：

```
visualizations/
├── device_usage_analysis.png       # 设备使用分析
├── user_activity_patterns.png      # 用户活动模式
├── user_habits_analysis.png        # 用户习惯分析
├── house_area_impact.png          # 房屋面积影响
└── energy_consumption_analysis.png # 能耗分析
```

### 4. 自定义图表生成

你也可以通过 Python 代码直接调用可视化模块：

```python
from sqlalchemy.orm import Session
import database
from visual import SmartHomeVisualizer

# 创建数据库会话
engine = database.engine
with Session(engine) as db:
    visualizer = SmartHomeVisualizer(db)
    
    # 生成单个图表
    device_chart = visualizer.plot_device_usage_analysis()
    energy_chart = visualizer.plot_energy_consumption_analysis()
    
    # 生成所有图表
    results = visualizer.generate_all_visualizations()
    print("图表生成结果:", results)
```

## 📁 数据库结构



### 核心数据表设计

| 表名                  | 功能         | 关键字段                          | 特色功能           |
| --------------------- | ------------ | --------------------------------- | ------------------ |
| **users**             | 用户信息管理 | house_area, city                  | 支持房屋面积分析   |
| **device_types**      | 设备类型定义 | avg_power_consumption             | 标准功耗参数       |
| **devices**           | 设备实例管理 | actual_power_consumption          | 实际vs额定功耗对比 |
| **usage_records**     | 使用记录追踪 | energy_consumed, duration_minutes | 自动能耗计算       |
| **security_events**   | 安防事件管理 | severity_level, is_resolved       | 事件分级处理       |
| **user_feedbacks**    | 用户反馈收集 | rating, is_processed              | 评分反馈系统       |
| **energy_statistics** | 能耗统计分析 | daily_consumption, cost           | 详细能耗报告       |

### 数据模型亮点

- **外键完整性**：严格的数据关联关系
- **自动时间戳**：created_at, updated_at 自动维护
- **能耗自动计算**：基于功耗和使用时长自动计算能耗
- **数据验证**：Pydantic 模型确保数据类型安全

## 🔬 核心分析算法

### 1. 设备使用频率分析

- **时间聚合算法**：按小时统计使用频次，识别高峰时段
- **设备利用率计算**：总使用时长/总时间，评估设备价值
- **模式识别**：基于使用记录识别用户行为模式

### 2. 用户习惯挖掘

- **设备联动检测**：时间窗口重叠分析，发现同时使用设备
- **偏好权重计算**：基于使用频次和时长的综合评分
- **个性化标签**：为用户生成使用习惯标签

### 3. 房屋面积影响模型

- **分层抽样分析**：按面积区间分组，计算平均值
- **相关性分析**：面积与设备数量、使用时长的关系
- **最优配置推荐**：基于分析结果提供设备配置建议

### 4. 能耗优化算法

- **设备能效评估**：实际功耗vs额定功耗对比分析
- **节能潜力识别**：找出能耗异常和优化空间
- **成本效益分析**：电费成本计算和节能建议



## 🚀 主要项目成果

### 📊 数据分析发现

1. 设备使用模式
   - 空调设备是使用时长绝对主力（30.5小时，占总时长31%）
   - 冰箱24小时运行但相对节能（日耗0.6-0.65度）
   - 电视设备使用频次高但时长适中（7小时）
2. 用户行为洞察
   - 明显的设备联动模式：67%活跃用户有固定设备组合
   - 时间规律性强：主要活跃时段为8-10点和19-20点
   - 个体差异明显：不同用户展现不同的使用模式
3. 房屋面积影响
   - 中户型（50-100㎡）设备利用率最高（10.19小时）
   - 超大户型（>150㎡）使用时长反而最低（0小时）
   - 最优设备配置点：中等面积房屋（平均5.5台设备）
4. 能耗优化建议
   - 空调占总能耗87%，是节能重点对象
   - LED灯具表现优异，平均能耗仅0.077度
   - 部分设备功耗效率超标，存在20-30%节能空间

