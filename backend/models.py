from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class VisitorInfo(db.Model):
    """访客信息表 - 收集访问者的各种信息"""
    __tablename__ = 'prank_visitor_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 基本信息
    ip_address = db.Column(db.String(50), comment='IP地址')
    user_agent = db.Column(db.Text, comment='浏览器UA')
    
    # 位置信息
    latitude = db.Column(db.Decimal(10, 8), comment='纬度')
    longitude = db.Column(db.Decimal(11, 8), comment='经度')
    accuracy = db.Column(db.Float, comment='位置精度(米)')
    altitude = db.Column(db.Float, comment='海拔')
    altitude_accuracy = db.Column(db.Float, comment='海拔精度')
    heading = db.Column(db.Float, comment='移动方向')
    speed = db.Column(db.Float, comment='移动速度')
    
    # 设备信息
    platform = db.Column(db.String(100), comment='操作系统')
    screen_width = db.Column(db.Integer, comment='屏幕宽度')
    screen_height = db.Column(db.Integer, comment='屏幕高度')
    device_pixel_ratio = db.Column(db.Float, comment='设备像素比')
    color_depth = db.Column(db.Integer, comment='颜色深度')
    
    # 浏览器信息
    browser_name = db.Column(db.String(100), comment='浏览器名称')
    browser_version = db.Column(db.String(100), comment='浏览器版本')
    language = db.Column(db.String(20), comment='语言')
    languages = db.Column(db.Text, comment='语言列表')
    timezone = db.Column(db.String(100), comment='时区')
    timezone_offset = db.Column(db.Integer, comment='时区偏移(分钟)')
    
    # 网络信息
    connection_type = db.Column(db.String(50), comment='网络类型')
    downlink = db.Column(db.Float, comment='下行速度')
    effective_type = db.Column(db.String(20), comment='有效网络类型')
    rtt = db.Column(db.Integer, comment='往返时间')
    
    # 电池信息
    battery_level = db.Column(db.Float, comment='电池电量')
    battery_charging = db.Column(db.Boolean, comment='是否充电中')
    
    # 硬件信息
    hardware_concurrency = db.Column(db.Integer, comment='CPU核心数')
    device_memory = db.Column(db.Float, comment='设备内存(GB)')
    max_touch_points = db.Column(db.Integer, comment='触摸点数')
    
    # 其他信息
    referrer = db.Column(db.Text, comment='来源页面')
    page_url = db.Column(db.Text, comment='访问页面')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'ip_address': self.ip_address,
            'latitude': float(self.latitude) if self.latitude else None,
            'longitude': float(self.longitude) if self.longitude else None,
            'platform': self.platform,
            'browser_name': self.browser_name,
            'language': self.language,
            'timezone': self.timezone,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

