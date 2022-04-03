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
-- Database: `freelancers`
--
CREATE DATABASE IF NOT EXISTS `freelancers` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `freelancers`;

-- --------------------------------------------------------

--
-- Table structure for table `freelancers`
--

DROP TABLE IF EXISTS `freelancers`;
CREATE TABLE IF NOT EXISTS `freelancers` (
  `freelancerID` int(6) NOT NULL,
  `name` varchar(64) NOT NULL,
  `phone` int(8) NOT NULL DEFAULT 0,
  PRIMARY KEY (`freelancerID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `freelancers`
--
INSERT INTO `freelancers` (`freelancerID`, `name`, `phone`) VALUES
(1000, 'Bob Toh', '98765432');

INSERT INTO `freelancers` (`freelancerID`, `name`, `phone`) VALUES
(1001, 'Sarah Tan', '84652345');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
