-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: 18 Mar, 2022
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
-- Database: `order`
--
CREATE DATABASE IF NOT EXISTS `jobs` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `jobs`;

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
CREATE TABLE IF NOT EXISTS `jobs` (
  `jobID` int(6) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `price` float(4,2) NOT NULL DEFAULT 0,
  `description` varchar(200) NOT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'NEW',
  `dateTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deadline` date NOT NULL,
  `pickUpLocation` varchar(1024) NOT NULL,
  `destination` varchar(1024) NOT NULL,
  `freelancerID` varchar(6),
  `distance` varchar(11) NOT NULL,
  PRIMARY KEY (`jobID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `jobs`
--
INSERT INTO `jobs` (`jobID`, `name`, `price`, `description`, `status`,`dateTime`, `deadline`, `pickUpLocation`,`destination`,`freelancerID`,`distance`) VALUES
(1, 'Baked Goods Delivery', '12.00', 'I need you to deliver 2 orders of cupcakes to the destination.', 'NEW', '2022-03-18 0:14:55', '2022-04-01', '520123 Simei Street 1 Blk 123 #02-07','510123 Pasir Ris Street 7 Blk 321 #07-02','F1','4.6 km');

INSERT INTO `jobs` (`jobID`, `name`, `price`, `description`, `status`,`dateTime`, `deadline`,`pickUpLocation`, `destination`, `freelancerID`,`distance`) VALUES (2, 'Brownies Delivery', '25.00', 'I need you to delivery 1 box of lemon pie to the destination, thanks!', 'NEW', '2022-03-19 19:38:11', '2022-04-01','520345 Bedok Street 2 Blk 345 #04-08', '600134 Jurong Street 10 Blk 134 #11-32', NULL,'30.6 km');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
