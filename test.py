"""
智能家居管理系统 - API 接口完整测试脚本
运行此脚本将测试所有API接口并输出结果
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List

# API基础配置
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

class APITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS
        self.test_results = []
        
        # 存储测试过程中创建的资源ID
        self.test_user_ids = []
        self.test_device_type_ids = []
        self.test_device_ids = []
        self.test_usage_record_ids = []
        self.test_security_event_ids = []
        self.test_feedback_ids = []
    
    def log_test(self, test_name: str, method: str, endpoint: str, status_code: int, 
                 response_data: Any = None, error: str = None):
        """记录测试结果"""
        result = {
            "test_name": test_name,
            "method": method,
            "endpoint": endpoint,
            "status_code": status_code,
            "success": 200 <= status_code < 300,
            "response_data": response_data,
            "error": error,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        
        # 控制台输出
        status = "  PASS" if result["success"] else "   FAIL"
        print(f"{status} | {method} | {endpoint} | {test_name}")
        
        if error:
            print(f"     Error: {error}")
        elif response_data:
            if isinstance(response_data, dict):
                if "message" in response_data:
                    print(f"     Response: {response_data['message']}")
                elif "user_id" in response_data:
                    print(f"     Created User ID: {response_data['user_id']}")
                elif "device_id" in response_data:
                    print(f"     Created Device ID: {response_data['device_id']}")
                elif "type_id" in response_data:
                    print(f"     Created Device Type ID: {response_data['type_id']}")
                elif "record_id" in response_data:
                    print(f"     Created Usage Record ID: {response_data['record_id']}")
                elif "event_id" in response_data:
                    print(f"     Created Security Event ID: {response_data['event_id']}")
                elif "feedback_id" in response_data:
                    print(f"     Created Feedback ID: {response_data['feedback_id']}")
                elif "count" in response_data:
                    print(f"     Result: {response_data['count']} items")
                elif "html_length" in response_data:
                    print(f"     HTML Response: {response_data['html_length']} characters")
                else:
                    # 对于GET请求，打印完整的数据
                    if method.upper() == "GET":
                        print(f"     Data: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                    else:
                        print(f"     Response: {response_data}")
            elif isinstance(response_data, list):
                print(f"     Data (总数: {len(response_data)}):")
                for i, item in enumerate(response_data[:3]):  # 只显示前3个项目
                    print(f"       [{i+1}] {json.dumps(item, ensure_ascii=False)}")
                if len(response_data) > 3:
                    print(f"       ... 还有 {len(response_data) - 3} 个项目")
            else:
                print(f"     Data: {response_data}")
        print()
    
    def make_request(self, method: str, endpoint: str, data: Dict = None) -> requests.Response:
        """发送HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=self.headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            return response
        except requests.exceptions.RequestException as e:
            # 创建一个模拟的失败响应
            class FailedResponse:
                def __init__(self, error):
                    self.status_code = 0
                    self.text = str(error)
                
                def json(self):
                    return {"error": str(error)}
            
            return FailedResponse(e)
    
    def test_system_info(self):
        """测试系统信息接口"""
        print("=" * 50)
        print("测试系统信息接口")
        print("=" * 50)
        
        # 测试根路径
        response = self.make_request("GET", "/")
        try:
            data = response.json()
            self.log_test("系统欢迎页面", "GET", "/", response.status_code, data)
        except:
            self.log_test("系统欢迎页面", "GET", "/", response.status_code, 
                         error=f"Response: {response.text}")
        
        # 测试健康检查
        response = self.make_request("GET", "/health")
        try:
            data = response.json()
            self.log_test("健康检查", "GET", "/health", response.status_code, data)
        except:
            self.log_test("健康检查", "GET", "/health", response.status_code,
                         error=f"Response: {response.text}")
    
    def test_user_management(self):
        """测试用户管理接口"""
        print("=" * 50)
        print("测试用户管理接口")
        print("=" * 50)
        
        # 0. 首先执行删除测试 - 获取现有用户列表找一个来删除
        response = self.make_request("GET", "/users/")
        existing_users = []
        try:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                existing_users = data
                self.log_test("获取用户列表（删除测试准备）", "GET", "/users/", response.status_code, data)
        except:
            self.log_test("获取用户列表（删除测试准备）", "GET", "/users/", response.status_code,
                         error=f"Response: {response.text}")
        
        # 删除测试：创建一个临时用户用于删除测试
        temp_user_data = {
            "username": "临时删除测试用户",
            "email": "temp_delete@test.com",
            "phone": "19900000001",
            "house_area": 50.0
        }
        response = self.make_request("POST", "/users/", temp_user_data)
        temp_user_id = None
        try:
            data = response.json()
            if response.status_code == 201 or response.status_code == 200:
                temp_user_id = data.get("user_id")
                self.log_test("创建临时用户（删除测试）", "POST", "/users/", response.status_code, data)
        except:
            self.log_test("创建临时用户（删除测试）", "POST", "/users/", 
                         response.status_code, error=f"Response: {response.text}")
        
        # 执行删除测试
        if temp_user_id:
            response = self.make_request("DELETE", f"/users/{temp_user_id}")
            try:
                data = response.json() if response.text else {"message": "删除成功"}
                self.log_test(f"删除用户测试 - ID:{temp_user_id}", "DELETE", f"/users/{temp_user_id}",
                             response.status_code, data)
            except:
                self.log_test(f"删除用户测试 - ID:{temp_user_id}", "DELETE", f"/users/{temp_user_id}",
                             response.status_code, error=f"Response: {response.text}")
        
        # 1. 创建用户
        test_users = [
            {
                "username": "测试用户1",
                "email": "test1@example.com",
                "phone": "13900000001",
                "house_area": 88.5
            },
            {
                "username": "测试用户2", 
                "email": "test2@example.com",
                "phone": "13900000002",
                "house_area": 120.0
            }
        ]
        
        for user_data in test_users:
            response = self.make_request("POST", "/users/", user_data)
            try:
                data = response.json()
                if response.status_code == 201 or response.status_code == 200:
                    self.test_user_ids.append(data.get("user_id"))
                self.log_test(f"创建用户 - {user_data['username']}", "POST", "/users/", 
                             response.status_code, data)
            except:
                self.log_test(f"创建用户 - {user_data['username']}", "POST", "/users/",
                             response.status_code, error=f"Response: {response.text}")
        
        # 2. 获取用户列表
        response = self.make_request("GET", "/users/")
        try:
            data = response.json()
            self.log_test("获取用户列表", "GET", "/users/", response.status_code, data)
        except:
            self.log_test("获取用户列表", "GET", "/users/", response.status_code,
                         error=f"Response: {response.text}")
        
        # 3. 获取单个用户
        if self.test_user_ids:
            user_id = self.test_user_ids[0]
            response = self.make_request("GET", f"/users/{user_id}")
            try:
                data = response.json()
                self.log_test(f"获取用户详情 - ID:{user_id}", "GET", f"/users/{user_id}",
                             response.status_code, data)
            except:
                self.log_test(f"获取用户详情 - ID:{user_id}", "GET", f"/users/{user_id}",
                             response.status_code, error=f"Response: {response.text}")
        
        # 4. 更新用户
        if self.test_user_ids:
            user_id = self.test_user_ids[0]
            update_data = {"house_area": 95.0, "phone": "13900000099"}
            response = self.make_request("PUT", f"/users/{user_id}", update_data)
            try:
                data = response.json()
                self.log_test(f"更新用户 - ID:{user_id}", "PUT", f"/users/{user_id}",
                             response.status_code, data)
            except:
                self.log_test(f"更新用户 - ID:{user_id}", "PUT", f"/users/{user_id}",
                             response.status_code, error=f"Response: {response.text}")
    
    def test_device_type_management(self):
        """测试设备类型管理接口"""
        print("=" * 50)
        print("测试设备类型管理接口")
        print("=" * 50)
        
        # 0. 首先执行删除测试 - 创建一个临时设备类型来测试删除
        temp_device_type_data = {
            "type_name": f"临时测试设备类型_{int(time.time())}",  # 使用时间戳确保唯一性
            "description": "用于删除测试的临时设备类型"
        }
        response = self.make_request("POST", "/device-types/", temp_device_type_data)
        temp_type_id = None
        try:
            data = response.json()
            if response.status_code == 201 or response.status_code == 200:
                temp_type_id = data.get("type_id")
                self.log_test("创建临时设备类型（删除测试）", "POST", "/device-types/",
                             response.status_code, data)
        except:
            self.log_test("创建临时设备类型（删除测试）", "POST", "/device-types/",
                         response.status_code, error=f"Response: {response.text}")
        
        # 删除临时设备类型
        if temp_type_id:
            response = self.make_request("DELETE", f"/device-types/{temp_type_id}")
            try:
                data = response.json() if response.text else {"message": "删除成功"}
                self.log_test(f"删除设备类型测试 - ID:{temp_type_id}", "DELETE", f"/device-types/{temp_type_id}",
                             response.status_code, data)
            except:
                self.log_test(f"删除设备类型测试 - ID:{temp_type_id}", "DELETE", f"/device-types/{temp_type_id}",
                             response.status_code, error=f"Response: {response.text}")
        
        # 1. 创建设备类型（使用时间戳确保唯一性）
        timestamp = int(time.time())
        test_device_types = [
            {
                "type_name": f"测试智能灯_{timestamp}",
                "description": "用于测试的智能灯设备"
            },
            {
                "type_name": f"测试智能开关_{timestamp}",
                "description": "用于测试的智能开关设备"
            }
        ]
        
        for device_type_data in test_device_types:
            response = self.make_request("POST", "/device-types/", device_type_data)
            try:
                data = response.json()
                if response.status_code == 201 or response.status_code == 200:
                    self.test_device_type_ids.append(data.get("type_id"))
                self.log_test(f"创建设备类型 - {device_type_data['type_name']}", "POST", 
                             "/device-types/", response.status_code, data)
            except:
                self.log_test(f"创建设备类型 - {device_type_data['type_name']}", "POST",
                             "/device-types/", response.status_code, 
                             error=f"Response: {response.text}")
        
        # 2. 获取设备类型列表
        response = self.make_request("GET", "/device-types/")
        try:
            data = response.json()
            self.log_test("获取设备类型列表", "GET", "/device-types/", response.status_code, data)
        except:
            self.log_test("获取设备类型列表", "GET", "/device-types/", response.status_code,
                         error=f"Response: {response.text}")
    
    def test_device_management(self):
        """测试设备管理接口"""
        print("=" * 50)
        print("📱 测试设备管理接口")
        print("=" * 50)
        
        if not self.test_user_ids or not self.test_device_type_ids:
            print("跳过设备管理测试 - 缺少必要的用户或设备类型数据")
            return
        
        # 0. 首先执行删除测试 - 创建一个临时设备来测试删除
        temp_device_data = {
            "device_name": f"临时删除测试设备_{int(time.time())}",
            "device_type_id": self.test_device_type_ids[0],
            "user_id": self.test_user_ids[0],
            "room_location": "临时房间",
            "power_consumption": 10.0
        }
        response = self.make_request("POST", "/devices/", temp_device_data)
        temp_device_id = None
        try:
            data = response.json()
            if response.status_code == 201 or response.status_code == 200:
                temp_device_id = data.get("device_id")
                self.log_test("创建临时设备（删除测试）", "POST", "/devices/",
                             response.status_code, data)
        except:
            self.log_test("创建临时设备（删除测试）", "POST", "/devices/",
                         response.status_code, error=f"Response: {response.text}")
        
        # 删除临时设备
        if temp_device_id:
            response = self.make_request("DELETE", f"/devices/{temp_device_id}")
            try:
                data = response.json() if response.text else {"message": "删除成功"}
                self.log_test(f"删除设备测试 - ID:{temp_device_id}", "DELETE", f"/devices/{temp_device_id}",
                             response.status_code, data)
            except:
                self.log_test(f"删除设备测试 - ID:{temp_device_id}", "DELETE", f"/devices/{temp_device_id}",
                             response.status_code, error=f"Response: {response.text}")
        
        # 1. 创建设备
        test_devices = [
            {
                "device_name": "测试客厅灯",
                "device_type_id": self.test_device_type_ids[0],
                "user_id": self.test_user_ids[0],
                "room_location": "客厅",
                "power_consumption": 15.0
            },
            {
                "device_name": "测试卧室开关",
                "device_type_id": self.test_device_type_ids[-1] if len(self.test_device_type_ids) > 1 else self.test_device_type_ids[0],
                "user_id": self.test_user_ids[-1] if len(self.test_user_ids) > 1 else self.test_user_ids[0],
                "room_location": "卧室",
                "power_consumption": 5.0
            }
        ]
        
        for device_data in test_devices:
            response = self.make_request("POST", "/devices/", device_data)
            try:
                data = response.json()
                if response.status_code == 201 or response.status_code == 200:
                    self.test_device_ids.append(data.get("device_id"))
                self.log_test(f"创建设备 - {device_data['device_name']}", "POST", "/devices/",
                             response.status_code, data)
            except:
                self.log_test(f"创建设备 - {device_data['device_name']}", "POST", "/devices/",
                             response.status_code, error=f"Response: {response.text}")
        
        # 2. 获取设备列表
        response = self.make_request("GET", "/devices/")
        try:
            data = response.json()
            self.log_test("获取设备列表", "GET", "/devices/", response.status_code, data)
        except:
            self.log_test("获取设备列表", "GET", "/devices/", response.status_code,
                         error=f"Response: {response.text}")
        
        # 3. 获取单个设备
        if self.test_device_ids:
            device_id = self.test_device_ids[0]
            response = self.make_request("GET", f"/devices/{device_id}")
            try:
                data = response.json()
                self.log_test(f"获取设备详情 - ID:{device_id}", "GET", f"/devices/{device_id}",
                             response.status_code, data)
            except:
                self.log_test(f"获取设备详情 - ID:{device_id}", "GET", f"/devices/{device_id}",
                             response.status_code, error=f"Response: {response.text}")
        
        # 4. 获取用户的设备
        if self.test_user_ids:
            user_id = self.test_user_ids[0]
            response = self.make_request("GET", f"/users/{user_id}/devices")
            try:
                data = response.json()
                self.log_test(f"获取用户设备 - 用户ID:{user_id}", "GET", f"/users/{user_id}/devices",
                             response.status_code, data)
            except:
                self.log_test(f"获取用户设备 - 用户ID:{user_id}", "GET", f"/users/{user_id}/devices",
                             response.status_code, error=f"Response: {response.text}")
        
        # 5. 更新设备
        if self.test_device_ids:
            device_id = self.test_device_ids[0]
            update_data = {"status": True, "power_consumption": 20.0}
            response = self.make_request("PUT", f"/devices/{device_id}", update_data)
            try:
                data = response.json()
                self.log_test(f"更新设备 - ID:{device_id}", "PUT", f"/devices/{device_id}",
                             response.status_code, data)
            except:
                self.log_test(f"更新设备 - ID:{device_id}", "PUT", f"/devices/{device_id}",
                             response.status_code, error=f"Response: {response.text}")
        

    
    def test_usage_records(self):
        """测试使用记录管理接口"""
        print("=" * 50)
        print("测试使用记录管理接口")
        print("=" * 50)
        
        if not self.test_user_ids or not self.test_device_ids:
            print("跳过使用记录测试 - 缺少必要的用户或设备数据")
            return
        
        # 0. 首先执行删除测试 - 创建一个临时使用记录来测试删除
        temp_usage_data = {
            "user_id": self.test_user_ids[0],
            "device_id": self.test_device_ids[0],
            "start_time": (datetime.now() - timedelta(minutes=10)).isoformat(),
            "end_time": (datetime.now() - timedelta(minutes=5)).isoformat(),
            "operation_type": f"临时删除测试_{int(time.time())}"
        }
        response = self.make_request("POST", "/usage-records/", temp_usage_data)
        temp_record_id = None
        try:
            data = response.json()
            if response.status_code == 201 or response.status_code == 200:
                temp_record_id = data.get("record_id")
                self.log_test("创建临时使用记录（删除测试）", "POST", "/usage-records/",
                             response.status_code, data)
        except:
            self.log_test("创建临时使用记录（删除测试）", "POST", "/usage-records/",
                         response.status_code, error=f"Response: {response.text}")
        
        # 删除临时使用记录
        if temp_record_id:
            response = self.make_request("DELETE", f"/usage-records/{temp_record_id}")
            try:
                data = response.json() if response.text else {"message": "删除成功"}
                self.log_test(f"删除使用记录测试 - ID:{temp_record_id}", "DELETE", f"/usage-records/{temp_record_id}",
                             response.status_code, data)
            except:
                self.log_test(f"删除使用记录测试 - ID:{temp_record_id}", "DELETE", f"/usage-records/{temp_record_id}",
                             response.status_code, error=f"Response: {response.text}")
        
        # 1. 创建使用记录
        now = datetime.now()
        test_usage_records = [
            {
                "user_id": self.test_user_ids[0],
                "device_id": self.test_device_ids[0],
                "start_time": (now - timedelta(hours=2)).isoformat(),
                "end_time": (now - timedelta(hours=1)).isoformat(),
                "operation_type": "开机"
            },
            {
                "user_id": self.test_user_ids[0],
                "device_id": self.test_device_ids[0],
                "start_time": (now - timedelta(minutes=30)).isoformat(),
                "operation_type": "调节"
            }
        ]
        
        for usage_data in test_usage_records:
            response = self.make_request("POST", "/usage-records/", usage_data)
            try:
                data = response.json()
                if response.status_code == 201 or response.status_code == 200:
                    self.test_usage_record_ids.append(data.get("record_id"))
                self.log_test(f"创建使用记录 - {usage_data['operation_type']}", "POST", 
                             "/usage-records/", response.status_code, data)
            except:
                self.log_test(f"创建使用记录 - {usage_data['operation_type']}", "POST",
                             "/usage-records/", response.status_code, 
                             error=f"Response: {response.text}")
        
        # 2. 获取使用记录列表
        response = self.make_request("GET", "/usage-records/")
        try:
            data = response.json()
            self.log_test("获取使用记录列表", "GET", "/usage-records/", response.status_code, data)
        except:
            self.log_test("获取使用记录列表", "GET", "/usage-records/", response.status_code,
                         error=f"Response: {response.text}")
        
        # 3. 获取用户的使用记录
        if self.test_user_ids:
            user_id = self.test_user_ids[0]
            response = self.make_request("GET", f"/users/{user_id}/usage-records")
            try:
                data = response.json()
                self.log_test(f"获取用户使用记录 - 用户ID:{user_id}", "GET", 
                             f"/users/{user_id}/usage-records", response.status_code, data)
            except:
                self.log_test(f"获取用户使用记录 - 用户ID:{user_id}", "GET",
                             f"/users/{user_id}/usage-records", response.status_code,
                             error=f"Response: {response.text}")
        
        # 4. 获取设备的使用记录
        if self.test_device_ids:
            device_id = self.test_device_ids[0]
            response = self.make_request("GET", f"/devices/{device_id}/usage-records")
            try:
                data = response.json()
                self.log_test(f"获取设备使用记录 - 设备ID:{device_id}", "GET",
                             f"/devices/{device_id}/usage-records", response.status_code, data)
            except:
                self.log_test(f"获取设备使用记录 - 设备ID:{device_id}", "GET",
                             f"/devices/{device_id}/usage-records", response.status_code,
                             error=f"Response: {response.text}")
        

    
    def test_security_events(self):
        """测试安防事件管理接口"""
        print("=" * 50)
        print("测试安防事件管理接口")
        print("=" * 50)
        
        if not self.test_user_ids:
            print("跳过安防事件测试 - 缺少必要的用户数据")
            return
        
        # 0. 首先执行删除测试 - 创建一个临时安防事件来测试删除
        temp_event_data = {
            "user_id": self.test_user_ids[0],
            "event_type": f"临时删除测试事件_{int(time.time())}",
            "severity_level": "低",
            "description": "用于删除测试的临时安防事件"
        }
        response = self.make_request("POST", "/security-events/", temp_event_data)
        temp_event_id = None
        try:
            data = response.json()
            if response.status_code == 201 or response.status_code == 200:
                temp_event_id = data.get("event_id")
                self.log_test("创建临时安防事件（删除测试）", "POST", "/security-events/",
                             response.status_code, data)
        except:
            self.log_test("创建临时安防事件（删除测试）", "POST", "/security-events/",
                         response.status_code, error=f"Response: {response.text}")
        
        # 删除临时安防事件
        if temp_event_id:
            response = self.make_request("DELETE", f"/security-events/{temp_event_id}")
            try:
                data = response.json() if response.text else {"message": "删除成功"}
                self.log_test(f"删除安防事件测试 - ID:{temp_event_id}", "DELETE", f"/security-events/{temp_event_id}",
                             response.status_code, data)
            except:
                self.log_test(f"删除安防事件测试 - ID:{temp_event_id}", "DELETE", f"/security-events/{temp_event_id}",
                             response.status_code, error=f"Response: {response.text}")
        
        # 1. 创建安防事件
        test_security_events = [
            {
                "user_id": self.test_user_ids[0],
                "device_id": self.test_device_ids[0] if self.test_device_ids else None,
                "event_type": "测试入侵检测",
                "severity_level": "中",
                "description": "这是一个测试安防事件"
            },
            {
                "user_id": self.test_user_ids[0],
                "event_type": "测试门锁异常",
                "severity_level": "高",
                "description": "测试门锁异常事件"
            }
        ]
        
        for event_data in test_security_events:
            response = self.make_request("POST", "/security-events/", event_data)
            try:
                data = response.json()
                if response.status_code == 201 or response.status_code == 200:
                    self.test_security_event_ids.append(data.get("event_id"))
                self.log_test(f"创建安防事件 - {event_data['event_type']}", "POST", 
                             "/security-events/", response.status_code, data)
            except:
                self.log_test(f"创建安防事件 - {event_data['event_type']}", "POST",
                             "/security-events/", response.status_code,
                             error=f"Response: {response.text}")
        
        # 2. 获取安防事件列表
        response = self.make_request("GET", "/security-events/")
        try:
            data = response.json()
            self.log_test("获取安防事件列表", "GET", "/security-events/", response.status_code, data)
        except:
            self.log_test("获取安防事件列表", "GET", "/security-events/", response.status_code,
                         error=f"Response: {response.text}")
        
        # 3. 获取用户的安防事件
        if self.test_user_ids:
            user_id = self.test_user_ids[0]
            response = self.make_request("GET", f"/users/{user_id}/security-events")
            try:
                data = response.json()
                self.log_test(f"获取用户安防事件 - 用户ID:{user_id}", "GET",
                             f"/users/{user_id}/security-events", response.status_code, data)
            except:
                self.log_test(f"获取用户安防事件 - 用户ID:{user_id}", "GET",
                             f"/users/{user_id}/security-events", response.status_code,
                             error=f"Response: {response.text}")
        
        # 4. 更新安防事件
        if self.test_security_event_ids:
            event_id = self.test_security_event_ids[0]
            update_data = {"is_resolved": True, "resolved_at": datetime.now().isoformat()}
            response = self.make_request("PUT", f"/security-events/{event_id}", update_data)
            try:
                data = response.json()
                self.log_test(f"更新安防事件 - ID:{event_id}", "PUT", 
                             f"/security-events/{event_id}", response.status_code, data)
            except:
                self.log_test(f"更新安防事件 - ID:{event_id}", "PUT",
                             f"/security-events/{event_id}", response.status_code,
                             error=f"Response: {response.text}")
        

    
    def test_user_feedbacks(self):
        """测试用户反馈管理接口"""
        print("=" * 50)
        print("测试用户反馈管理接口")
        print("=" * 50)
        
        if not self.test_user_ids:
            print("跳过用户反馈测试 - 缺少必要的用户数据")
            return
        
        # 0. 首先执行删除测试 - 创建一个临时反馈来测试删除
        temp_feedback_data = {
            "user_id": self.test_user_ids[0],
            "feedback_type": f"临时删除测试_{int(time.time())}",
            "rating": 3,
            "content": "用于删除测试的临时用户反馈"
        }
        response = self.make_request("POST", "/user-feedbacks/", temp_feedback_data)
        temp_feedback_id = None
        try:
            data = response.json()
            if response.status_code == 201 or response.status_code == 200:
                temp_feedback_id = data.get("feedback_id")
                self.log_test("创建临时用户反馈（删除测试）", "POST", "/user-feedbacks/",
                             response.status_code, data)
        except:
            self.log_test("创建临时用户反馈（删除测试）", "POST", "/user-feedbacks/",
                         response.status_code, error=f"Response: {response.text}")
        
        # 删除临时用户反馈
        if temp_feedback_id:
            response = self.make_request("DELETE", f"/user-feedbacks/{temp_feedback_id}")
            try:
                data = response.json() if response.text else {"message": "删除成功"}
                self.log_test(f"删除用户反馈测试 - ID:{temp_feedback_id}", "DELETE", f"/user-feedbacks/{temp_feedback_id}",
                             response.status_code, data)
            except:
                self.log_test(f"删除用户反馈测试 - ID:{temp_feedback_id}", "DELETE", f"/user-feedbacks/{temp_feedback_id}",
                             response.status_code, error=f"Response: {response.text}")
        
        # 1. 创建用户反馈
        test_feedbacks = [
            {
                "user_id": self.test_user_ids[0],
                "feedback_type": "功能建议",
                "rating": 4,
                "content": "这是一个测试反馈，建议增加更多功能"
            },
            {
                "user_id": self.test_user_ids[0],
                "feedback_type": "使用体验",
                "rating": 5,
                "content": "测试系统使用体验很好"
            }
        ]
        
        for feedback_data in test_feedbacks:
            response = self.make_request("POST", "/user-feedbacks/", feedback_data)
            try:
                data = response.json()
                if response.status_code == 201 or response.status_code == 200:
                    self.test_feedback_ids.append(data.get("feedback_id"))
                self.log_test(f"创建用户反馈 - {feedback_data['feedback_type']}", "POST",
                             "/user-feedbacks/", response.status_code, data)
            except:
                self.log_test(f"创建用户反馈 - {feedback_data['feedback_type']}", "POST",
                             "/user-feedbacks/", response.status_code,
                             error=f"Response: {response.text}")
        
        # 2. 获取用户反馈列表
        response = self.make_request("GET", "/user-feedbacks/")
        try:
            data = response.json()
            self.log_test("获取用户反馈列表", "GET", "/user-feedbacks/", response.status_code, data)
        except:
            self.log_test("获取用户反馈列表", "GET", "/user-feedbacks/", response.status_code,
                         error=f"Response: {response.text}")
        
        # 3. 获取用户的反馈
        if self.test_user_ids:
            user_id = self.test_user_ids[0]
            response = self.make_request("GET", f"/users/{user_id}/feedbacks")
            try:
                data = response.json()
                self.log_test(f"获取用户反馈 - 用户ID:{user_id}", "GET",
                             f"/users/{user_id}/feedbacks", response.status_code, data)
            except:
                self.log_test(f"获取用户反馈 - 用户ID:{user_id}", "GET",
                             f"/users/{user_id}/feedbacks", response.status_code,
                             error=f"Response: {response.text}")
        
        # 4. 更新用户反馈
        if self.test_feedback_ids:
            feedback_id = self.test_feedback_ids[0]
            update_data = {"is_processed": True}
            response = self.make_request("PUT", f"/user-feedbacks/{feedback_id}", update_data)
            try:
                data = response.json()
                self.log_test(f"更新用户反馈 - ID:{feedback_id}", "PUT",
                             f"/user-feedbacks/{feedback_id}", response.status_code, data)
            except:
                self.log_test(f"更新用户反馈 - ID:{feedback_id}", "PUT",
                             f"/user-feedbacks/{feedback_id}", response.status_code,
                             error=f"Response: {response.text}")
        

    
    def test_analytics(self):
        """测试数据分析接口"""
        print("=" * 50)
        print("测试数据分析接口")
        print("=" * 50)
        
        analytics_endpoints = [
            ("/analytics/device-usage", "设备使用频率分析"),
            ("/analytics/user-habits", "用户使用习惯分析"),
            ("/analytics/house-area-impact", "房屋面积影响分析"),
            ("/analytics/energy-consumption", "能耗分析报告")
        ]
        
        for endpoint, description in analytics_endpoints:
            response = self.make_request("GET", endpoint)
            try:
                data = response.json()
                self.log_test(description, "GET", endpoint, response.status_code, data)
            except:
                self.log_test(description, "GET", endpoint, response.status_code,
                             error=f"Response: {response.text[:200]}...")
    

    
    def cleanup_test_data(self):
        """清理测试数据"""
        print("=" * 50)
        print("清理测试数据")
        print("=" * 50)
        
        # 删除测试设备（按逆序删除，避免外键约束问题）
        for device_id in reversed(self.test_device_ids):
            response = self.make_request("DELETE", f"/devices/{device_id}")
            self.log_test(f"删除测试设备 - ID:{device_id}", "DELETE", f"/devices/{device_id}",
                         response.status_code)
        
        # 删除测试用户
        for user_id in reversed(self.test_user_ids):
            response = self.make_request("DELETE", f"/users/{user_id}")
            self.log_test(f"删除测试用户 - ID:{user_id}", "DELETE", f"/users/{user_id}",
                         response.status_code)
    
    def print_summary(self):
        """打印测试总结"""
        print("=" * 50)
        print("测试总结")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests}  ")
        print(f"失败: {failed_tests}   ")
        print(f"成功率: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "成功率: 0%")
        
        if failed_tests > 0:
            print("\n失败的测试:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"     {result['method']} {result['endpoint']} - {result['test_name']}")
                    if result["error"]:
                        print(f"     错误: {result['error']}")
        
        print("\n" + "=" * 50)
    
    def run_all_tests(self):
        """运行所有测试"""
        
        try:
            # 按顺序执行测试
            self.test_system_info()
            time.sleep(1)
            
            self.test_user_management()
            time.sleep(1)
            
            self.test_device_type_management()
            time.sleep(1)
            
            self.test_device_management()
            time.sleep(1)
            
            self.test_usage_records()
            time.sleep(1)
            
            self.test_security_events()
            time.sleep(1)
            
            self.test_user_feedbacks()
            time.sleep(1)
            
            self.test_analytics()
            time.sleep(1)
            
            # 可选：清理测试数据
            # self.cleanup_test_data()
            
        except KeyboardInterrupt:
            print("\n 测试被用户中断")
        except Exception as e:
            print(f"\n   测试过程中发生错误: {e}")
        finally:
            self.print_summary()

def main():
    """主函数"""
    # 检查系统是否可用
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("   系统检查失败，请确保系统已启动")
            return
    except requests.exceptions.RequestException:
        print("   无法连接到系统，请确保系统已启动在 http://localhost:8000")
        return
    
    print("  系统连接正常，开始测试...")
    print()
    
    # 创建测试器并运行测试
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 