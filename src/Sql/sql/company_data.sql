DROP DATABASE IF EXISTS company_data;

CREATE DATABASE `company_data`;
USE company_data;

CREATE TABLE `Company_employees` (
  `Employee_id` varchar(10) NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `Job_code` varchar(45) NOT NULL,
  `Job_title` varchar(45) DEFAULT NULL,
  `State_code` int DEFAULT NULL,
  `Home_state` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Employee_id`,`Job_code`)
);

INSERT INTO `Company_employees` (`Employee_id`,`Name`,`Job_code`,`Job_title`,`State_code`,`Home_state`) VALUES ('E001','Carmel','J01','Chef',26,'Cape Town');
INSERT INTO `Company_employees` (`Employee_id`,`Name`,`Job_code`,`Job_title`,`State_code`,`Home_state`) VALUES ('E001','Carmel','J02','Waiter',26,'Cape Town');
INSERT INTO `Company_employees` (`Employee_id`,`Name`,`Job_code`,`Job_title`,`State_code`,`Home_state`) VALUES ('E002','Stefanie','J02','Waiter',56,'Joburg');
INSERT INTO `Company_employees` (`Employee_id`,`Name`,`Job_code`,`Job_title`,`State_code`,`Home_state`) VALUES ('E002','Stefanie','J03','Bartender',56,'Joburg');
INSERT INTO `Company_employees` (`Employee_id`,`Name`,`Job_code`,`Job_title`,`State_code`,`Home_state`) VALUES ('E003','Lisa','J01','Chef',5,'Nairobi');

