from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# 用户相关模型
class UserCreate(BaseModel):
    username: str
    email: str
    phone: Optional[str] = None
    house_area: Optional[float] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    house_area: Optional[float] = None

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    phone: Optional[str]
    house_area: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 设备类型相关模型
class DeviceTypeCreate(BaseModel):
    type_name: str
    description: Optional[str] = None

class DeviceTypeResponse(BaseModel):
    type_id: int
    type_name: str
    description: Optional[str]

    class Config:
        from_attributes = True

# 设备相关模型
class DeviceCreate(BaseModel):
    device_name: str
    device_type_id: int
    user_id: int
    room_location: Optional[str] = None
    power_consumption: Optional[float] = 0.0

class DeviceUpdate(BaseModel):
    device_name: Optional[str] = None
    room_location: Optional[str] = None
    status: Optional[bool] = None
    power_consumption: Optional[float] = None
    last_maintenance: Optional[datetime] = None

class DeviceResponse(BaseModel):
    device_id: int
    device_name: str
    device_type_id: int
    user_id: int
    room_location: Optional[str]
    status: bool
    power_consumption: float
    installation_date: datetime
    last_maintenance: Optional[datetime]

    class Config:
        from_attributes = True

# 使用记录相关模型
class UsageRecordCreate(BaseModel):
    user_id: int
    device_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    operation_type: Optional[str] = None

class UsageRecordResponse(BaseModel):
    record_id: int
    user_id: int
    device_id: int
    start_time: datetime
    end_time: Optional[datetime]
    duration_minutes: Optional[int]
    energy_consumed: float
    operation_type: Optional[str]

    class Config:
        from_attributes = True

# 安防事件相关模型
class SecurityEventCreate(BaseModel):
    user_id: int
    device_id: Optional[int] = None
    event_type: str
    severity_level: Optional[str] = '低'
    description: Optional[str] = None

class SecurityEventUpdate(BaseModel):
    severity_level: Optional[str] = None
    description: Optional[str] = None
    resolved_at: Optional[datetime] = None
    is_resolved: Optional[bool] = None

class SecurityEventResponse(BaseModel):
    event_id: int
    user_id: int
    device_id: Optional[int]
    event_type: str
    severity_level: str
    description: Optional[str]
    occurred_at: datetime
    resolved_at: Optional[datetime]
    is_resolved: bool

    class Config:
        from_attributes = True

# 用户反馈相关模型
class UserFeedbackCreate(BaseModel):
    user_id: int
    feedback_type: Optional[str] = None
    rating: Optional[int] = None
    content: str

class UserFeedbackUpdate(BaseModel):
    is_processed: bool

class UserFeedbackResponse(BaseModel):
    feedback_id: int
    user_id: int
    feedback_type: Optional[str]
    rating: Optional[int]
    content: str
    submitted_at: datetime
    is_processed: bool

    class Config:
        from_attributes = True

# 分析结果模型
class DeviceUsageAnalysis(BaseModel):
    device_name: str
    device_type: str
    total_usage_hours: float
    usage_frequency: int
    avg_session_duration: float
    peak_usage_hours: List[int]

class UserHabitAnalysis(BaseModel):
    user_id: int
    username: str
    frequently_used_together: List[List[str]]
    peak_activity_hours: List[int]
    favorite_devices: List[str]

class HouseAreaAnalysis(BaseModel):
    area_range: str
    avg_devices_count: float
    avg_usage_hours: float
    popular_device_types: List[str] 