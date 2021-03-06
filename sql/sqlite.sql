

CREATE TABLE "template" (
	"name1" VARCHAR(30) NOT NULL,
	"name2" VARCHAR(30) NOT NULL,
	"field1" VARCHAR(30) NULL,
	"position1" INTEGER NULL,
	"field2" VARCHAR(30) NULL,
	"position2" INTEGER NULL,
	"field3" VARCHAR(30) NULL,
	"position3" INTEGER NULL,
	"field4" VARCHAR(30) NULL,
	"position4" INTEGER NULL,
	"field5" VARCHAR(30) NOT NULL,
	"field6" VARCHAR(30) NOT NULL,
	"type" INTEGER NOT NULL
);

INSERT INTO "template" ("name1", "name2", "field1", "position1", "field2", "position2", "field3", "position3", "field4", "position4", "field5", "field6", "type") VALUES
	('A', 'C', '白细胞计数（WBC）', 2, '', 0, '', 0, '', 0, '报告', '白细胞计数（WBC）', 1),
	('A', 'C', '中性粒细胞绝对值（NEU#）', 2, '', 0, '', 0, '', 0, '报告', '中性粒细胞绝对值（NEU#）', 2),
	('A', 'C', '嗜酸性粒细胞百分数（EOS%）', 2, '''''', 0, NULL, 0, '''''', 0, '报告', '嗜酸性粒细胞百分数（EOS%）', 1),
	('A', 'D', '血红蛋白（HGB）', 1, '', 0, '', 0, '', 0, '报告', '血红蛋白', 1),
	('A', 'D', '血小板计数（PLT）', 1, '', 0, '', 0, '', 0, '报告', '血小板计数', 1),
	('B', 'F', '血红蛋白（HGB）', 1, '', 0, '', 0, '', 0, '报告', '血红蛋白', 0),
	('B', 'F', '红细胞计数（RBC）', 1, '', 0, '', 0, '', 0, '报告', '红细胞计数', 0);

INSERT INTO "template" ("name1", "name2", "field1", "position1", "field2", "position2", "field3", "position3", "field4", "position4", "field5", "field6", "type") VALUES
	('A', 'B', '白细胞计数', 1, '', 2, '', 3, NULL, 4, '报告', '白细胞计数', 1),
	('A', 'B', '白细胞计数', 2, '', 23, '', 3, NULL, 4, '报告', '白细胞计数', 2),
	('A', 'B', '白细胞计数', 1, '', 2, '', 3, '', 4, '报告', '白细胞计数', 1),
	('A', 'B', '白细胞计数', 2, '', 23, '', 3, '', 4, '报告', '白细胞计数', 2),
	('A', 'C', '白细胞计数（WBC）', 2, '', 0, '', 0, '', 0, '报告', '白细胞计数（WBC）', 1),
	('A', 'C', '中性粒细胞绝对值（NEU#）', 2, '', 0, '', 0, '', 0, '报告', '中性粒细胞绝对值（NEU#）', 2),
	('A', 'C', '嗜酸性粒细胞百分数（EOS%）', 2, '''''', 0, NULL, 0, '''''', 0, '报告', '嗜酸性粒细胞百分数（EOS%）', 1),
	('A', 'D', '血红蛋白（HGB）', 1, '', 0, '', 0, '', 0, '报告', '血红蛋白', 1),
	('A', 'D', '血小板计数（PLT）', 1, '', 0, '', 0, '', 0, '报告', '血小板计数', 1),
	('B', 'F', '血红蛋白（HGB）', 1, '', 0, '', 0, '', 0, '报告', '血红蛋白', 0),
	('B', 'F', '红细胞计数（RBC）', 1, '', 0, '', 0, '', 0, '报告', '红细胞计数', 0);

