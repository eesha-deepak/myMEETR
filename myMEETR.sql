DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS time_zone;
DROP TABLE IF EXISTS meeting_details;
DROP TABLE IF EXISTS availability_info;
DROP TABLE IF EXISTS link_meeting;
DROP TABLE IF EXISTS attendee_info;
DROP TABLE IF EXISTS importance;

CREATE TABLE IF NOT EXISTS `person` (
  `person_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `time_zone_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`person_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `person`
--

INSERT INTO `person` (`person_id`, `first_name`, `last_name`, `time_zone_name`, `email`) VALUES
(1, 'John', 'Wilcox', 'EDT', 'jwilcox@purdue.edu'),
(2, 'Will', 'Smith', 'PDT', 'wsmith@purdue.edu'),
(3, 'Xavier', 'Cunningham', 'JST', 'xcunningham@purdue.edu'),
(4, 'Bernard', 'Stevenson', 'IST', 'bstevenson@purdue.edu'),
(5, 'Jolie', 'Baker', 'CDT', 'jbaker@purdue.edu'),
(6, 'Christie', 'Tate', 'CST', 'ctate@purdue.edu');

-- --------------------------------------------------------

--
-- Table structure for table `time_zone`
--

CREATE TABLE IF NOT EXISTS `time_zone` (
  `name` varchar(50) NOT NULL,
  `offset` decimal(4,2) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `time_zone`
--

INSERT INTO `time_zone` (`name`, `offset`) VALUES
('LINT', 14),
('CHADT', 13.75),
('NZDT', 13),
('ANAT', 12),
('AEDT', 11),
('ACDT', 10.5),
('AEST', 10),
('ACST', 9.5),
('JST', 9),
('ACWST', 8.75),
('CST', 8),
('WIB', 7),
('MMT', 6.5),
('BST', 6),
('NPT', 5.75),
('IST', 5.5),
('UZT', 5),
('AFT', 4.5),
('GST', 4),
('IRDT', 4.5),
('MSK', 3),
('EET', 2),
('CET', 1),
('GMT', 0),
('CVT', -1),
('NDT', -2.5),
('ART', -3),
('EDT', -4),
('CDT', -5),
('PDT', -7),
('AKDT', -8),
('HDT', -9),
('MART', -9.5),
('HST', -10),
('NUT', -11),
('AoE', -12);


-- --------------------------------------------------------

--
-- Table structure for table `meeting_details`
--

CREATE TABLE IF NOT EXISTS `meeting_details` (
  `meeting_id` int(11) NOT NULL,
  `in_person` tinyint(4) NOT NULL,
  `online` tinyint(4) NOT NULL,
  `start_day` date NOT NULL,
  `end_day` date NOT NULL,
  `length_hr` decimal(4,2) NOT NULL,
  `description` varchar(200) DEFAULT NULL,
  `creator_id` int(11) NOT NULL REFERENCES person(person_id),
  PRIMARY KEY (`meeting_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `meeting_details`
--

INSERT INTO `meeting_details` (`meeting_id`, `in_person`, `online`, `start_day`, `end_day`, `length_hr`, `description`, `creator_id`) VALUES
(1, 0, 1, '2021-04-20', '2021-04-25', 2, "Pitching project", 1),
(2, 0, 1, '2021-03-24', '2021-03-25', 2.5, "Progress update", 5),
(3, 0, 1, '2021-04-04', '2021-04-15', 3, "Demo project", 6),
(4, 1, 0, '2021-04-10', '2021-04-13', 1, "", 6);

-- --------------------------------------------------------

--
-- Table structure for table `link_meeting`
--

CREATE TABLE IF NOT EXISTS `link_meeting` (
	`availability_id` int(11) NOT NULL,
  `person_id` int(11) NOT NULL REFERENCES person(person_id),
  `meeting_id` int(11) NOT NULL REFERENCES meeting_details(meeting_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `link_meeting`
--

INSERT INTO `link_meeting` (`availability_id`, `person_id`, `meeting_id`) VALUES
(1, 1, 1),
(2, 1, 1),
(3, 1, 1),
(1, 2, 1),
(1, 3, 1),
(2, 4, 1),
(4, 4, 2),
(5, 4, 2),
(5, 5, 2),
(5, 6, 2),
(6, 6, 2);

-- --------------------------------------------------------

--
-- Table structure for table `availability_info`
--

CREATE TABLE IF NOT EXISTS `availability_info` (
	`availability_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(50) NOT NULL,
  `start_time` varchar(50) NOT NULL,
  `end_time` varchar(50) NOT NULL,
  PRIMARY KEY (`availability_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `availability_info`
--

INSERT INTO `availability_info` (`availability_id`, `date`, `start_time`, `end_time`) VALUES
(1, '2021-04-20', '8:00:00', '10:00:00'),
(2, '2021-04-20', '7:00:00', '9:00:00'),
(3, '2021-04-22', '7:00:00', '9:00:00'),
(4, '2021-03-24', '7:00:00', '9:30:00'),
(5, '2021-03-24', '7:30:00', '10:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `attendee_info`
--

CREATE TABLE IF NOT EXISTS `attendee_info` (
  `person_id` int(11) NOT NULL,
  `meeting_id` int(11) NOT NULL,
  `meeting_role` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `attendee_info`
--

INSERT INTO `attendee_info` (`person_id`, `meeting_id`, `meeting_role`) VALUES
(1, 1, 'Coordinator'),
(2, 1, 'Guest Speaker'),
(3, 1, 'Recorder'),
(4, 1, 'Presenter'),
(5, 2, 'Coordinator'),
(6, 2, 'Attendee'),
(4, 2, 'Presenter');

-- --------------------------------------------------------

--
-- Table structure for table `importance`
--

CREATE TABLE IF NOT EXISTS `importance` (
	`meeting_role` varchar(50) NOT NULL,
  `importance_level` int(11) NOT NULL,
  PRIMARY KEY (`meeting_role`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `importance`
--

INSERT INTO `importance` (`meeting_role`, `importance_level`) VALUES
('Coordinator', 1),
('Guest Speaker', 2),
('Presenter', 3),
('Recorder', 4),
('Attendee', 5);
