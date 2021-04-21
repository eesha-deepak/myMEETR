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
(6, 'Christie', 'Tate', 'CST', 'ctate@purdue.edu'),
(7, 'Raveena', 'Gupta', 'PDT', 'rgupta@purdue.edu'),
(8, 'Koa', 'Kahele', 'HST', 'kkahele@purdue.edu'),
(9, 'Lucy', 'Winters', 'GMT', 'lwinters@purdue.edu'),
(10, 'Aditya', 'Kapoor', 'IST', 'akapoor@purdue.edu'),
(11, 'Emily', 'Huang', 'CST', 'ehuang@purdue.edu'),
(12, 'Dana', 'Darsh', 'IRDT', 'ddarsh@purdue.edu'),
(13, 'Jessica', 'Brown', 'AEDT', 'jbrown@purdue.edu'),
(14, 'Neha', 'Patel', 'NPT', 'npatel@purdue.edu'),
(15, 'Igor', 'Karkaroff', 'MSK', 'ikarkaroff@purdue.edu'),
(16, 'Carlos', 'Santos', 'GST', 'csantos@purdue.edu'),
(17, 'Aryan', 'Abbasi', 'UZT', 'aabbasi@purdue.edu'),
(18, 'Ark', 'Macintosh', 'HDT', 'amacintosh@purdue.edu'),
(19, 'Felicity', 'Weathers', 'EDT', 'fweathers@purdue.edu'),
(20, 'Oliver', 'Stone', 'EDT', 'ostone@purdue.edu');

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
(1, 0, 1, '2021-04-20', '2021-04-25', 2, "Pitching project", 2),
(2, 0, 1, '2021-03-24', '2021-03-25', 2.5, "Progress update", 5),
(3, 0, 1, '2021-04-04', '2021-04-15', 3, "Demo project", 6),
(4, 1, 0, '2021-04-10', '2021-04-13', 1, "", 6),
(5, 1, 0, '2021-04-12', '2021-04-16', 0.5, "Sprint review", 12),
(6, 1, 0, '2021-04-14', '2021-04-15', 2, "Assign tasks and explain proj", 13),
(7, 1, 0, '2021-04-23', '2021-04-23', 4, "Create presention", 18);

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
(2, 2, 1),
(3, 2, 1),
(4, 14, 2),
(5, 15, 2);

-- --------------------------------------------------------

--
-- Table structure for table `availability_info`
--

CREATE TABLE IF NOT EXISTS `availability_info` (
	`availability_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  PRIMARY KEY (`availability_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `availability_info`
--

INSERT INTO `availability_info` (`availability_id`, `date`, `start_time`, `end_time`) VALUES
(1, '2021-04-20', '08:00:00', '10:00:00'),
(2, '2021-04-20', '07:00:00', '09:00:00'),
(3, '2021-04-22', '07:00:00', '09:00:00'),
(4, '2021-03-24', '07:00:00', '09:30:00'),
(5, '2021-03-24', '07:30:00', '10:00:00');

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
(1, 4, 'Coordinator'),
(2, 2, 'Presenter'),
(3, 7, 'Coordinator'),
(4, 7, 'Guest Speaker'),
(5, 1, 'Attendee'),
(6, 3, 'Presenter'),
(7, 2,'Attendee'),
(8, 6, 'Attendee'),
(9, 1, 'Coordinator'),
(10, 3, 'Coordinator'),
(11, 7, 'Attendee'),
(12, 5, 'Recorder'),
(13, 1, 'Attendee'),
(14, 4, 'Attendee'),
(15, 6, 'Coordinator'),
(16, 1, 'Attendee'),
(17, 6, 'Presenter'),
(18, 2, 'Coordinator'),
(19, 5,'Coordinator'),
(20, 2, 'Guest Speaker');

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