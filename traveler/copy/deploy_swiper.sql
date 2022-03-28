/*
 Navicat Premium Data Transfer

 Source Server         : mypc
 Source Server Type    : MySQL
 Source Server Version : 80020
 Source Host           : localhost:3306
 Source Schema         : traveler

 Target Server Type    : MySQL
 Target Server Version : 80020
 File Encoding         : 65001

 Date: 23/09/2021 22:34:55
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for deploy_swiper
-- ----------------------------
DROP TABLE IF EXISTS `deploy_swiper`;
CREATE TABLE `deploy_swiper`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `img` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `path` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_date` datetime(6) DEFAULT NULL,
  `last_edited_date` datetime(6) DEFAULT NULL,
  `deleted` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_by_id` int(0) DEFAULT NULL,
  `last_edited_by_id` int(0) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `deploy_swiper_created_by_id_c9e35094_fk_user_userextension_id`(`created_by_id`) USING BTREE,
  INDEX `deploy_swiper_last_edited_by_id_abfac5b8_fk_user_user`(`last_edited_by_id`) USING BTREE,
  CONSTRAINT `deploy_swiper_created_by_id_c9e35094_fk_user_userextension_id` FOREIGN KEY (`created_by_id`) REFERENCES `user_userextension` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `deploy_swiper_last_edited_by_id_abfac5b8_fk_user_user` FOREIGN KEY (`last_edited_by_id`) REFERENCES `user_userextension` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of deploy_swiper
-- ----------------------------
INSERT INTO `deploy_swiper` VALUES (1, '探险 · 燃起的篝火不仅点亮原野的夜晚', 'imgs/2021_09/tanxian.jpg', '', '2021-09-23 14:27:30.870844', '2021-09-23 14:27:30.870844', '0', 1, 1);
INSERT INTO `deploy_swiper` VALUES (2, '自驾 · 这条路通向着自由的信仰', 'imgs/2021_09/zijia.jpg', '', '2021-09-23 14:28:56.218670', '2021-09-23 14:28:56.218670', '0', 1, 1);
INSERT INTO `deploy_swiper` VALUES (3, '乡村 · 结庐在人境而无车马喧', 'imgs/2021_09/xiangcun.jpg', '', '2021-09-23 14:29:27.763220', '2021-09-23 14:29:27.763220', '0', 1, 1);
INSERT INTO `deploy_swiper` VALUES (4, '工业 · 钢筋混泥土孕育的希望', 'imgs/2021_09/gongye.jpg', '', '2021-09-23 14:30:11.800385', '2021-09-23 14:30:11.800385', '0', 1, 1);
INSERT INTO `deploy_swiper` VALUES (5, '民俗 · 风土人情写满了诗的篇章', 'imgs/2021_09/minsu.jpg', '', '2021-09-23 14:32:29.650695', '2021-09-23 14:32:29.650695', '0', 1, 1);

SET FOREIGN_KEY_CHECKS = 1;
