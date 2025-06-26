from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uvicorn

import database
import models
import crud
from analytics import SmartHomeAnalytics

# 创建FastAPI应用
app = FastAPI(
    title="智能家居管理系统",
    description="基于FastAPI的智能家居设备管理和数据分析系统",
    version="1.0.0"
)

# 初始化数据库
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    database.init_database()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== 用户管理 API ====================

@app.post("/users/", response_model=models.UserResponse, tags=["用户管理"])
def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
    """创建新用户"""
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[models.UserResponse], tags=["用户管理"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取用户列表"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=models.UserResponse, tags=["用户管理"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """获取指定用户信息"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

@app.put("/users/{user_id}", response_model=models.UserResponse, tags=["用户管理"])
def update_user(user_id: int, user_update: models.UserUpdate, db: Session = Depends(get_db)):
    """更新用户信息"""
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

@app.delete("/users/{user_id}", tags=["用户管理"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """删除用户"""
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "用户删除成功"}

# ==================== 设备类型管理 API ====================

@app.post("/device-types/", response_model=models.DeviceTypeResponse, tags=["设备类型管理"])
def create_device_type(device_type: models.DeviceTypeCreate, db: Session = Depends(get_db)):
    """创建设备类型"""
    return crud.create_device_type(db=db, device_type=device_type)

@app.get("/device-types/", response_model=List[models.DeviceTypeResponse], tags=["设备类型管理"])
def read_device_types(db: Session = Depends(get_db)):
    """获取所有设备类型"""
    return crud.get_device_types(db)

@app.delete("/device-types/{type_id}", tags=["设备类型管理"])
def delete_device_type(type_id: int, db: Session = Depends(get_db)):
    """删除设备类型"""
    # 先检查设备类型是否存在
    device_type = crud.get_device_type(db, type_id)
    if not device_type:
        raise HTTPException(status_code=404, detail="设备类型不存在")
    
    # 尝试删除
    db_device_type = crud.delete_device_type(db, type_id=type_id)
    if db_device_type is None:
        raise HTTPException(status_code=400, detail="无法删除：该设备类型正被设备使用")
    return {"message": "设备类型删除成功"}

# ==================== 设备管理 API ====================

@app.post("/devices/", response_model=models.DeviceResponse, tags=["设备管理"])
def create_device(device: models.DeviceCreate, db: Session = Depends(get_db)):
    """创建新设备"""
    # 验证用户存在
    user = crud.get_user(db, device.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 验证设备类型存在
    device_type = crud.get_device_type(db, device.device_type_id)
    if not device_type:
        raise HTTPException(status_code=404, detail="设备类型不存在")
    
    return crud.create_device(db=db, device=device)

@app.get("/devices/", response_model=List[models.DeviceResponse], tags=["设备管理"])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取设备列表"""
    devices = crud.get_devices(db, skip=skip, limit=limit)
    return devices

@app.get("/devices/{device_id}", response_model=models.DeviceResponse, tags=["设备管理"])
def read_device(device_id: int, db: Session = Depends(get_db)):
    """获取指定设备信息"""
    db_device = crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="设备不存在")
    return db_device

@app.get("/users/{user_id}/devices", response_model=List[models.DeviceResponse], tags=["设备管理"])
def read_user_devices(user_id: int, db: Session = Depends(get_db)):
    """获取用户的所有设备"""
    return crud.get_user_devices(db, user_id=user_id)

@app.put("/devices/{device_id}", response_model=models.DeviceResponse, tags=["设备管理"])
def update_device(device_id: int, device_update: models.DeviceUpdate, db: Session = Depends(get_db)):
    """更新设备信息"""
    db_device = crud.update_device(db, device_id=device_id, device_update=device_update)
    if db_device is None:
        raise HTTPException(status_code=404, detail="设备不存在")
    return db_device

@app.delete("/devices/{device_id}", tags=["设备管理"])
def delete_device(device_id: int, db: Session = Depends(get_db)):
    """删除设备"""
    db_device = crud.delete_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="设备不存在")
    return {"message": "设备删除成功"}

# ==================== 使用记录管理 API ====================

@app.post("/usage-records/", response_model=models.UsageRecordResponse, tags=["使用记录管理"])
def create_usage_record(usage_record: models.UsageRecordCreate, db: Session = Depends(get_db)):
    """创建使用记录"""
    return crud.create_usage_record(db=db, usage_record=usage_record)

@app.get("/usage-records/", response_model=List[models.UsageRecordResponse], tags=["使用记录管理"])
def read_usage_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取使用记录列表"""
    return crud.get_usage_records(db, skip=skip, limit=limit)

@app.get("/users/{user_id}/usage-records", response_model=List[models.UsageRecordResponse], tags=["使用记录管理"])
def read_user_usage_records(user_id: int, db: Session = Depends(get_db)):
    """获取用户的使用记录"""
    return crud.get_user_usage_records(db, user_id=user_id)

@app.get("/devices/{device_id}/usage-records", response_model=List[models.UsageRecordResponse], tags=["使用记录管理"])
def read_device_usage_records(device_id: int, db: Session = Depends(get_db)):
    """获取设备的使用记录"""
    return crud.get_device_usage_records(db, device_id=device_id)

@app.delete("/usage-records/{record_id}", tags=["使用记录管理"])
def delete_usage_record(record_id: int, db: Session = Depends(get_db)):
    """删除使用记录"""
    db_record = crud.delete_usage_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="使用记录不存在")
    return {"message": "使用记录删除成功"}

# ==================== 安防事件管理 API ====================

@app.post("/security-events/", response_model=models.SecurityEventResponse, tags=["安防事件管理"])
def create_security_event(security_event: models.SecurityEventCreate, db: Session = Depends(get_db)):
    """创建安防事件"""
    return crud.create_security_event(db=db, security_event=security_event)

@app.get("/security-events/", response_model=List[models.SecurityEventResponse], tags=["安防事件管理"])
def read_security_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取安防事件列表"""
    return crud.get_security_events(db, skip=skip, limit=limit)

@app.get("/users/{user_id}/security-events", response_model=List[models.SecurityEventResponse], tags=["安防事件管理"])
def read_user_security_events(user_id: int, db: Session = Depends(get_db)):
    """获取用户的安防事件"""
    return crud.get_user_security_events(db, user_id=user_id)

@app.put("/security-events/{event_id}", response_model=models.SecurityEventResponse, tags=["安防事件管理"])
def update_security_event(event_id: int, event_update: models.SecurityEventUpdate, db: Session = Depends(get_db)):
    """更新安防事件"""
    db_event = crud.update_security_event(db, event_id=event_id, event_update=event_update)
    if db_event is None:
        raise HTTPException(status_code=404, detail="安防事件不存在")
    return db_event

@app.delete("/security-events/{event_id}", tags=["安防事件管理"])
def delete_security_event(event_id: int, db: Session = Depends(get_db)):
    """删除安防事件"""
    db_event = crud.delete_security_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="安防事件不存在")
    return {"message": "安防事件删除成功"}

# ==================== 用户反馈管理 API ====================

@app.post("/user-feedbacks/", response_model=models.UserFeedbackResponse, tags=["用户反馈管理"])
def create_user_feedback(feedback: models.UserFeedbackCreate, db: Session = Depends(get_db)):
    """创建用户反馈"""
    return crud.create_user_feedback(db=db, feedback=feedback)

@app.get("/user-feedbacks/", response_model=List[models.UserFeedbackResponse], tags=["用户反馈管理"])
def read_user_feedbacks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取用户反馈列表"""
    return crud.get_user_feedbacks(db, skip=skip, limit=limit)

@app.get("/users/{user_id}/feedbacks", response_model=List[models.UserFeedbackResponse], tags=["用户反馈管理"])
def read_user_feedback_by_user(user_id: int, db: Session = Depends(get_db)):
    """获取用户的反馈"""
    return crud.get_user_feedback_by_user(db, user_id=user_id)

@app.put("/user-feedbacks/{feedback_id}", response_model=models.UserFeedbackResponse, tags=["用户反馈管理"])
def update_user_feedback(feedback_id: int, feedback_update: models.UserFeedbackUpdate, db: Session = Depends(get_db)):
    """处理用户反馈"""
    db_feedback = crud.update_user_feedback(db, feedback_id=feedback_id, feedback_update=feedback_update)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="用户反馈不存在")
    return db_feedback

@app.delete("/user-feedbacks/{feedback_id}", tags=["用户反馈管理"])
def delete_user_feedback(feedback_id: int, db: Session = Depends(get_db)):
    """删除用户反馈"""
    db_feedback = crud.delete_user_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="用户反馈不存在")
    return {"message": "用户反馈删除成功"}

# ==================== 数据分析 API ====================

@app.get("/analytics/device-usage", response_model=List[models.DeviceUsageAnalysis], tags=["数据分析"])
def analyze_device_usage(db: Session = Depends(get_db)):
    """分析设备使用频率和使用时间段"""
    analytics = SmartHomeAnalytics(db)
    return analytics.analyze_device_usage_frequency()

@app.get("/analytics/user-habits", response_model=List[models.UserHabitAnalysis], tags=["数据分析"])
def analyze_user_habits(db: Session = Depends(get_db)):
    """分析用户使用习惯"""
    analytics = SmartHomeAnalytics(db)
    return analytics.analyze_user_habits()

@app.get("/analytics/house-area-impact", response_model=List[models.HouseAreaAnalysis], tags=["数据分析"])
def analyze_house_area_impact(db: Session = Depends(get_db)):
    """分析房屋面积对设备使用行为的影响"""
    analytics = SmartHomeAnalytics(db)
    return analytics.analyze_house_area_impact()

@app.get("/analytics/energy-consumption", tags=["数据分析"])
def get_energy_consumption_report(db: Session = Depends(get_db)):
    """获取能耗分析报告"""
    analytics = SmartHomeAnalytics(db)
    return analytics.generate_energy_consumption_report()



# ==================== 系统信息 API ====================

@app.get("/", tags=["系统信息"])
def read_root():
    """系统欢迎页面"""
    return {
        "message": "欢迎使用智能家居管理系统",
        "version": "1.0.0",
        "api_endpoints": {
            "用户管理": "/users/",
            "设备管理": "/devices/",
            "使用记录": "/usage-records/",
            "安防事件": "/security-events/",
            "用户反馈": "/user-feedbacks/",
            "数据分析": "/analytics/"
        }
    }

@app.get("/health", tags=["系统信息"])
def health_check():
    return {"status": "healthy", "message": "系统运行正常"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    ) 