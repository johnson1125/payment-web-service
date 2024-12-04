-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 22, 2024 at 09:03 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `payment_web_service`
--

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `paymentID` varchar(20) NOT NULL,
  `transactionID` varchar(16) NOT NULL,
  `paymentDateTime` datetime NOT NULL,
  `paymentMethod` varchar(21) NOT NULL,
  `paymentAmount` decimal(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payment`
--

INSERT INTO `payment` (`paymentID`, `transactionID`, `paymentDateTime`, `paymentMethod`, `paymentAmount`) VALUES
('PYM-TST-240922-00001', 'TST-240922-00001', '2024-09-22 14:18:10', 'Card Payment', 90),
('PYM-TST-240922-00002', 'TST-240922-00003', '2024-09-22 14:23:34', 'FPX', 100),
('PYM-TST-240922-00003', 'TST-240922-00004', '2024-09-22 14:26:03', 'TNG E-Wallet', 180),
('PYM-TST-240922-00004', 'TST-240922-00006', '2024-09-22 14:50:45', 'FPX', 90),
('PYM-TST-240922-00005', 'TST-240922-00007', '2024-09-22 14:51:37', 'Card Payment', 50),
('PYM-TST-240922-00006', 'TST-240922-00009', '2024-09-22 14:53:29', 'TNG E-Wallet', 180),
('PYM-TST-240922-00007', 'TST-240922-00012', '2024-09-22 15:00:29', 'TNG E-Wallet', 90),
('PYM-TST-240922-00008', 'TST-240922-00013', '2024-09-22 15:02:09', 'Card Payment', 50);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`paymentID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
