-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 06, 2014 at 11:44 AM
-- Server version: 5.5.29
-- PHP Version: 5.4.6-1ubuntu1.2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `sandyfiles`
--

-- --------------------------------------------------------

--
-- Table structure for table `attribute`
--

CREATE TABLE IF NOT EXISTS `attribute` (
  `attribid` bigint(100) NOT NULL AUTO_INCREMENT,
  `attrib_au` varchar(100) NOT NULL,
  `time` datetime NOT NULL,
  `new` int(1) NOT NULL DEFAULT '1',
  `downloded` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`attribid`),
  UNIQUE KEY `attrib_au` (`attrib_au`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=213 ;

-- --------------------------------------------------------

--
-- Table structure for table `links`
--

CREATE TABLE IF NOT EXISTS `links` (
  `id` bigint(255) NOT NULL AUTO_INCREMENT,
  `url` char(255) NOT NULL,
  `uid` bigint(255) NOT NULL,
  `binary_found` int(1) NOT NULL,
  `exploit_found` int(1) NOT NULL,
  `sucess` int(1) NOT NULL,
  `browser` int(1) NOT NULL DEFAULT '1',
  `java_version` int(1) NOT NULL DEFAULT '1',
  `reader` int(11) NOT NULL DEFAULT '1',
  `flash` int(11) NOT NULL DEFAULT '1',
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `sigscan` varchar(5000) NOT NULL,
  `infection_status` int(1) NOT NULL,
  `html` longblob NOT NULL,
  `ip` varchar(16) NOT NULL,
  `private` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1547 ;

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE IF NOT EXISTS `messages` (
  `msg_id` int(11) NOT NULL AUTO_INCREMENT,
  `msg` text,
  PRIMARY KEY (`msg_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

-- --------------------------------------------------------

--
-- Table structure for table `sas`
--

CREATE TABLE IF NOT EXISTS `sas` (
  `sas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

CREATE TABLE IF NOT EXISTS `test` (
  `sas` int(1) NOT NULL,
  `done` varchar(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `traffic`
--

CREATE TABLE IF NOT EXISTS `traffic` (
  `traffic_id` bigint(255) NOT NULL AUTO_INCREMENT,
  `urlid` bigint(255) NOT NULL,
  `request` varchar(500) NOT NULL,
  `response` text NOT NULL,
  `filetype` varchar(100) NOT NULL,
  PRIMARY KEY (`traffic_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=335 ;

-- --------------------------------------------------------

--
-- Table structure for table `traffic_links`
--

CREATE TABLE IF NOT EXISTS `traffic_links` (
  `traffic_id` bigint(255) NOT NULL AUTO_INCREMENT,
  `urlid` bigint(255) NOT NULL,
  `request` varchar(500) NOT NULL,
  `response` text NOT NULL,
  `filetype` varchar(500) NOT NULL,
  `html_source` mediumblob NOT NULL,
  PRIMARY KEY (`traffic_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=14186 ;

-- --------------------------------------------------------

--
-- Table structure for table `uploads`
--

CREATE TABLE IF NOT EXISTS `uploads` (
  `uploadid` int(11) NOT NULL AUTO_INCREMENT,
  `data` longblob,
  `filename` varchar(255) DEFAULT NULL,
  `filesize` int(11) DEFAULT NULL,
  `filetype` varchar(255) DEFAULT NULL,
  `done` int(1) DEFAULT NULL,
  `sigscan` text,
  `metascan` text NOT NULL,
  `md5` varchar(32) DEFAULT NULL,
  `fileinfo` text,
  `binaryfound` varchar(1) NOT NULL,
  `attribid` int(100) NOT NULL,
  `author` varchar(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `creadate` datetime NOT NULL,
  `moddate` datetime NOT NULL,
  `ctid` bigint(100) NOT NULL,
  `urls` varchar(1000) NOT NULL DEFAULT 'Nothing',
  `jar_type` int(1) NOT NULL DEFAULT '0',
  `jar_main_class` varchar(50) NOT NULL,
  `urlgen` int(1) NOT NULL DEFAULT '0',
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `sigscan2` text NOT NULL,
  `strings` mediumtext NOT NULL,
  `email` varchar(200) DEFAULT NULL,
  `private` int(1) NOT NULL DEFAULT '0',
  `ip` varchar(16) NOT NULL,
  PRIMARY KEY (`uploadid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=918 ;

-- --------------------------------------------------------

--
-- Table structure for table `urls`
--

CREATE TABLE IF NOT EXISTS `urls` (
  `id` bigint(255) NOT NULL AUTO_INCREMENT,
  `url` char(255) NOT NULL,
  `uid` bigint(255) NOT NULL,
  `binary_found` int(1) NOT NULL,
  `exploit_found` int(1) NOT NULL,
  `sucess` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=236 ;

-- --------------------------------------------------------

--
-- Table structure for table `zipfiles`
--

CREATE TABLE IF NOT EXISTS `zipfiles` (
  `id` bigint(255) NOT NULL AUTO_INCREMENT,
  `fname` char(100) NOT NULL,
  `md5` char(32) NOT NULL,
  `uid` int(10) NOT NULL,
  `filetype` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=42860 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
