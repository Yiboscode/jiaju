/*
 Navicat Premium Dump SQL

 Source Server         : mysql8
 Source Server Type    : MySQL
 Source Server Version : 80037 (8.0.37)
 Source Host           : localhost:3306
 Source Schema         : smart_home_db

 Target Server Type    : MySQL
 Target Server Version : 80037 (8.0.37)
 File Encoding         : 65001

 Date: 26/06/2025 22:15:49
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for device_types
-- ----------------------------
DROP TABLE IF EXISTS `device_types`;
CREATE TABLE `device_types`  (
  `type_id` int NOT NULL AUTO_INCREMENT,
  `type_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `avg_power_consumption` float NULL DEFAULT NULL COMMENT '平均功耗(瓦)',
  `avg_daily_usage_hours` float NULL DEFAULT NULL COMMENT '平均每日使用小时数',
  PRIMARY KEY (`type_id`) USING BTREE,
  UNIQUE INDEX `type_name`(`type_name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 36 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of device_types
-- ----------------------------
INSERT INTO `device_types` VALUES (1, '智能LED灯泡', '9.5W智能LED灯泡，相当于60W白炽灯亮度，支持调光调色', 9.5, 6);
INSERT INTO `device_types` VALUES (2, '变频空调1.5匹', '1.5匹变频空调，适合18平米房间，制冷功率800W', 800, 8);
INSERT INTO `device_types` VALUES (3, '智能音响', '智能AI音响，支持语音控制，待机功率2W，工作功率15W', 15, 4);
INSERT INTO `device_types` VALUES (4, '智能摄像头', '1080P智能安防摄像头，支持夜视和移动侦测', 8, 24);
INSERT INTO `device_types` VALUES (5, '智能门锁', '指纹+密码智能门锁，5V供电，正常使用3个月换电池', 3, 0.5);
INSERT INTO `device_types` VALUES (6, '智能插座', '16A智能插座，支持远程控制和定时开关', 2, 24);
INSERT INTO `device_types` VALUES (7, '智能窗帘', '电动智能窗帘，支持手机和语音控制', 45, 0.5);
INSERT INTO `device_types` VALUES (8, '智能冰箱300L', '300升变频智能冰箱，一级能效，日耗电0.6度', 150, 8);
INSERT INTO `device_types` VALUES (9, '滚筒洗衣机8KG', '8公斤滚筒洗衣机，变频电机，平均功率500W', 500, 1.5);
INSERT INTO `device_types` VALUES (10, '55寸智能电视', '55寸4K智能液晶电视，HDR支持，功率120W', 120, 6);
INSERT INTO `device_types` VALUES (11, '65寸智能电视', '65寸4K智能液晶电视，功率200W', 200, 6);
INSERT INTO `device_types` VALUES (12, '变频空调1匹', '1匹变频空调，适合12平米房间，制冷功率600W', 600, 8);
INSERT INTO `device_types` VALUES (13, '变频空调2匹', '2匹变频空调，适合28平米房间，制冷功率1200W', 1200, 8);
INSERT INTO `device_types` VALUES (14, '波轮洗衣机7KG', '7公斤波轮洗衣机，功率350W，洗涤时间40分钟', 350, 1);
INSERT INTO `device_types` VALUES (15, '智能冰箱500L', '500升对开门智能冰箱，变频压缩机，日耗电0.62度', 180, 8);
INSERT INTO `device_types` VALUES (16, '43寸智能电视', '43寸智能液晶电视，功率75W', 75, 6);
INSERT INTO `device_types` VALUES (17, '智能热水器60L', '60升电热水器，智能预约加热，功率2000W', 2000, 2);
INSERT INTO `device_types` VALUES (18, '智能电饭煲', '5L智能电饭煲，IH加热，功率1200W', 1200, 1);
INSERT INTO `device_types` VALUES (19, '智能加湿器', '超声波加湿器，静音运行，功率25W', 25, 8);
INSERT INTO `device_types` VALUES (20, '智能扫地机器人', '激光导航扫地机器人，锂电池供电，功率30W', 30, 1.5);

-- ----------------------------
-- Table structure for devices
-- ----------------------------
DROP TABLE IF EXISTS `devices`;
CREATE TABLE `devices`  (
  `device_id` int NOT NULL AUTO_INCREMENT,
  `device_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `device_type_id` int NOT NULL,
  `user_id` int NOT NULL,
  `room_location` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` tinyint(1) NULL DEFAULT NULL COMMENT '0=离线,1=在线',
  `actual_power_consumption` float NULL DEFAULT NULL COMMENT '实际功耗(瓦)',
  `installation_date` datetime NULL DEFAULT NULL,
  `last_maintenance` datetime NULL DEFAULT NULL,
  `brand` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `model` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`device_id`) USING BTREE,
  INDEX `device_type_id`(`device_type_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_devices_status`(`status` ASC) USING BTREE,
  CONSTRAINT `devices_ibfk_1` FOREIGN KEY (`device_type_id`) REFERENCES `device_types` (`type_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `devices_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 151 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of devices
-- ----------------------------
INSERT INTO `devices` VALUES (1, '客厅主灯', 1, 1, '客厅', 1, 9.5, '2024-01-20 10:00:00', '2024-12-15 14:30:00', '飞利浦', 'Hue White A19');
INSERT INTO `devices` VALUES (2, '主卧空调', 2, 1, '主卧', 1, 820, '2024-01-22 14:30:00', '2024-11-20 09:15:00', '格力', 'KFR-35GW');
INSERT INTO `devices` VALUES (3, '客厅智能音响', 3, 1, '客厅', 1, 18, '2024-02-01 11:20:00', NULL, '小米', 'XiaoAI Speaker Pro');
INSERT INTO `devices` VALUES (4, '门口摄像头', 4, 1, '门厅', 1, 8.5, '2024-01-25 16:45:00', '2024-10-12 11:20:00', '海康威视', 'DS-2CD2143G0-I');
INSERT INTO `devices` VALUES (5, '入户门锁', 5, 1, '门厅', 1, 3.2, '2024-01-23 09:30:00', NULL, '德施曼', 'T11');
INSERT INTO `devices` VALUES (6, '厨房冰箱', 8, 1, '厨房', 1, 155, '2024-01-26 13:15:00', '2024-09-08 15:40:00', '海尔', 'BCD-318WDPCU1');
INSERT INTO `devices` VALUES (7, '客厅电视', 10, 1, '客厅', 1, 125, '2024-02-05 10:25:00', NULL, '小米', 'L55M8-5ANE');
INSERT INTO `devices` VALUES (8, '卧室吸顶灯', 1, 2, '主卧', 1, 12, '2024-02-25 14:20:00', NULL, '欧普', 'MX780');
INSERT INTO `devices` VALUES (9, '客厅空调', 13, 2, '客厅', 1, 1250, '2024-03-01 09:40:00', '2024-12-03 16:20:00', '美的', 'KFR-50LW');
INSERT INTO `devices` VALUES (10, '阳台洗衣机', 9, 2, '阳台', 1, 520, '2024-03-05 11:30:00', '2024-08-15 10:45:00', '小天鹅', 'TD100V61WDG');
INSERT INTO `devices` VALUES (11, '智能插座01', 6, 2, '客厅', 1, 2.5, '2024-03-10 15:15:00', NULL, '米家', 'ZNCZ05CM');
INSERT INTO `devices` VALUES (12, '客厅窗帘', 7, 2, '客厅', 0, 48, '2024-03-15 13:50:00', '2024-11-28 14:20:00', '杜亚', 'DT52S');
INSERT INTO `devices` VALUES (13, '餐厅吊灯', 1, 3, '餐厅', 1, 10.5, '2024-03-15 10:30:00', NULL, '雷士', 'LED-CL-36W');
INSERT INTO `devices` VALUES (14, '书房空调', 12, 3, '书房', 1, 650, '2024-03-18 14:15:00', '2024-10-25 11:30:00', '奥克斯', 'KFR-26GW');
INSERT INTO `devices` VALUES (15, '厨房电饭煲', 18, 3, '厨房', 1, 1180, '2024-03-20 16:40:00', NULL, '苏泊尔', 'CFXB40FC833A');
INSERT INTO `devices` VALUES (16, '客厅扫地机器人', 20, 3, '客厅', 1, 32, '2024-03-25 09:20:00', '2024-12-10 15:45:00', '科沃斯', 'T10 PLUS');
INSERT INTO `devices` VALUES (17, '主卧台灯', 1, 4, '主卧', 1, 8.5, '2024-01-30 12:15:00', NULL, '飞利浦', 'Hue Go');
INSERT INTO `devices` VALUES (18, '客厅大空调', 13, 4, '客厅', 1, 1320, '2024-02-02 15:30:00', '2024-11-15 10:20:00', '海信', 'KFR-50LW');
INSERT INTO `devices` VALUES (19, '门厅智能音响', 3, 4, '门厅', 1, 16, '2024-02-08 11:45:00', NULL, '天猫精灵', 'X5');
INSERT INTO `devices` VALUES (20, '阳台摄像头', 4, 4, '阳台', 1, 7.8, '2024-02-10 14:20:00', '2024-09-30 16:15:00', '萤石', 'C6CN');

-- ----------------------------
-- Table structure for energy_statistics
-- ----------------------------
DROP TABLE IF EXISTS `energy_statistics`;
CREATE TABLE `energy_statistics`  (
  `stat_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `device_id` int NULL DEFAULT NULL,
  `stat_date` date NOT NULL,
  `daily_consumption` float NULL DEFAULT NULL COMMENT '日耗电量(千瓦时)',
  `peak_power` float NULL DEFAULT NULL COMMENT '峰值功率(瓦)',
  `avg_power` float NULL DEFAULT NULL COMMENT '平均功率(瓦)',
  `usage_duration` int NULL DEFAULT NULL COMMENT '使用时长(分钟)',
  `cost` decimal(10, 2) NULL DEFAULT NULL COMMENT '电费成本(元)',
  PRIMARY KEY (`stat_id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `device_id`(`device_id` ASC) USING BTREE,
  INDEX `stat_date`(`stat_date` ASC) USING BTREE,
  INDEX `idx_energy_stats_date`(`stat_date` ASC) USING BTREE,
  CONSTRAINT `energy_statistics_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `energy_statistics_ibfk_2` FOREIGN KEY (`device_id`) REFERENCES `devices` (`device_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 101 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of energy_statistics
-- ----------------------------
INSERT INTO `energy_statistics` VALUES (1, 1, 2, '2025-06-24', 8.2, 850, 820, 600, 4.10);
INSERT INTO `energy_statistics` VALUES (2, 1, 6, '2025-06-24', 0.62, 180, 155, 1440, 0.31);
INSERT INTO `energy_statistics` VALUES (3, 1, 7, '2025-06-24', 0.563, 125, 120, 270, 0.28);
INSERT INTO `energy_statistics` VALUES (4, 2, 9, '2025-06-24', 15, 1280, 1250, 720, 7.50);
INSERT INTO `energy_statistics` VALUES (5, 2, 10, '2025-06-24', 1.17, 550, 520, 135, 0.59);

-- ----------------------------
-- Table structure for security_events
-- ----------------------------
DROP TABLE IF EXISTS `security_events`;
CREATE TABLE `security_events`  (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `device_id` int NULL DEFAULT NULL,
  `event_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `severity_level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `occurred_at` datetime NULL DEFAULT NULL,
  `resolved_at` datetime NULL DEFAULT NULL,
  `is_resolved` tinyint(1) NULL DEFAULT NULL,
  `location` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`event_id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `device_id`(`device_id` ASC) USING BTREE,
  INDEX `occurred_at`(`occurred_at` ASC) USING BTREE,
  INDEX `idx_security_events_resolved`(`is_resolved` ASC) USING BTREE,
  CONSTRAINT `security_events_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `security_events_ibfk_2` FOREIGN KEY (`device_id`) REFERENCES `devices` (`device_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 57 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of security_events
-- ----------------------------
INSERT INTO `security_events` VALUES (1, 1, 4, '移动检测', '低', '门口检测到人员活动', '2025-06-24 14:30:00', '2025-06-24 14:31:00', 1, '门厅');
INSERT INTO `security_events` VALUES (2, 1, 5, '门锁异常', '中', '连续5次错误密码输入', '2025-06-23 22:15:00', '2025-06-23 22:20:00', 1, '门厅');
INSERT INTO `security_events` VALUES (3, 2, NULL, '设备离线', '中', '客厅窗帘控制器离线', '2025-06-24 10:45:00', NULL, 0, '客厅');
INSERT INTO `security_events` VALUES (4, 3, 16, '设备故障', '低', '扫地机器人电量不足自动返回充电', '2025-06-24 16:20:00', '2025-06-24 18:30:00', 1, '客厅');
INSERT INTO `security_events` VALUES (5, 4, 20, '夜视激活', '低', '阳台摄像头检测到夜间活动', '2025-06-24 02:30:00', '2025-06-24 02:31:00', 1, '阳台');

-- ----------------------------
-- Table structure for usage_records
-- ----------------------------
DROP TABLE IF EXISTS `usage_records`;
CREATE TABLE `usage_records`  (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `device_id` int NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NULL DEFAULT NULL,
  `duration_minutes` int NULL DEFAULT NULL,
  `energy_consumed` float NULL DEFAULT NULL COMMENT '消耗电量(千瓦时)',
  `operation_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `ambient_temperature` float NULL DEFAULT NULL COMMENT '环境温度',
  `humidity` float NULL DEFAULT NULL COMMENT '湿度百分比',
  PRIMARY KEY (`record_id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `device_id`(`device_id` ASC) USING BTREE,
  INDEX `start_time`(`start_time` ASC) USING BTREE,
  INDEX `idx_usage_records_date`(`start_time` ASC) USING BTREE,
  CONSTRAINT `usage_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `usage_records_ibfk_2` FOREIGN KEY (`device_id`) REFERENCES `devices` (`device_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1001 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of usage_records
-- ----------------------------
INSERT INTO `usage_records` VALUES (1, 1, 2, '2025-06-24 08:30:00', '2025-06-24 18:30:00', 600, 8.2, '制冷', 28.5, 65);
INSERT INTO `usage_records` VALUES (2, 1, 2, '2025-06-23 09:15:00', '2025-06-23 17:45:00', 510, 6.97, '制冷', 29.2, 68);
INSERT INTO `usage_records` VALUES (3, 2, 9, '2025-06-24 10:00:00', '2025-06-24 22:00:00', 720, 15, '制冷', 31, 72);
INSERT INTO `usage_records` VALUES (4, 1, 7, '2025-06-24 19:00:00', '2025-06-24 23:30:00', 270, 0.563, '观看', 25, 60);
INSERT INTO `usage_records` VALUES (5, 1, 7, '2025-06-23 20:15:00', '2025-06-23 22:45:00', 150, 0.313, '观看', 24.8, 58);
INSERT INTO `usage_records` VALUES (6, 2, 10, '2025-06-24 14:30:00', '2025-06-24 16:45:00', 135, 1.17, '洗涤', 26, 55);
INSERT INTO `usage_records` VALUES (7, 2, 10, '2025-06-22 10:20:00', '2025-06-22 12:35:00', 135, 1.17, '洗涤', 25.5, 52);
INSERT INTO `usage_records` VALUES (8, 1, 6, '2025-06-24 00:00:00', '2025-06-25 00:00:00', 1440, 0.62, '保鲜', 22, 45);
INSERT INTO `usage_records` VALUES (9, 1, 6, '2025-06-23 00:00:00', '2025-06-24 00:00:00', 1440, 0.65, '保鲜', 23.5, 48);
INSERT INTO `usage_records` VALUES (10, 1, 1, '2025-06-24 18:00:00', '2025-06-24 23:00:00', 300, 0.048, '照明', 24, 55);
INSERT INTO `usage_records` VALUES (11, 1, 1, '2025-06-23 19:30:00', '2025-06-23 22:30:00', 180, 0.029, '照明', 23.8, 57);

-- ----------------------------
-- Table structure for user_feedbacks
-- ----------------------------
DROP TABLE IF EXISTS `user_feedbacks`;
CREATE TABLE `user_feedbacks`  (
  `feedback_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `feedback_type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `rating` int NULL DEFAULT NULL COMMENT '评分1-5',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `submitted_at` datetime NULL DEFAULT NULL,
  `is_processed` tinyint(1) NULL DEFAULT NULL,
  `response` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `processed_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`feedback_id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `submitted_at`(`submitted_at` ASC) USING BTREE,
  CONSTRAINT `user_feedbacks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 37 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_feedbacks
-- ----------------------------
INSERT INTO `user_feedbacks` VALUES (1, 1, '功能建议', 5, '希望能增加语音控制场景模式，比如说\"睡眠模式\"就能自动关闭所有灯光和电视', '2025-06-20 10:30:00', 1, '感谢您的建议，我们正在开发场景模式功能，预计下个版本上线', '2025-06-21 14:20:00');
INSERT INTO `user_feedbacks` VALUES (2, 2, '使用体验', 4, '空调的智能温控很好用，能自动调节温度，比以前省电不少', '2025-06-18 16:45:00', 1, '谢谢您的反馈，我们会继续优化智能温控算法', '2025-06-19 09:15:00');
INSERT INTO `user_feedbacks` VALUES (3, 3, 'Bug报告', 3, '扫地机器人有时会在同一个地方转圈，希望能优化路径规划', '2025-06-15 14:20:00', 1, '我们已收到您的反馈，将在下次固件更新中改进路径算法', '2025-06-16 11:30:00');
INSERT INTO `user_feedbacks` VALUES (4, 4, '性能问题', 4, '智能门锁响应速度很快，指纹识别准确率也很高', '2025-06-22 09:10:00', 0, NULL, NULL);
INSERT INTO `user_feedbacks` VALUES (5, 5, '界面优化', 3, '手机APP界面可以更简洁一些，功能分类不够清晰', '2025-06-21 20:30:00', 0, NULL, NULL);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `house_area` float NULL DEFAULT NULL COMMENT '房屋面积平方米',
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 28 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, '张伟', 'zhangwei@163.com', '13800138001', 89.5, '北京', '2024-01-15 10:30:00', '2025-06-25 15:20:00');
INSERT INTO `users` VALUES (2, '王芳', 'wangfang@qq.com', '13800138002', 125.8, '上海', '2024-02-20 14:15:00', '2025-06-25 16:45:00');
INSERT INTO `users` VALUES (3, '李军', 'lijun@gmail.com', '13800138003', 68.2, '深圳', '2024-03-10 09:20:00', '2025-06-25 11:30:00');
INSERT INTO `users` VALUES (4, '刘敏', 'liumin@sina.com', '13800138004', 156.7, '广州', '2024-01-25 16:40:00', '2025-06-25 13:15:00');
INSERT INTO `users` VALUES (5, '陈强', 'chenqiang@126.com', '13800138005', 95.3, '杭州', '2024-04-05 11:25:00', '2025-06-25 14:50:00');
INSERT INTO `users` VALUES (6, '赵丽', 'zhaoli@163.com', '13800138006', 78.9, '南京', '2024-02-28 13:50:00', '2025-06-25 12:10:00');
INSERT INTO `users` VALUES (7, '孙涛', 'suntao@qq.com', '13800138007', 142.6, '成都', '2024-03-18 15:30:00', '2025-06-25 17:25:00');
INSERT INTO `users` VALUES (8, '周静', 'zhoujing@gmail.com', '13800138008', 85.4, '武汉', '2024-01-08 08:45:00', '2025-06-25 09:35:00');
INSERT INTO `users` VALUES (9, '吴斌', 'wubin@sina.com', '13800138009', 118.7, '西安', '2024-04-12 10:15:00', '2025-06-25 16:20:00');
INSERT INTO `users` VALUES (10, '徐琳', 'xulin@126.com', '13800138010', 103.2, '重庆', '2024-02-14 12:30:00', '2025-06-25 14:40:00');
INSERT INTO `users` VALUES (11, '朱华', 'zhuhua@163.com', '13800138011', 76.8, '天津', '2024-03-22 14:20:00', '2025-06-25 11:55:00');
INSERT INTO `users` VALUES (12, '郭鹏', 'guopeng@qq.com', '13800138012', 134.5, '苏州', '2024-01-30 16:10:00', '2025-06-25 15:30:00');
INSERT INTO `users` VALUES (13, '何玲', 'heling@gmail.com', '13800138013', 92.1, '青岛', '2024-04-08 09:40:00', '2025-06-25 13:45:00');
INSERT INTO `users` VALUES (14, '高峰', 'gaofeng@sina.com', '13800138014', 108.9, '大连', '2024-02-16 11:20:00', '2025-06-25 16:15:00');
INSERT INTO `users` VALUES (15, '梁雪', 'liangxue@126.com', '13800138015', 87.6, '厦门', '2024-03-26 13:35:00', '2025-06-25 12:25:00');
INSERT INTO `users` VALUES (16, '曹磊', 'caolei@163.com', '13800138016', 121.3, '宁波', '2024-01-12 15:45:00', '2025-06-25 17:50:00');
INSERT INTO `users` VALUES (17, '邓红', 'denghong@qq.com', '13800138017', 99.7, '长沙', '2024-04-15 08:25:00', '2025-06-25 10:40:00');
INSERT INTO `users` VALUES (18, '姚勇', 'yaoyong@gmail.com', '13800138018', 115.4, '郑州', '2024-02-08 10:50:00', '2025-06-25 14:15:00');
INSERT INTO `users` VALUES (19, '秦丽', 'qinli@sina.com', '13800138019', 82.3, '合肥', '2024-03-30 12:40:00', '2025-06-25 15:55:00');
INSERT INTO `users` VALUES (20, '韩涛', 'hantao@126.com', '13800138020', 138.8, '济南', '2024-01-20 14:55:00', '2025-06-25 13:20:00');

-- ----------------------------
-- View structure for daily_energy_summary
-- ----------------------------
DROP VIEW IF EXISTS `daily_energy_summary`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `daily_energy_summary` AS select `u`.`username` AS `username`,`u`.`city` AS `city`,`es`.`stat_date` AS `stat_date`,sum(`es`.`daily_consumption`) AS `total_consumption`,sum(`es`.`cost`) AS `total_cost`,count(distinct `es`.`device_id`) AS `active_devices` from (`energy_statistics` `es` join `users` `u` on((`es`.`user_id` = `u`.`user_id`))) group by `u`.`user_id`,`es`.`stat_date` order by `es`.`stat_date` desc;

-- ----------------------------
-- View structure for device_efficiency
-- ----------------------------
DROP VIEW IF EXISTS `device_efficiency`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `device_efficiency` AS select `d`.`device_name` AS `device_name`,`dt`.`type_name` AS `type_name`,`dt`.`avg_power_consumption` AS `rated_power`,`d`.`actual_power_consumption` AS `actual_power`,round(((`d`.`actual_power_consumption` / `dt`.`avg_power_consumption`) * 100),2) AS `efficiency_ratio`,`d`.`brand` AS `brand`,`d`.`model` AS `model` from (`devices` `d` join `device_types` `dt` on((`d`.`device_type_id` = `dt`.`type_id`))) where (`d`.`status` = 1);

SET FOREIGN_KEY_CHECKS = 1;
