-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mar. 15 oct. 2024 à 15:14
-- Version du serveur : 8.0.31
-- Version de PHP : 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `airport`
--

-- --------------------------------------------------------

--
-- Structure de la table `airlines`
--

DROP TABLE IF EXISTS `airlines`;
CREATE TABLE IF NOT EXISTS `airlines` (
  `carrier` char(2) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `faa` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`carrier`),
  KEY `faa` (`faa`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `airports`
--

DROP TABLE IF EXISTS `airports`;
CREATE TABLE IF NOT EXISTS `airports` (
  `faa` char(3) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `lat` float DEFAULT NULL,
  `lon` float DEFAULT NULL,
  `alt` int DEFAULT NULL,
  `tz` int DEFAULT NULL,
  `dst` char(1) DEFAULT NULL,
  `tzone` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`faa`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



DROP TABLE IF EXISTS `weathers`;
CREATE TABLE IF NOT EXISTS `weathers` (
  `origin` CHAR(3) NOT NULL,
  `year` INT NOT NULL,
  `month` INT NOT NULL,
  `day` INT NOT NULL,
  `hour` INT NOT NULL,
  `temp` FLOAT DEFAULT NULL,
  `dewp` FLOAT DEFAULT NULL,
  `humid` FLOAT DEFAULT NULL,
  `wind_dir` INT DEFAULT NULL,
  `wind_speed` FLOAT DEFAULT NULL,
  `wind_gust` FLOAT DEFAULT NULL,
  `precip` FLOAT DEFAULT NULL,
  `pressure` FLOAT DEFAULT NULL,
  `visib` FLOAT DEFAULT NULL,
  `time_hour` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`origin`, `year`, `month`, `day`, `hour`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `flights`
--

DROP TABLE IF EXISTS `flights`;
CREATE TABLE IF NOT EXISTS `flights` (
  `id` int NOT NULL AUTO_INCREMENT,
  `year` int DEFAULT NULL,
  `month` int DEFAULT NULL,
  `day` int DEFAULT NULL,
  `dep_time` varchar(4) DEFAULT NULL,
  `sched_dep_time` int DEFAULT NULL,
  `dep_delay` varchar(255) DEFAULT NULL,
  `arr_time` varchar(4) DEFAULT NULL,
  `sched_arr_time` int DEFAULT NULL,
  `arr_delay` varchar(255) DEFAULT NULL,
  `carrier` char(2) DEFAULT NULL,
  `flight` int DEFAULT NULL,
  `tailnum` char(6) DEFAULT NULL,
  `origin` char(3) DEFAULT NULL,
  `dest` char(3) DEFAULT NULL,
  `air_time` varchar(255) DEFAULT NULL,
  `distance` int DEFAULT NULL,
  `hour` int DEFAULT NULL,
  `minute` int DEFAULT NULL,
  `time_hour` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `carrier` (`carrier`),
  KEY `tailnum` (`tailnum`),
  KEY `origin` (`origin`),
  KEY `dest` (`dest`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `planes`
--

DROP TABLE IF EXISTS `planes`;
CREATE TABLE IF NOT EXISTS `planes` (
  `tailnum` char(6) NOT NULL,
  `year` float DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `manufacturer` varchar(255) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `engines` int DEFAULT NULL,
  `seats` int DEFAULT NULL,
  `speed` float DEFAULT NULL,
  `engine` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`tailnum`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
