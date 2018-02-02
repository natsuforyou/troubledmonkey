/*
 Navicat Premium Data Transfer

 Source Server         : local-mysql
 Source Server Type    : MySQL
 Source Server Version : 50720
 Source Host           : localhost:3306
 Source Schema         : monkey

 Target Server Type    : MySQL
 Target Server Version : 50720
 File Encoding         : 65001

 Date: 02/02/2018 15:09:28
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for case
-- ----------------------------
DROP TABLE IF EXISTS `case`;
CREATE TABLE `case` (
  `ID` int(16) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `NAME` varchar(20) DEFAULT NULL COMMENT 'case名称',
  `SCHEMA` varchar(100) DEFAULT NULL COMMENT '页面地址',
  `KEYWORDS` varchar(100) DEFAULT NULL COMMENT '关键字',
  `RESPONSE` varchar(500) DEFAULT NULL COMMENT '返回报文',
  `TOTAL_COUNT` int(11) DEFAULT NULL COMMENT '执行次数',
  `COMMENTS` varchar(50) DEFAULT NULL COMMENT '备注',
  `CREATE_TIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for task
-- ----------------------------
DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
  `ID` int(16) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `NAME` varchar(20) DEFAULT NULL,
  `TEAM` varchar(10) DEFAULT NULL,
  `PLATFORM` varchar(20) DEFAULT NULL,
  `CASES` varchar(100) NOT NULL,
  `COMMENTS` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for troubled_log
-- ----------------------------
DROP TABLE IF EXISTS `troubled_log`;
CREATE TABLE `troubled_log` (
  `ID` int(16) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `TASK_ID` int(16) unsigned zerofill DEFAULT NULL,
  `TASK_NAME` varchar(20) DEFAULT NULL,
  `STATE` varchar(10) DEFAULT NULL,
  `CREATE_TIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `LOG_SIZE` int(11) DEFAULT NULL,
  `OFFSET` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for troubled_log_detail
-- ----------------------------
DROP TABLE IF EXISTS `troubled_log_detail`;
CREATE TABLE `troubled_log_detail` (
  `ID` int(16) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `LOG_ID` int(16) DEFAULT NULL,
  `CASE_ID` int(16) DEFAULT NULL,
  `CASE_NAME` varchar(20) DEFAULT NULL,
  `STATE` varchar(10) DEFAULT NULL,
  `TROUBLED_STRATEGY` varchar(20) DEFAULT NULL,
  `TROUBLED_RESPONSE` mediumtext,
  `IS_CRASH` varchar(5) DEFAULT NULL,
  `CRASH_LOG` varchar(500) DEFAULT NULL,
  `SCREEN_SHOT` varchar(50) DEFAULT NULL,
  `CREATE_TIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
