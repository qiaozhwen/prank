import os
from datetime import timedelta
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


class Config:
    # 数据库配置 - 使用 shop 项目相同的数据库
    DB_HOST = os.getenv('DB_HOST', '106.14.227.122')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_USER = os.getenv('DB_USERNAME', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '13524155957Qz@1')
    DB_NAME = os.getenv('DB_DATABASE', 'shop')

    # URL 编码密码中的特殊字符
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 应用配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'prank-tool-secret')

