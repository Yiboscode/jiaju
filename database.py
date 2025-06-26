import pymysql
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import DATABASE_CONFIG, DATABASE_URL

Base = declarative_base()

# 用户表
class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    house_area = Column(Float)  # 房屋面积（平方米）
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    devices = relationship("Device", back_populates="user")
    usage_records = relationship("UsageRecord", back_populates="user")
    security_events = relationship("SecurityEvent", back_populates="user")
    feedbacks = relationship("UserFeedback", back_populates="user")

# 设备类型表
class DeviceType(Base):
    __tablename__ = 'device_types'
    
    type_id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(50), unique=True, nullable=False)  # 如：灯具、空调、摄像头等
    description = Column(Text)
    
    # 关系
    devices = relationship("Device", back_populates="device_type")

# 设备表
class Device(Base):
    __tablename__ = 'devices'
    
    device_id = Column(Integer, primary_key=True, autoincrement=True)
    device_name = Column(String(100), nullable=False)
    device_type_id = Column(Integer, ForeignKey('device_types.type_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    room_location = Column(String(50))  # 房间位置
    status = Column(Boolean, default=False)  # 设备状态：开/关
    power_consumption = Column(Float, default=0.0)  # 功耗（瓦特）
    installation_date = Column(DateTime, default=datetime.now)
    last_maintenance = Column(DateTime)
    
    # 关系
    user = relationship("User", back_populates="devices")
    device_type = relationship("DeviceType", back_populates="devices")
    usage_records = relationship("UsageRecord", back_populates="device")
    security_events = relationship("SecurityEvent", back_populates="device")

# 使用记录表
class UsageRecord(Base):
    __tablename__ = 'usage_records'
    
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    device_id = Column(Integer, ForeignKey('devices.device_id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration_minutes = Column(Integer)  # 使用时长（分钟）
    energy_consumed = Column(Float, default=0.0)  # 消耗的电量（度）
    operation_type = Column(String(20))  # 操作类型：开机、关机、调节等
    
    # 关系
    user = relationship("User", back_populates="usage_records")
    device = relationship("Device", back_populates="usage_records")

# 安防事件表
class SecurityEvent(Base):
    __tablename__ = 'security_events'
    
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    device_id = Column(Integer, ForeignKey('devices.device_id'))
    event_type = Column(String(50), nullable=False)  # 事件类型：入侵、火警、门锁异常等
    severity_level = Column(String(20), default='低')  # 严重程度：低、中、高
    description = Column(Text)
    occurred_at = Column(DateTime, default=datetime.now)
    resolved_at = Column(DateTime)
    is_resolved = Column(Boolean, default=False)
    
    # 关系
    user = relationship("User", back_populates="security_events")
    device = relationship("Device", back_populates="security_events")

# 用户反馈表
class UserFeedback(Base):
    __tablename__ = 'user_feedbacks'
    
    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    feedback_type = Column(String(30))  # 反馈类型：bug报告、功能建议、使用体验等
    rating = Column(Integer)  # 评分 1-5
    content = Column(Text, nullable=False)
    submitted_at = Column(DateTime, default=datetime.now)
    is_processed = Column(Boolean, default=False)
    
    # 关系
    user = relationship("User", back_populates="feedbacks")

# 数据库引擎和会话
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """初始化数据库"""
    try:
        # 创建数据库（如果不存在）
        connection = pymysql.connect(
            host=DATABASE_CONFIG['host'],
            port=DATABASE_CONFIG['port'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            charset=DATABASE_CONFIG['charset']
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_CONFIG['database']}")
        connection.close()
        
        # 创建表
        Base.metadata.create_all(bind=engine)
        print("数据库初始化成功！")
        return True
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        return False