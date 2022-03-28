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

 Date: 23/09/2021 22:34:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for blog_blogtags
-- ----------------------------
DROP TABLE IF EXISTS `blog_blogtags`;
CREATE TABLE `blog_blogtags`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `color` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_date` datetime(6) DEFAULT NULL,
  `last_edited_date` datetime(6) DEFAULT NULL,
  `deleted` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_by_id` int(0) DEFAULT NULL,
  `last_edited_by_id` int(0) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `blog_blogtags_created_by_id_9e1437f9_fk_user_userextension_id`(`created_by_id`) USING BTREE,
  INDEX `blog_blogtags_last_edited_by_id_1d42585e_fk_user_user`(`last_edited_by_id`) USING BTREE,
  CONSTRAINT `blog_blogtags_created_by_id_9e1437f9_fk_user_userextension_id` FOREIGN KEY (`created_by_id`) REFERENCES `user_userextension` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `blog_blogtags_last_edited_by_id_1d42585e_fk_user_user` FOREIGN KEY (`last_edited_by_id`) REFERENCES `user_userextension` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of blog_blogtags
-- ----------------------------
INSERT INTO `blog_blogtags` VALUES (1, '工业', '#6190e8', '2021-09-23 13:34:33.107804', '2021-09-23 13:37:46.113676', '0', 1, 1);
INSERT INTO `blog_blogtags` VALUES (2, '乡村', '#6190e8', '2021-09-23 13:34:49.099976', '2021-09-23 13:37:41.560132', '0', 1, 1);
INSERT INTO `blog_blogtags` VALUES (3, '自驾', '#6190e8', '2021-09-23 13:35:07.356742', '2021-09-23 13:37:38.034988', '0', 1, 1);
INSERT INTO `blog_blogtags` VALUES (4, '闲逛', '#6190e8', '2021-09-23 13:35:24.325335', '2021-09-23 13:37:33.350662', '0', 1, 1);
INSERT INTO `blog_blogtags` VALUES (5, '观光', '#6190e8', '2021-09-23 13:36:43.644972', '2021-09-23 13:36:43.644972', '0', 1, 1);
INSERT INTO `blog_blogtags` VALUES (6, '度假', '#6190e8', '2021-09-23 13:36:52.568527', '2021-09-23 13:36:52.568527', '0', 1, 1);
INSERT INTO `blog_blogtags` VALUES (7, '民俗', '#6190e8', '2021-09-23 13:37:11.676450', '2021-09-23 13:37:11.676450', '0', 1, 1);

SET FOREIGN_KEY_CHECKS = 1;
