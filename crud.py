from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from typing import List, Optional
import database
import models

# 用户CRUD操作
def create_user(db: Session, user: models.UserCreate):
    db_user = database.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(database.User).filter(database.User.user_id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(database.User).filter(database.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_update: models.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db_user.updated_at = datetime.now()
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        # 先删除相关的使用记录
        db.query(database.UsageRecord).filter(database.UsageRecord.user_id == user_id).delete()
        
        # 删除相关的安防事件
        db.query(database.SecurityEvent).filter(database.SecurityEvent.user_id == user_id).delete()
        
        # 删除相关的用户反馈
        db.query(database.UserFeedback).filter(database.UserFeedback.user_id == user_id).delete()
        
        # 删除用户的设备
        db.query(database.Device).filter(database.Device.user_id == user_id).delete()
        
        # 最后删除用户
        db.delete(db_user)
        db.commit()
    return db_user

# 设备类型CRUD操作
def create_device_type(db: Session, device_type: models.DeviceTypeCreate):
    db_device_type = database.DeviceType(**device_type.dict())
    db.add(db_device_type)
    db.commit()
    db.refresh(db_device_type)
    return db_device_type

def get_device_types(db: Session):
    return db.query(database.DeviceType).all()

def get_device_type(db: Session, type_id: int):
    return db.query(database.DeviceType).filter(database.DeviceType.type_id == type_id).first()

def delete_device_type(db: Session, type_id: int):
    db_device_type = get_device_type(db, type_id)
    if db_device_type:
        # 检查是否有设备正在使用此设备类型
        devices_using_type = db.query(database.Device).filter(database.Device.device_type_id == type_id).count()
        if devices_using_type > 0:
            return None  # 不能删除正在使用的设备类型
        
        db.delete(db_device_type)
        db.commit()
    return db_device_type

# 设备CRUD操作
def create_device(db: Session, device: models.DeviceCreate):
    # 验证用户存在
    user = get_user(db, device.user_id)
    if not user:
        return None
    
    # 验证设备类型存在
    device_type = get_device_type(db, device.device_type_id)
    if not device_type:
        return None
    
    db_device = database.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_device(db: Session, device_id: int):
    return db.query(database.Device).filter(database.Device.device_id == device_id).first()

def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.Device).offset(skip).limit(limit).all()

def get_user_devices(db: Session, user_id: int):
    return db.query(database.Device).filter(database.Device.user_id == user_id).all()

def update_device(db: Session, device_id: int, device_update: models.DeviceUpdate):
    db_device = get_device(db, device_id)
    if db_device:
        update_data = device_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_device, field, value)
        db.commit()
        db.refresh(db_device)
    return db_device

def delete_device(db: Session, device_id: int):
    db_device = get_device(db, device_id)
    if db_device:
        # 先删除相关的使用记录
        db.query(database.UsageRecord).filter(database.UsageRecord.device_id == device_id).delete()
        
        # 删除相关的安防事件
        db.query(database.SecurityEvent).filter(database.SecurityEvent.device_id == device_id).delete()
        
        # 最后删除设备
        db.delete(db_device)
        db.commit()
    return db_device

# 使用记录CRUD操作
def create_usage_record(db: Session, usage_record: models.UsageRecordCreate):
    db_record = database.UsageRecord(**usage_record.dict())
    if db_record.end_time and db_record.start_time:
        duration = db_record.end_time - db_record.start_time
        db_record.duration_minutes = int(duration.total_seconds() / 60)
        device = get_device(db, db_record.device_id)
        if device:
            hours = duration.total_seconds() / 3600
            db_record.energy_consumed = device.actual_power_consumption * hours / 1000  # 转换为度
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_usage_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.UsageRecord).offset(skip).limit(limit).all()

def get_user_usage_records(db: Session, user_id: int):
    return db.query(database.UsageRecord).filter(database.UsageRecord.user_id == user_id).all()

def get_device_usage_records(db: Session, device_id: int):
    return db.query(database.UsageRecord).filter(database.UsageRecord.device_id == device_id).all()

def delete_usage_record(db: Session, record_id: int):
    db_record = db.query(database.UsageRecord).filter(database.UsageRecord.record_id == record_id).first()
    if db_record:
        db.delete(db_record)
        db.commit()
    return db_record

# 安防事件CRUD操作
def create_security_event(db: Session, security_event: models.SecurityEventCreate):
    db_event = database.SecurityEvent(**security_event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_security_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.SecurityEvent).offset(skip).limit(limit).all()

def get_user_security_events(db: Session, user_id: int):
    return db.query(database.SecurityEvent).filter(database.SecurityEvent.user_id == user_id).all()

def update_security_event(db: Session, event_id: int, event_update: models.SecurityEventUpdate):
    db_event = db.query(database.SecurityEvent).filter(database.SecurityEvent.event_id == event_id).first()
    if db_event:
        update_data = event_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_event, field, value)
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_security_event(db: Session, event_id: int):
    db_event = db.query(database.SecurityEvent).filter(database.SecurityEvent.event_id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event

# 用户反馈CRUD操作
def create_user_feedback(db: Session, feedback: models.UserFeedbackCreate):
    db_feedback = database.UserFeedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_user_feedbacks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.UserFeedback).offset(skip).limit(limit).all()

def get_user_feedback_by_user(db: Session, user_id: int):
    return db.query(database.UserFeedback).filter(database.UserFeedback.user_id == user_id).all()

def update_user_feedback(db: Session, feedback_id: int, feedback_update: models.UserFeedbackUpdate):
    db_feedback = db.query(database.UserFeedback).filter(database.UserFeedback.feedback_id == feedback_id).first()
    if db_feedback:
        update_data = feedback_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_feedback, field, value)
        db.commit()
        db.refresh(db_feedback)
    return db_feedback

def delete_user_feedback(db: Session, feedback_id: int):
    db_feedback = db.query(database.UserFeedback).filter(database.UserFeedback.feedback_id == feedback_id).first()
    if db_feedback:
        db.delete(db_feedback)
        db.commit()
    return db_feedback