-- 访客信息表
-- 存储通过整人链接收集到的用户信息

CREATE TABLE IF NOT EXISTS `prank_visitor_info` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    
    -- 基本信息
    `ip_address` VARCHAR(50) COMMENT 'IP地址',
    `user_agent` TEXT COMMENT '浏览器UA',
    
    -- 位置信息
    `latitude` DECIMAL(10, 8) COMMENT '纬度',
    `longitude` DECIMAL(11, 8) COMMENT '经度',
    `accuracy` FLOAT COMMENT '位置精度(米)',
    `altitude` FLOAT COMMENT '海拔',
    `altitude_accuracy` FLOAT COMMENT '海拔精度',
    `heading` FLOAT COMMENT '移动方向',
    `speed` FLOAT COMMENT '移动速度',
    
    -- 设备信息
    `platform` VARCHAR(100) COMMENT '操作系统',
    `screen_width` INT COMMENT '屏幕宽度',
    `screen_height` INT COMMENT '屏幕高度',
    `device_pixel_ratio` FLOAT COMMENT '设备像素比',
    `color_depth` INT COMMENT '颜色深度',
    
    -- 浏览器信息
    `browser_name` VARCHAR(100) COMMENT '浏览器名称',
    `browser_version` VARCHAR(100) COMMENT '浏览器版本',
    `language` VARCHAR(20) COMMENT '语言',
    `languages` TEXT COMMENT '语言列表',
    `timezone` VARCHAR(100) COMMENT '时区',
    `timezone_offset` INT COMMENT '时区偏移(分钟)',
    
    -- 网络信息
    `connection_type` VARCHAR(50) COMMENT '网络类型',
    `downlink` FLOAT COMMENT '下行速度',
    `effective_type` VARCHAR(20) COMMENT '有效网络类型',
    `rtt` INT COMMENT '往返时间',
    
    -- 电池信息
    `battery_level` FLOAT COMMENT '电池电量',
    `battery_charging` BOOLEAN COMMENT '是否充电中',
    
    -- 硬件信息
    `hardware_concurrency` INT COMMENT 'CPU核心数',
    `device_memory` FLOAT COMMENT '设备内存(GB)',
    `max_touch_points` INT COMMENT '触摸点数',
    
    -- 其他信息
    `referrer` TEXT COMMENT '来源页面',
    `page_url` TEXT COMMENT '访问页面',
    
    -- 时间戳
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    INDEX `idx_ip` (`ip_address`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='访客信息收集表';

