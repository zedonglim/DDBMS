DROP TABLE IF EXISTS `popular_rank`;
CREATE TABLE `popular_rank` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `timestamp` char(14) DEFAULT NULL,
  `temporalGranularity` text,
  `articleAidList` text,
  PRIMARY KEY (`id`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `popular_rank` WRITE;
INSERT INTO `popular_rank` (`timestamp`, `temporalGranularity`, `articleAidList`) VALUES
(1703148201, 'daily', ''),
(1703148201, 'weekly', ''),
(1703148201, 'monthly', '');
UNLOCK TABLES;