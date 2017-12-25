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

 Date: 25/12/2017 17:05:49
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for task_case
-- ----------------------------
DROP TABLE IF EXISTS `task_case`;
CREATE TABLE `task_case` (
  `ID` int(16) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `TASK_ID` int(16) DEFAULT NULL,
  `TASK_NAME` varchar(20) DEFAULT NULL,
  `CASE_ID` int(16) DEFAULT NULL,
  `CASE_NAME` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for test_task
-- ----------------------------
DROP TABLE IF EXISTS `test_task`;
CREATE TABLE `test_task` (
  `ID` int(16) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `NAME` varchar(20) DEFAULT NULL,
  `TEAM` varchar(10) DEFAULT NULL,
  `PLATFORM` varchar(20) DEFAULT NULL,
  `COMMENTS` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for troubled_log
-- ----------------------------
DROP TABLE IF EXISTS `troubled_log`;
CREATE TABLE `troubled_log` (
  `ID` int(16) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `TASK_ID` int(16) DEFAULT NULL,
  `TASK_NAME` varchar(20) DEFAULT NULL,
  `CASE_ID` int(16) DEFAULT NULL,
  `CASE_NAME` varchar(20) DEFAULT NULL,
  `TROUBLED_STRATEGY` varchar(20) DEFAULT NULL,
  `TROUBLED_RESPONSE` mediumtext,
  `IS_CRASH` varchar(5) DEFAULT NULL,
  `CRASH_LOG` varchar(500) DEFAULT NULL,
  `SCREEN_SHOT` varchar(50) DEFAULT NULL,
  `CREATE_TIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for url_case
-- ----------------------------
DROP TABLE IF EXISTS `url_case`;
CREATE TABLE `url_case` (
  `ID` int(16) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `NAME` varchar(20) DEFAULT NULL,
  `SCHEMA` varchar(100) DEFAULT NULL,
  `KEYWORDS` varchar(100) DEFAULT NULL,
  `COMMENTS` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
