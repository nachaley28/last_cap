-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 03, 2025 at 04:11 PM
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
-- Database: `labguard`
--

-- --------------------------------------------------------

--
-- Table structure for table `computer_equipments`
--

CREATE TABLE `computer_equipments` (
  `pc_name` varchar(50) DEFAULT NULL,
  `lab_name` varchar(100) DEFAULT NULL,
  `specs` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`specs`)),
  `id` varchar(255) NOT NULL,
  `lab_id` int(11) NOT NULL,
  `other_parts` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `computer_equipments`
--

INSERT INTO `computer_equipments` (`pc_name`, `lab_name`, `specs`, `id`, `lab_id`, `other_parts`) VALUES
('1', '1', '{\"hdmi\": \"1\", \"headphone\": \"1\", \"keyboard\": \"1\", \"monitor\": \"1\", \"mouse\": \"1\", \"power\": \"1\", \"systemUnit\": \"1\", \"wifi\": \"1\"}', '92509786', 5, '{\"Pencil\": \"1\", \"paper\": \"4\"}'),
('2', '1', '{\"monitor\":2,\"systemUnit\":2,\"keyboard\":2,\"mouse\":2,\"headphone\":2,\"hdmi\":2,\"power\":2,\"wifi\":2}', '95434437', 0, NULL),
('3', '1', '{\"monitor\":3,\"systemUnit\":3,\"keyboard\":3,\"mouse\":3,\"headphone\":3,\"hdmi\":3,\"power\":3,\"wifi\":3}', '85840580', 0, NULL),
('4', '1', '{\"monitor\":4,\"systemUnit\":4,\"keyboard\":4,\"mouse\":4,\"headphone\":4,\"hdmi\":4,\"power\":4,\"wifi\":4}', '78615636', 0, NULL),
('5', '1', '{\"monitor\":5,\"systemUnit\":5,\"keyboard\":5,\"mouse\":5,\"headphone\":5,\"hdmi\":5,\"power\":5,\"wifi\":5}', '96618844', 0, NULL),
('6', '1', '{\"monitor\":6,\"systemUnit\":6,\"keyboard\":6,\"mouse\":6,\"headphone\":6,\"hdmi\":6,\"power\":6,\"wifi\":6}', '54639076', 0, NULL),
('7', '1', '{\"monitor\":7,\"systemUnit\":7,\"keyboard\":7,\"mouse\":7,\"headphone\":7,\"hdmi\":7,\"power\":7,\"wifi\":7}', '88983715', 0, NULL),
('8', '1', '{\"monitor\":8,\"systemUnit\":8,\"keyboard\":8,\"mouse\":8,\"headphone\":8,\"hdmi\":8,\"power\":8,\"wifi\":8}', '92410724', 0, NULL),
('9', '1', '{\"monitor\":9,\"systemUnit\":9,\"keyboard\":9,\"mouse\":9,\"headphone\":9,\"hdmi\":9,\"power\":9,\"wifi\":9}', '38119435', 0, NULL),
('10', '1', '{\"monitor\":10,\"systemUnit\":10,\"keyboard\":10,\"mouse\":10,\"headphone\":10,\"hdmi\":10,\"power\":10,\"wifi\":10}', '72984978', 0, NULL),
('11', '1', '{\"monitor\":11,\"systemUnit\":11,\"keyboard\":11,\"mouse\":11,\"headphone\":11,\"hdmi\":11,\"power\":11,\"wifi\":11}', '84732688', 0, NULL),
('12', '1', '{\"monitor\":12,\"systemUnit\":12,\"keyboard\":12,\"mouse\":12,\"headphone\":12,\"hdmi\":12,\"power\":12,\"wifi\":12}', '58305685', 0, NULL),
('13', '1', '{\"monitor\":13,\"systemUnit\":13,\"keyboard\":13,\"mouse\":13,\"headphone\":13,\"hdmi\":13,\"power\":13,\"wifi\":13}', '84643061', 0, NULL),
('14', '1', '{\"monitor\":14,\"systemUnit\":14,\"keyboard\":14,\"mouse\":14,\"headphone\":14,\"hdmi\":14,\"power\":14,\"wifi\":14}', '88379069', 0, NULL),
('15', '1', '{\"monitor\":15,\"systemUnit\":15,\"keyboard\":15,\"mouse\":15,\"headphone\":15,\"hdmi\":15,\"power\":15,\"wifi\":15}', '98956984', 0, NULL),
('16', '1', '{\"monitor\":16,\"systemUnit\":16,\"keyboard\":16,\"mouse\":16,\"headphone\":16,\"hdmi\":16,\"power\":16,\"wifi\":16}', '96583659', 0, NULL),
('17', '1', '{\"monitor\":17,\"systemUnit\":17,\"keyboard\":17,\"mouse\":17,\"headphone\":17,\"hdmi\":17,\"power\":17,\"wifi\":17}', '13381193', 0, NULL),
('18', '1', '{\"monitor\":18,\"systemUnit\":18,\"keyboard\":18,\"mouse\":18,\"headphone\":18,\"hdmi\":18,\"power\":18,\"wifi\":18}', '55583196', 0, NULL),
('19', '1', '{\"monitor\":19,\"systemUnit\":19,\"keyboard\":19,\"mouse\":19,\"headphone\":19,\"hdmi\":19,\"power\":19,\"wifi\":19}', '73692576', 0, NULL),
('20', '1', '{\"monitor\":20,\"systemUnit\":20,\"keyboard\":20,\"mouse\":20,\"headphone\":20,\"hdmi\":20,\"power\":20,\"wifi\":20}', '81399398', 0, NULL),
('21', '1', '{\"monitor\":21,\"systemUnit\":21,\"keyboard\":21,\"mouse\":21,\"headphone\":21,\"hdmi\":21,\"power\":21,\"wifi\":21}', '44597170', 0, NULL),
('22', '1', '{\"monitor\":22,\"systemUnit\":22,\"keyboard\":22,\"mouse\":22,\"headphone\":22,\"hdmi\":22,\"power\":22,\"wifi\":22}', '22522516', 0, NULL),
('23', '1', '{\"monitor\":23,\"systemUnit\":23,\"keyboard\":23,\"mouse\":23,\"headphone\":23,\"hdmi\":23,\"power\":23,\"wifi\":23}', '16317188', 0, NULL),
('24', '1', '{\"monitor\":24,\"systemUnit\":24,\"keyboard\":24,\"mouse\":24,\"headphone\":24,\"hdmi\":24,\"power\":24,\"wifi\":24}', '17947368', 0, NULL),
('25', '1', '{\"monitor\":25,\"systemUnit\":25,\"keyboard\":25,\"mouse\":25,\"headphone\":25,\"hdmi\":25,\"power\":25,\"wifi\":25}', '35121963', 0, NULL),
('26', '1', '{\"monitor\":26,\"systemUnit\":26,\"keyboard\":26,\"mouse\":26,\"headphone\":26,\"hdmi\":26,\"power\":26,\"wifi\":26}', '61962110', 0, NULL),
('27', '1', '{\"monitor\":27,\"systemUnit\":27,\"keyboard\":27,\"mouse\":27,\"headphone\":27,\"hdmi\":27,\"power\":27,\"wifi\":27}', '21290591', 0, NULL),
('28', '1', '{\"monitor\":28,\"systemUnit\":28,\"keyboard\":28,\"mouse\":28,\"headphone\":28,\"hdmi\":28,\"power\":28,\"wifi\":28}', '65425228', 0, NULL),
('29', '1', '{\"monitor\":29,\"systemUnit\":29,\"keyboard\":29,\"mouse\":29,\"headphone\":29,\"hdmi\":29,\"power\":29,\"wifi\":29}', '97781019', 0, NULL),
('30', '1', '{\"monitor\":30,\"systemUnit\":30,\"keyboard\":30,\"mouse\":30,\"headphone\":30,\"hdmi\":30,\"power\":30,\"wifi\":30}', '70095415', 0, NULL),
('31', '1', '{\"monitor\":31,\"systemUnit\":31,\"keyboard\":31,\"mouse\":31,\"headphone\":31,\"hdmi\":31,\"power\":31,\"wifi\":31}', '19412366', 0, NULL),
('32', '1', '{\"monitor\":32,\"systemUnit\":32,\"keyboard\":32,\"mouse\":32,\"headphone\":32,\"hdmi\":32,\"power\":32,\"wifi\":32}', '59772518', 0, NULL),
('33', '1', '{\"monitor\":33,\"systemUnit\":33,\"keyboard\":33,\"mouse\":33,\"headphone\":33,\"hdmi\":33,\"power\":33,\"wifi\":33}', '15442232', 0, NULL),
('34', '1', '{\"monitor\":34,\"systemUnit\":34,\"keyboard\":34,\"mouse\":34,\"headphone\":34,\"hdmi\":34,\"power\":34,\"wifi\":34}', '47808657', 0, NULL),
('35', '1', '{\"monitor\":35,\"systemUnit\":35,\"keyboard\":35,\"mouse\":35,\"headphone\":35,\"hdmi\":35,\"power\":35,\"wifi\":35}', '42115859', 0, NULL),
('36', '1', '{\"monitor\":36,\"systemUnit\":36,\"keyboard\":36,\"mouse\":36,\"headphone\":36,\"hdmi\":36,\"power\":36,\"wifi\":36}', '35621167', 0, NULL),
('37', '1', '{\"monitor\":37,\"systemUnit\":37,\"keyboard\":37,\"mouse\":37,\"headphone\":37,\"hdmi\":37,\"power\":37,\"wifi\":37}', '44456137', 0, NULL),
('38', '1', '{\"monitor\":38,\"systemUnit\":38,\"keyboard\":38,\"mouse\":38,\"headphone\":38,\"hdmi\":38,\"power\":38,\"wifi\":38}', '87893281', 0, NULL),
('39', '1', '{\"monitor\":39,\"systemUnit\":39,\"keyboard\":39,\"mouse\":39,\"headphone\":39,\"hdmi\":39,\"power\":39,\"wifi\":39}', '86778690', 0, NULL),
('40', '1', '{\"monitor\":40,\"systemUnit\":40,\"keyboard\":40,\"mouse\":40,\"headphone\":40,\"hdmi\":40,\"power\":40,\"wifi\":40}', '15150694', 0, NULL),
('41', '1', '{\"monitor\":41,\"systemUnit\":41,\"keyboard\":41,\"mouse\":41,\"headphone\":41,\"hdmi\":41,\"power\":41,\"wifi\":41}', '11793746', 0, NULL),
('42', '1', '{\"monitor\":42,\"systemUnit\":42,\"keyboard\":42,\"mouse\":42,\"headphone\":42,\"hdmi\":42,\"power\":42,\"wifi\":42}', '83322696', 0, NULL),
('43', '1', '{\"monitor\":43,\"systemUnit\":43,\"keyboard\":43,\"mouse\":43,\"headphone\":43,\"hdmi\":43,\"power\":43,\"wifi\":43}', '26266124', 0, NULL),
('44', '1', '{\"monitor\":44,\"systemUnit\":44,\"keyboard\":44,\"mouse\":44,\"headphone\":44,\"hdmi\":44,\"power\":44,\"wifi\":44}', '30640931', 0, NULL),
('45', '1', '{\"monitor\":45,\"systemUnit\":45,\"keyboard\":45,\"mouse\":45,\"headphone\":45,\"hdmi\":45,\"power\":45,\"wifi\":45}', '82527457', 0, NULL),
('46', '1', '{\"monitor\":46,\"systemUnit\":46,\"keyboard\":46,\"mouse\":46,\"headphone\":46,\"hdmi\":46,\"power\":46,\"wifi\":46}', '44968157', 0, NULL),
('47', '1', '{\"monitor\":47,\"systemUnit\":47,\"keyboard\":47,\"mouse\":47,\"headphone\":47,\"hdmi\":47,\"power\":47,\"wifi\":47}', '69617189', 0, NULL),
('48', '1', '{\"monitor\":48,\"systemUnit\":48,\"keyboard\":48,\"mouse\":48,\"headphone\":48,\"hdmi\":48,\"power\":48,\"wifi\":48}', '28387762', 0, NULL),
('49', '1', '{\"monitor\":49,\"systemUnit\":49,\"keyboard\":49,\"mouse\":49,\"headphone\":49,\"hdmi\":49,\"power\":49,\"wifi\":49}', '82066825', 0, NULL),
('50', '1', '{\"monitor\":50,\"systemUnit\":50,\"keyboard\":50,\"mouse\":50,\"headphone\":50,\"hdmi\":50,\"power\":50,\"wifi\":50}', '27535495', 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `computer_status`
--

CREATE TABLE `computer_status` (
  `com_id` text NOT NULL DEFAULT 'operational',
  `hdmi` text NOT NULL DEFAULT 'operational',
  `headphone` text NOT NULL DEFAULT 'operational',
  `keyboard` text NOT NULL DEFAULT 'operational',
  `monitor` text NOT NULL DEFAULT 'operational',
  `mouse` text NOT NULL DEFAULT 'operational',
  `power` text NOT NULL DEFAULT 'operational',
  `systemUnit` text NOT NULL DEFAULT 'operational',
  `wifi` text NOT NULL DEFAULT 'operational',
  `status_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `computer_status`
--

INSERT INTO `computer_status` (`com_id`, `hdmi`, `headphone`, `keyboard`, `monitor`, `mouse`, `power`, `systemUnit`, `wifi`, `status_id`) VALUES
('92509786', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 92781535),
('95434437', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 28270175),
('85840580', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 19569528),
('78615636', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 18181231),
('96618844', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 70453783),
('54639076', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 23159496),
('88983715', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 50047507),
('92410724', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 13337883),
('38119435', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 98667402),
('72984978', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 83497631),
('84732688', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 40838818),
('58305685', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 89928860),
('84643061', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 92030191),
('88379069', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 82086475),
('98956984', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 80576174),
('96583659', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 53178397),
('13381193', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 56362067),
('55583196', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 45834715),
('73692576', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 24107207),
('81399398', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 64216991),
('44597170', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 19036121),
('22522516', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 19154233),
('16317188', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 42148818),
('17947368', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 90010642),
('35121963', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 68325026),
('61962110', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 83838562),
('21290591', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 39915209),
('65425228', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 11899256),
('97781019', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 65264106),
('70095415', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 97416819),
('19412366', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 71741223),
('59772518', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 76923886),
('15442232', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 53141302),
('47808657', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 61375881),
('42115859', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 88367619),
('35621167', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 11171949),
('44456137', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 79248823),
('87893281', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 43158722),
('86778690', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 24641491),
('15150694', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 40567085),
('11793746', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 31952650),
('83322696', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 26329436),
('26266124', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 79969832),
('30640931', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 72342745),
('82527457', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 55887367),
('44968157', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 69936545),
('69617189', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 33516615),
('28387762', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 39457672),
('82066825', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 56647089),
('27535495', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 'operational', 18157592);

-- --------------------------------------------------------

--
-- Table structure for table `laboratory`
--

CREATE TABLE `laboratory` (
  `lab_id` int(11) NOT NULL,
  `lab_name` text NOT NULL,
  `location` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `laboratory`
--

INSERT INTO `laboratory` (`lab_id`, `lab_name`, `location`) VALUES
(5, '1', 'CL1');

-- --------------------------------------------------------

--
-- Table structure for table `other_part_status`
--

CREATE TABLE `other_part_status` (
  `com_id` int(11) NOT NULL,
  `parts` varchar(255) NOT NULL,
  `status_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `other_part_status`
--

INSERT INTO `other_part_status` (`com_id`, `parts`, `status_id`) VALUES
(92509786, '{\"Pencil\": \"operational\", \"paper\": \"operational\"}', 92781535);

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `id` int(11) NOT NULL,
  `com_id` varchar(50) DEFAULT NULL,
  `part` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `lab` varchar(100) DEFAULT NULL,
  `submitted_by` varchar(100) DEFAULT 'System',
  `notes` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `sent` tinyint(1) NOT NULL DEFAULT 0,
  `solution_done` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `technician_logs`
--

CREATE TABLE `technician_logs` (
  `report_id` text NOT NULL,
  `fix_id` text NOT NULL,
  `issue_found` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `solution` text NOT NULL,
  `status` text NOT NULL,
  `technician_email` text NOT NULL,
  `fix_time` datetime NOT NULL DEFAULT current_timestamp(),
  `sent` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `technician_logs`
--

INSERT INTO `technician_logs` (`report_id`, `fix_id`, `issue_found`, `solution`, `status`, `technician_email`, `fix_time`, `sent`) VALUES
('488', '58757040', '{\'lab\': \'1\', \'PC_Number\': \'1\', \'status\': \'Damaged\', \'notes\': \'Other part Pencil issue detected\'}', 'Repaired', 'operational', '1@gmail.com', '2025-11-03 19:40:39', 0);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `lgid` varchar(50) NOT NULL,
  `name` text NOT NULL,
  `email` text NOT NULL,
  `role` text NOT NULL,
  `year` text DEFAULT NULL,
  `password` text NOT NULL,
  `profile` varchar(255) NOT NULL,
  `department` varchar(100) DEFAULT 'Not specified',
  `position` varchar(100) DEFAULT 'Not Specified'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`lgid`, `name`, `email`, `role`, `year`, `password`, `profile`, `department`, `position`) VALUES
('DEAN-12345678', 'Seth Nono', 'seth@gmail.com', 'Dean', NULL, '1', '462572679_1566813483918217_3611730803966493123_n.jpg', 'CITE', 'Dean'),
('24788795', 'ALARCON, NATALIE JENH M.', '123@gmail.com', 'Technician', 'NA', '123', '2024-06-13-222528538.jpeg', 'ITSD', 'ITSD'),
('41122886', 'Ryan Valeriam', 'rcvaleriano.ui@phinmaed.com', 'CL Advisor', 'NA', '1234', 'ryan.jpg', 'CITE Department', 'Admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `laboratory`
--
ALTER TABLE `laboratory`
  ADD PRIMARY KEY (`lab_id`);

--
-- Indexes for table `other_part_status`
--
ALTER TABLE `other_part_status`
  ADD PRIMARY KEY (`com_id`,`parts`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `laboratory`
--
ALTER TABLE `laboratory`
  MODIFY `lab_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=489;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
