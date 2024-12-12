DROP DATABASE listado_trabajadores;

CREATE DATABASE `listado_trabajadores`;

USE `listado_trabajadores`;

CREATE TABLE `gender` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL
);

CREATE TABLE `role` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL
);

CREATE TABLE `department` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL
);

CREATE TABLE `area` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL
);

CREATE TABLE `job_title` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(60) NOT NULL
);

CREATE TABLE `relationship` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL
);

CREATE TABLE `user` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `username` varchar(50) UNIQUE NOT NULL,
  `email` varchar(80) UNIQUE NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` int NOT NULL
);

CREATE TABLE `user_info` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `id_user` int UNIQUE NOT NULL,
  `name` varchar(40) NOT NULL,
  `lastname` varchar(40) NOT NULL,
  `rut` varchar(12) NOT NULL,
  `gender` int NOT NULL,
  `direction` varchar(120) NOT NULL,
  `phone` varchar(20) NOT NULL,
  FOREIGN KEY (id_user) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE `user_info_work` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `id_user` int UNIQUE NOT NULL,
  `entry_date` date NOT NULL,
  `department` int NOT NULL,
  `area` int NOT NULL,
  `job_title` int NOT NULL,
  FOREIGN KEY (id_user) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE `user_emergency_contact` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `id_user` int NOT NULL,
  `name` varchar(80) NOT NULL,
  `relationship` int NOT NULL,
  `phone` varchar(20) NOT NULL,
  FOREIGN KEY (id_user) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE `family_responsibilities` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `id_user` int NOT NULL,
  `name` varchar(40) NOT NULL,
  `rut` varchar(12) NOT NULL,
  `relationship` int NOT NULL,
  `gender` int NOT NULL,
  FOREIGN KEY (id_user) REFERENCES user (id) ON DELETE CASCADE
);

ALTER TABLE `user` ADD FOREIGN KEY (`role`) REFERENCES `role` (`id`);

ALTER TABLE `user_info` ADD FOREIGN KEY (`gender`) REFERENCES `gender` (`id`);

ALTER TABLE `user_info_work` ADD FOREIGN KEY (`department`) REFERENCES `department` (`id`);

ALTER TABLE `user_info_work` ADD FOREIGN KEY (`area`) REFERENCES `area` (`id`);

ALTER TABLE `user_info_work` ADD FOREIGN KEY (`job_title`) REFERENCES `job_title` (`id`);

ALTER TABLE `user_emergency_contact` ADD FOREIGN KEY (`relationship`) REFERENCES `relationship` (`id`);

ALTER TABLE `family_responsibilities` ADD FOREIGN KEY (`relationship`) REFERENCES `relationship` (`id`);

ALTER TABLE `family_responsibilities` ADD FOREIGN KEY (`gender`) REFERENCES `gender` (`id`);

-- Añadiendo datos de iniciales
INSERT INTO `gender` (name)
VALUES ("Male"), ("Famele");

INSERT INTO `relationship` (name)
VALUES ("Father"), ("Mother"), ("Son / Daughter"), ("Husband / Wife"), ("Brother / Sister"), ("Friend"), ("Other");

INSERT INTO `role` (name)
VALUES ("admin"), ("HR Manager"), ("HR Staff"), ("Employee");

INSERT INTO `job_title` (name)
VALUES ("Software Develoepr"), ("Warehouse Assistant"), ("Sales Executive"), ("Marketing Specialist");

INSERT INTO `area` (name)
VALUES ("Information Technology (IT)"), ("Logistics / Warehouse"), ("Sales"), ("Marketing");

INSERT INTO `department` (name)
VALUES ("IT Department"), ("Operations Department"), ("Customer Support Department"), ("Marketing Department");

-- Usuario admin por defecto user: admin, pass: admin
INSERT INTO user (username, email, password, role) 
VALUES ("admin", "admin@example.com", "$2b$10$KkkiQSlM6G99P/qov2Hv/eX/zECOYL3FnvHTWnmcpO18b9VJyNprO", (select id from role where name = "admin"));