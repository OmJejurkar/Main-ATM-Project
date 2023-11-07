-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 27, 2023 at 06:14 AM
-- Server version: 8.0.34
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `atmdatabase`
--

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `ID` int NOT NULL,
  `UserId` int NOT NULL,
  `Time` datetime NOT NULL,
  `Transaction_type` varchar(100) NOT NULL,
  `Transaction_amt` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`ID`, `UserId`, `Time`, `Transaction_type`, `Transaction_amt`) VALUES
(1, 2, '2023-08-20 10:19:22', 'withdraw', 100);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `ID` int NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Balance` int NOT NULL,
  `Pin` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `SecQuestion` varchar(100) NOT NULL,
  `SecAnswer` varchar(100) NOT NULL,
  `OTP` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`ID`, `Name`, `Balance`, `Pin`, `Email`, `SecQuestion`, `SecAnswer`, `OTP`) VALUES
(1, 'Harshada Jejurkar', 10000, 'c4dedb9a70293c16a09e8587e4782fb31459aedcff9a7e90fe', 'harshadajejurkar403@gmail.com', 'Bday', '2404', 0),
(2, 'Om Jejurkar', 9900, 'c4dedb9a70293c16a09e8587e4782fb31459aedcff9a7e90fef6565379fa0afa', 'jejurkarom@gmail.com', 'Bday', '2401', 6871);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `transaction`
--
ALTER TABLE `transaction`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
