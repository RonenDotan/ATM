-- --------------------------------------------------------
-- Host:                         sql7.freesqldatabase.com
-- Server version:               5.5.62-0ubuntu0.14.04.1 - (Ubuntu)
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             11.0.0.6061
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for sql7638042
CREATE DATABASE IF NOT EXISTS `sql7638042` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `sql7638042`;

-- Dumping structure for table sql7638042.atm_funds
CREATE TABLE IF NOT EXISTS `atm_funds` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `funds` text COLLATE latin2_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin2 COLLATE=latin2_bin;

-- Dumping data for table sql7638042.atm_funds: ~1 rows (approximately)
/*!40000 ALTER TABLE `atm_funds` DISABLE KEYS */;
INSERT INTO `atm_funds` (`id`, `funds`) VALUES
	(1, '{"200.0":1 ,"100.0": 2, "20.0":5, "10.0":10,"5.0":10, "1.0": 10, "0.1": 1, "0.01":10}');
/*!40000 ALTER TABLE `atm_funds` ENABLE KEYS */;

-- Dumping structure for table sql7638042.constants
CREATE TABLE IF NOT EXISTS `constants` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `value_int` int(11) DEFAULT NULL,
  `value_decimal` decimal(10,5) DEFAULT NULL,
  `value_str` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- Dumping data for table sql7638042.constants: ~2 rows (approximately)
/*!40000 ALTER TABLE `constants` DISABLE KEYS */;
INSERT INTO `constants` (`id`, `name`, `value_int`, `value_decimal`, `value_str`) VALUES
	(1, 'MAX_WITHDRAWAL_AMOUNT', 2000, NULL, NULL),
	(2, 'MAX_COINS', 50, NULL, NULL);
/*!40000 ALTER TABLE `constants` ENABLE KEYS */;

-- Dumping structure for table sql7638042.fund_types
CREATE TABLE IF NOT EXISTS `fund_types` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `amount` decimal(10,5) unsigned NOT NULL,
  `type` enum('BILL','COIN') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `u` (`amount`,`type`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

-- Dumping data for table sql7638042.fund_types: ~9 rows (approximately)
/*!40000 ALTER TABLE `fund_types` DISABLE KEYS */;
INSERT INTO `fund_types` (`id`, `amount`, `type`) VALUES
	(9, 0.01000, 'COIN'),
	(8, 0.10000, 'COIN'),
	(7, 1.00000, 'COIN'),
	(6, 5.00000, 'COIN'),
	(5, 10.00000, 'COIN'),
	(4, 20.00000, 'BILL'),
	(3, 50.00000, 'BILL'),
	(2, 100.00000, 'BILL'),
	(1, 200.00000, 'BILL');
/*!40000 ALTER TABLE `fund_types` ENABLE KEYS */;

-- Dumping structure for table sql7638042.state_machine_flows
CREATE TABLE IF NOT EXISTS `state_machine_flows` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` tinyint(3) unsigned NOT NULL,
  `parameters` text,
  `description` text,
  `state` text,
  `time_started` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_state_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table sql7638042.state_machine_flows: ~0 rows (approximately)
/*!40000 ALTER TABLE `state_machine_flows` DISABLE KEYS */;
/*!40000 ALTER TABLE `state_machine_flows` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
