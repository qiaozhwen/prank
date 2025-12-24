from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, VisitorInfo
import requests
import os

app = Flask(__name__)
app.config.from_object(Config)

# 允许跨域
CORS(app)

# 初始化数据库
db.init_app(app)

# 百度地图 AK（需要在百度地图开放平台申请）
BAIDU_MAP_AK = os.getenv('BAIDU_MAP_AK', '')


def get_address_from_location(lat, lng):
    """通过百度地图逆地理编码获取地址"""
    if not BAIDU_MAP_AK or not lat or not lng:
        return None, None, None, None
    
    try:
        url = f"https://api.map.baidu.com/reverse_geocoding/v3/?ak={BAIDU_MAP_AK}&output=json&coordtype=wgs84ll&location={lat},{lng}"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        
        if data.get('status') == 0:
            result = data.get('result', {})
            address = result.get('formatted_address', '')
            component = result.get('addressComponent', {})
            province = component.get('province', '')
            city = component.get('city', '')
            district = component.get('district', '')
            return address, province, city, district
    except Exception as e:
        print(f"百度地图API调用失败: {e}")
    
    return None, None, None, None


def get_address_from_ip(ip):
    """通过百度地图IP定位获取地址"""
    if not BAIDU_MAP_AK or not ip or ip in ('127.0.0.1', 'localhost'):
        return None, None, None, None
    
    try:
        url = f"https://api.map.baidu.com/location/ip?ak={BAIDU_MAP_AK}&ip={ip}&coor=bd09ll"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        
        if data.get('status') == 0:
            content = data.get('content', {})
            address = content.get('address', '')
            detail = content.get('address_detail', {})
            province = detail.get('province', '')
            city = detail.get('city', '')
            district = detail.get('district', '')
            return address, province, city, district
    except Exception as e:
        print(f"百度地图IP定位失败: {e}")
    
    return None, None, None, None


def get_real_ip():
    """获取真实IP地址"""
    # 优先从代理头获取
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr


@app.route('/api/collect', methods=['POST'])
def collect_info():
    """收集访客信息"""
    try:
        data = request.get_json() or {}
        
        # 获取真实IP
        ip_address = get_real_ip()
        
        # 获取地址信息
        lat = data.get('latitude')
        lng = data.get('longitude')
        address, province, city, district = None, None, None, None
        
        # 优先通过经纬度获取地址
        if lat and lng:
            address, province, city, district = get_address_from_location(lat, lng)
        
        # 如果没有经纬度，尝试通过IP获取
        if not address:
            address, province, city, district = get_address_from_ip(ip_address)
        
        # 创建访客记录
        visitor = VisitorInfo(
            # 基本信息
            ip_address=ip_address,
            user_agent=data.get('userAgent'),
            
            # 位置信息
            latitude=lat,
            longitude=lng,
            accuracy=data.get('accuracy'),
            altitude=data.get('altitude'),
            altitude_accuracy=data.get('altitudeAccuracy'),
            heading=data.get('heading'),
            speed=data.get('speed'),
            
            # 地址信息
            address=address,
            province=province,
            city=city,
            district=district,
            
            # 设备信息
            platform=data.get('platform'),
            screen_width=data.get('screenWidth'),
            screen_height=data.get('screenHeight'),
            device_pixel_ratio=data.get('devicePixelRatio'),
            color_depth=data.get('colorDepth'),
            
            # 浏览器信息
            browser_name=data.get('browserName'),
            browser_version=data.get('browserVersion'),
            language=data.get('language'),
            languages=','.join(data.get('languages', [])) if data.get('languages') else None,
            timezone=data.get('timezone'),
            timezone_offset=data.get('timezoneOffset'),
            
            # 网络信息
            connection_type=data.get('connectionType'),
            downlink=data.get('downlink'),
            effective_type=data.get('effectiveType'),
            rtt=data.get('rtt'),
            
            # 电池信息
            battery_level=data.get('batteryLevel'),
            battery_charging=data.get('batteryCharging'),
            
            # 硬件信息
            hardware_concurrency=data.get('hardwareConcurrency'),
            device_memory=data.get('deviceMemory'),
            max_touch_points=data.get('maxTouchPoints'),
            
            # 其他信息
            referrer=data.get('referrer'),
            page_url=data.get('pageUrl')
        )
        
        db.session.add(visitor)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '数据已记录',
            'id': visitor.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/visitors', methods=['GET'])
def get_visitors():
    """获取所有访客信息（管理接口）"""
    try:
        visitors = VisitorInfo.query.order_by(VisitorInfo.created_at.desc()).limit(100).all()
        return jsonify({
            'success': True,
            'data': [v.to_dict() for v in visitors]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/visitor/<int:id>', methods=['GET'])
def get_visitor(id):
    """获取单个访客详情"""
    try:
        visitor = VisitorInfo.query.get(id)
        if not visitor:
            return jsonify({
                'success': False,
                'message': '未找到记录'
            }), 404
            
        # 返回完整信息
        return jsonify({
            'success': True,
            'data': {
                'id': visitor.id,
                'ip_address': visitor.ip_address,
                'user_agent': visitor.user_agent,
                'latitude': float(visitor.latitude) if visitor.latitude else None,
                'longitude': float(visitor.longitude) if visitor.longitude else None,
                'accuracy': visitor.accuracy,
                'altitude': visitor.altitude,
                'platform': visitor.platform,
                'screen_width': visitor.screen_width,
                'screen_height': visitor.screen_height,
                'device_pixel_ratio': visitor.device_pixel_ratio,
                'color_depth': visitor.color_depth,
                'browser_name': visitor.browser_name,
                'browser_version': visitor.browser_version,
                'language': visitor.language,
                'languages': visitor.languages,
                'timezone': visitor.timezone,
                'timezone_offset': visitor.timezone_offset,
                'connection_type': visitor.connection_type,
                'downlink': visitor.downlink,
                'effective_type': visitor.effective_type,
                'rtt': visitor.rtt,
                'battery_level': visitor.battery_level,
                'battery_charging': visitor.battery_charging,
                'hardware_concurrency': visitor.hardware_concurrency,
                'device_memory': visitor.device_memory,
                'max_touch_points': visitor.max_touch_points,
                'referrer': visitor.referrer,
                'page_url': visitor.page_url,
                'created_at': visitor.created_at.strftime('%Y-%m-%d %H:%M:%S') if visitor.created_at else None
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({'status': 'ok'})


# 创建数据库表
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

