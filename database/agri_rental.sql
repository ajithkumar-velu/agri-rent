-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 01, 2024 at 12:27 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `agri_rental`
--

-- --------------------------------------------------------

--
-- Table structure for table `ar_admin`
--

CREATE TABLE `ar_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ar_admin`
--

INSERT INTO `ar_admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `ar_booking`
--

CREATE TABLE `ar_booking` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `provider` varchar(20) NOT NULL,
  `vid` int(11) NOT NULL,
  `duration` int(11) NOT NULL,
  `time_type` int(11) NOT NULL,
  `req_date` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `pay_st` int(11) NOT NULL,
  `transid` varchar(20) NOT NULL,
  `pdate` varchar(20) NOT NULL,
  `ptime` varchar(20) NOT NULL,
  `reviews` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ar_booking`
--

INSERT INTO `ar_booking` (`id`, `uname`, `provider`, `vid`, `duration`, `time_type`, `req_date`, `status`, `amount`, `pay_st`, `transid`, `pdate`, `ptime`, `reviews`) VALUES
(1, 'dinesh', 'ramesh', 2, 2, 2, '2024-06-01', 2, 700, 0, '434343434', '01-06-2024', '17:56:20', 'super');

-- --------------------------------------------------------

--
-- Table structure for table `ar_provider`
--

CREATE TABLE `ar_provider` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `district` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `account` varchar(20) NOT NULL,
  `gpay` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ar_provider`
--

INSERT INTO `ar_provider` (`id`, `name`, `address`, `district`, `mobile`, `email`, `uname`, `pass`, `create_date`, `status`, `account`, `gpay`) VALUES
(1, 'Ramesh', '57,ad st', 'Trichy', 9894442716, 'ramesh@gmail.com', 'ramesh', '123456', '08-02-2024', 1, '2200035611', 9894442716);

-- --------------------------------------------------------

--
-- Table structure for table `ar_user`
--

CREATE TABLE `ar_user` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `district` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ar_user`
--

INSERT INTO `ar_user` (`id`, `name`, `address`, `district`, `mobile`, `email`, `uname`, `pass`) VALUES
(1, 'Dinesh', '33,KS Nagar', 'Thanjavur', 9894442716, 'dinesh@gmail.com', 'dinesh', '123456');

-- --------------------------------------------------------

--
-- Table structure for table `ar_vehicle`
--

CREATE TABLE `ar_vehicle` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `vehicle` varchar(30) NOT NULL,
  `vno` varchar(20) NOT NULL,
  `details` varchar(100) NOT NULL,
  `cost1` int(11) NOT NULL,
  `cost2` int(11) NOT NULL,
  `photo` varchar(50) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ar_vehicle`
--

INSERT INTO `ar_vehicle` (`id`, `uname`, `vehicle`, `vno`, `details`, `cost1`, `cost2`, `photo`, `create_date`, `status`) VALUES
(1, 'ramesh', 'Tractor', 'TN2121', 'Fuel-Petrol, rotary cutters, cultivators', 40, 300, 'P1ag1.jpg', '08-02-2024', 0),
(2, 'ramesh', 'Tractor', 'TN2466', 'Fuel: Diesel, tiller, aerator, rotary cutters', 45, 350, 'P2ag5.jpg', '08-02-2024', 0);
