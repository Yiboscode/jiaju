import os

# 数据库配置
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'smart_home_db',
    'charset': 'utf8mb4'
}

# MySQL连接URL
DATABASE_URL = f"mysql+pymysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}?charset={DATABASE_CONFIG['charset']}"

# API配置
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 8000,
    'debug': True
} 