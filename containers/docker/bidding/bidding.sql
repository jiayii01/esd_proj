-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bidding`
--
CREATE DATABASE IF NOT EXISTS `bidding` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `bidding`;

-- --------------------------------------------------------

--
-- Table structure for table `bidding`
--

DROP TABLE IF EXISTS `bidding`;
CREATE TABLE IF NOT EXISTS `bidding` (
  `biddingID` int(6) NOT NULL AUTO_INCREMENT,
  `userID` char(6) NOT NULL,
  `freelancerID` char(6)  NOT NULL,
  `jobID` int(6) NOT NULL,
`status` varchar(10) NOT NULL DEFAULT 'NEW',
  `dateTime` DATE NOT NULL,
  `price` float(4,2) NOT NULL DEFAULT 0,
  
  PRIMARY KEY (`biddingID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `bidding`
--

INSERT INTO `bidding` (`biddingID`, `userID`, `freelancerID`, `jobID`, `status`, `dateTime`, `price` ) VALUES
(245624, 'browniem', 'F2',2,'New','2022-03-19 19:38:11','25.00'),
(245625, 'curryi', 'F1',1,'New','2022-03-18 0:14:55','12.00'),
(245630, 'fishba', 'F1',8,'New','2022-03-18 0:14:55','20.00');

;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;