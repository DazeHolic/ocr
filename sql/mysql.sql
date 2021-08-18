
CREATE DATABASE IF NOT EXISTS `ocr` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `ocr`;

CREATE TABLE IF NOT EXISTS `tb_ocr_record_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `ocr_log_id` bigint(20) DEFAULT NULL COMMENT '记录id',
  `resident_id` bigint(20) DEFAULT NULL COMMENT '居民id',
  `parameter_id` bigint(20) DEFAULT NULL COMMENT '参数id',
  `parameter` varchar(500) DEFAULT NULL COMMENT '参数值',
  `picture` varchar(500) DEFAULT NULL COMMENT '识别图片',
  `accuracy` decimal(10,4) DEFAULT NULL COMMENT '准确率',
  `Identification_time` timestamp NULL DEFAULT NULL COMMENT '识别时间',
  `is_delete` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否删除，1：是，0：否',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
PARTITION BY HASH (MOD(id, 100)) PARTITIONS 100;


CREATE TABLE IF NOT EXISTS `tbl_template` (
  `template_id` int(11) NOT NULL,
  `name1` varchar(30) NOT NULL,
  `name2` varchar(30) NOT NULL,
  `field1` varchar(30) DEFAULT '',
  `position1` int(11) DEFAULT '0',
  `field2` varchar(30) DEFAULT '',
  `position2` int(11) DEFAULT '0',
  `field3` varchar(30) DEFAULT '',
  `position3` int(11) DEFAULT '0',
  `field4` varchar(30) DEFAULT '',
  `position4` int(11) DEFAULT '0',
  `field5` varchar(30) DEFAULT '',
  `field6` int(11) DEFAULT '0',
  `type` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


INSERT INTO `tbl_template` (`template_id`, `name1`, `name2`, `field1`, `position1`, `field2`, `position2`, `field3`, `position3`, `field4`, `position4`, `field5`, `field6`, `type`) VALUES
	(4, 'B', 'F', '血红蛋白（HGB）', 1, '', 0, '', 0, '', 0, '报告', 1, 0),
	(4, 'B', 'F', '红细胞计数（RBC）', 1, '', 0, '', 0, '', 0, '报告', 2, 0),
	(2, 'A', 'B', '白细胞计数', 1, '', 2, '', 3, '', 4, '报告', 3, 1),
	(2, 'A', 'B', '白细胞计数', 1, '', 2, '', 3, '', 4, '报告', 4, 1),
	(1, 'A', 'C', '白细胞计数（WBC）', 2, '', 0, '', 0, '', 0, '报告', 5, 1),
	(1, 'A', 'C', '嗜酸性粒细胞百分数（EOS%）', 2, '', 0, '', 0, '', 0, '报告', 6, 1),
	(3, 'A', 'D', '血红蛋白（HGB）', 1, '', 0, '', 0, '', 0, '报告', 7, 1),
	(3, 'A', 'D', '血小板计数（PLT）', 1, '', 0, '', 0, '', 0, '报告', 8, 1),
	(2, 'A', 'B', '白细胞计数', 2, '', 23, '', 3, '', 4, '报告', 9, 2),
	(2, 'A', 'B', '白细胞计数', 2, '', 23, '', 3, '', 4, '报告', 10, 2),
	(1, 'A', 'C', '中性粒细胞绝对值（NEU#）', 2, '', 0, '', 0, '', 0, '报告', 11, 2);




