-- MySQL dump 10.16  Distrib 10.1.38-MariaDB, for debian-linux-gnueabihf (armv7l)
--
-- Host: localhost    Database: fcity
-- ------------------------------------------------------
-- Server version	10.1.38-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `data`
--

DROP TABLE IF EXISTS `data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ride_id` int(10) unsigned NOT NULL,
  `measure_id` int(10) unsigned NOT NULL,
  `value` double NOT NULL,
  `added_on` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`id`),
  KEY `data_ride_id_foreign` (`ride_id`),
  KEY `data_measure_id_foreign` (`measure_id`),
  CONSTRAINT `data_measure_id_foreign` FOREIGN KEY (`measure_id`) REFERENCES `measure` (`id`),
  CONSTRAINT `data_ride_id_foreign` FOREIGN KEY (`ride_id`) REFERENCES `ride` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data`
--

LOCK TABLES `data` WRITE;
/*!40000 ALTER TABLE `data` DISABLE KEYS */;
/*!40000 ALTER TABLE `data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measure`
--

DROP TABLE IF EXISTS `measure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `measure` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sensor_id` int(10) unsigned NOT NULL,
  `name` varchar(255) NOT NULL,
  `unit` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `measure_sensor_id_foreign` (`sensor_id`),
  CONSTRAINT `measure_sensor_id_foreign` FOREIGN KEY (`sensor_id`) REFERENCES `sensor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measure`
--

LOCK TABLES `measure` WRITE;
/*!40000 ALTER TABLE `measure` DISABLE KEYS */;
INSERT INTO `measure` VALUES (1,1,'speed','km/h','2019-05-13 08:35:23','2019-05-13 08:35:23'),(2,2,'voltage','V','2019-05-13 08:35:46','2019-05-13 08:35:46'),(3,2,'intensity','A','2019-05-13 08:35:58','2019-05-13 08:35:58'),(4,4,'lux1','lux','2019-05-17 08:49:32','2019-05-17 08:49:32'),(5,4,'lux2','lux','2019-05-17 08:49:38','2019-05-17 08:49:38'),(6,5,'acceleration','g','2019-05-17 08:50:22','2019-05-17 08:50:22'),(7,4,'lux3','lux','2019-05-21 14:16:24','2019-05-21 14:16:24');
/*!40000 ALTER TABLE `measure` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `migrations`
--

DROP TABLE IF EXISTS `migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `migrations` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `migration` varchar(255) NOT NULL,
  `batch` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `migrations`
--

LOCK TABLES `migrations` WRITE;
/*!40000 ALTER TABLE `migrations` DISABLE KEYS */;
/*!40000 ALTER TABLE `migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `password_resets`
--

DROP TABLE IF EXISTS `password_resets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `password_resets` (
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  KEY `password_resets_email_index` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_resets`
--

LOCK TABLES `password_resets` WRITE;
/*!40000 ALTER TABLE `password_resets` DISABLE KEYS */;
/*!40000 ALTER TABLE `password_resets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ride`
--

DROP TABLE IF EXISTS `ride`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ride` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `vehicle_id` int(10) unsigned NOT NULL,
  `start_reservation` datetime DEFAULT NULL,
  `end_reservation` datetime DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ride_user_id_foreign` (`user_id`),
  KEY `ride_vehicle_id_foreign` (`vehicle_id`),
  CONSTRAINT `ride_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `ride_vehicle_id_foreign` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ride`
--

LOCK TABLES `ride` WRITE;
/*!40000 ALTER TABLE `ride` DISABLE KEYS */;
INSERT INTO `ride` VALUES (7,1,1,'2019-05-13 14:33:00','2019-05-13 14:45:00','2019-05-13 14:34:59','2019-05-13 14:35:10','2019-05-13 12:32:47','2019-05-13 12:32:47'),(8,1,1,'2019-05-13 14:47:00','2019-05-13 15:00:00','2019-05-13 14:57:33','2019-05-13 14:57:47','2019-05-13 12:45:37','2019-05-13 12:45:37'),(9,1,1,'2019-05-13 16:30:00','2019-05-13 17:30:00','2019-05-13 17:26:40','2019-05-13 17:28:56','2019-05-13 14:31:20','2019-05-13 14:31:20'),(10,1,1,'2019-05-13 17:32:00','2019-05-13 19:00:00','2019-05-13 18:53:29','2019-05-13 18:53:46','2019-05-13 15:32:53','2019-05-13 15:32:53'),(11,2,1,'2019-05-15 09:00:00','2019-05-15 10:00:00','2019-05-15 09:32:10',NULL,'2019-05-15 07:03:59','2019-05-15 07:03:59'),(12,2,1,'2019-05-15 10:01:00','2019-05-15 11:00:00','2019-05-15 10:54:31','2019-05-15 10:55:16','2019-05-15 08:02:51','2019-05-15 08:02:51'),(14,2,1,'2019-05-15 11:01:00','2019-05-15 12:20:00','2019-05-15 11:13:36','2019-05-15 11:31:49','2019-05-15 09:01:31','2019-05-15 09:01:31'),(15,2,1,'2019-05-15 14:01:00','2019-05-15 14:55:00','2019-05-15 14:44:58','2019-05-15 14:55:35','2019-05-15 12:27:13','2019-05-15 12:27:13'),(16,1,1,'2019-05-15 15:10:00','2019-05-15 15:30:00','2019-05-15 15:12:16','2019-05-15 15:14:15','2019-05-15 13:11:56','2019-05-15 13:11:56'),(19,2,1,'2019-05-15 17:00:00','2019-05-15 19:00:00','2019-05-15 17:28:13','2019-05-15 18:36:32','2019-05-15 15:22:07','2019-05-15 15:23:04'),(20,2,1,'2019-05-15 19:05:00','2019-05-15 20:00:00','2019-05-15 19:57:19','2019-05-15 19:45:49','2019-05-15 17:37:28','2019-05-15 17:37:28'),(21,2,1,'2019-05-15 20:01:00','2019-05-15 21:00:00','2019-05-15 20:01:38','2019-05-15 20:06:10','2019-05-15 18:00:40','2019-05-15 18:01:07'),(22,1,1,'2019-05-16 09:30:00','2019-05-16 12:00:00','2019-05-16 11:57:00','2019-05-16 11:31:08','2019-05-16 07:31:22','2019-05-16 07:31:22'),(23,1,1,'2019-05-16 12:10:00','2019-05-16 12:20:00','2019-05-16 12:13:50',NULL,'2019-05-16 10:13:33','2019-05-16 10:13:33'),(24,1,1,'2019-05-16 13:35:00','2019-05-16 14:00:00','2019-05-16 13:37:31','2019-05-16 14:01:50','2019-05-16 11:35:28','2019-05-16 11:35:28'),(25,1,1,'2019-05-16 14:01:00','2019-05-16 14:59:00','2019-05-16 14:56:24','2019-05-16 14:56:24','2019-05-16 12:02:39','2019-05-16 12:02:39'),(26,1,1,'2019-05-16 15:05:00','2019-05-16 15:59:00','2019-05-16 15:27:17','2019-05-16 15:28:01','2019-05-16 13:06:59','2019-05-16 13:06:59'),(27,1,1,'2019-05-16 16:10:00','2019-05-16 17:00:00','2019-05-16 16:33:39','2019-05-16 17:44:29','2019-05-16 14:09:00','2019-05-16 14:09:00'),(28,1,1,'2019-05-17 11:05:00','2019-05-17 11:20:00','2019-05-17 11:11:59',NULL,'2019-05-17 09:05:14','2019-05-17 09:05:14'),(29,1,1,'2019-05-17 11:30:00','2019-05-17 11:45:00','2019-05-17 11:33:20',NULL,'2019-05-17 09:32:37','2019-05-17 09:32:37'),(30,1,1,'2019-05-17 11:58:00','2019-05-17 12:15:00','2019-05-17 12:13:30','2019-05-17 12:13:57','2019-05-17 09:58:49','2019-05-17 09:58:49'),(31,2,1,'2019-05-17 14:30:00','2019-05-17 15:40:00','2019-05-17 14:39:46','2019-05-17 15:36:52','2019-05-17 12:36:59','2019-05-17 12:36:59'),(32,1,1,'2019-05-17 16:30:00','2019-05-17 18:00:00','2019-05-17 17:22:53',NULL,'2019-05-17 14:25:46','2019-05-17 14:25:46'),(33,2,1,'2019-05-17 18:05:00','2019-05-17 19:05:00','2019-05-17 18:13:41','2019-05-17 18:53:41','2019-05-17 16:08:23','2019-05-17 16:08:23'),(34,1,1,'2019-05-20 09:50:00','2019-05-20 10:10:00','2019-05-20 09:53:14','2019-05-20 10:13:14','2019-05-20 07:49:49','2019-05-20 07:49:49'),(35,1,1,'2019-05-20 15:30:00','2019-05-20 18:00:00','2019-05-20 16:31:10','2019-05-20 16:34:03','2019-05-20 13:32:22','2019-05-20 13:32:22'),(36,1,1,'2019-05-21 10:45:00','2019-05-21 11:15:00','2019-05-21 11:00:09','2019-05-21 11:21:22','2019-05-21 08:45:23','2019-05-21 08:45:23'),(37,1,1,'2019-05-21 12:25:00','2019-05-21 12:45:00','2019-05-21 12:27:53','2019-05-21 12:28:28','2019-05-21 10:27:40','2019-05-21 10:27:40');
/*!40000 ALTER TABLE `ride` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor`
--

DROP TABLE IF EXISTS `sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sensor` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor`
--

LOCK TABLES `sensor` WRITE;
/*!40000 ALTER TABLE `sensor` DISABLE KEYS */;
INSERT INTO `sensor` VALUES (1,'GPS','2019-05-13 08:33:52','2019-05-13 08:33:52'),(2,'battery','2019-05-13 08:34:02','2019-05-13 08:34:02'),(4,'luxmeter','2019-05-17 08:47:54','2019-05-17 08:47:54'),(5,'accelerometer','2019-05-17 08:48:20','2019-05-17 08:48:20');
/*!40000 ALTER TABLE `sensor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nickname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `badgeId` varchar(255) NOT NULL,
  `remember_token` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_badgeid_unique` (`badgeId`),
  UNIQUE KEY `users_email_unique` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'aauffr20','a.y.auffret@gmail.com','2019-05-13 08:46:30','$2y$10$rJKDvzn3ZCOB3mD8s..xHeYQXGvtQreLHywJAPoVkmR7/FacQXH/m','003173','lge7r7i2sxsbclhSvPXNMLclDiR1SdF0FzQIrcFcjKUEJG7Ke2gHar0SVVnl','2019-05-13 08:46:17','2019-05-13 08:46:30'),(2,'Virkin','virgile.prin@gmail.com','2019-05-13 12:58:40','$2y$10$g12eqDqTBrr125aDPEmwguV6DpFvIM3TnH6yWDtacoFmImbduwKWy','003188','mhqX6wOZNedlb0EvMnl4HAvTk0ygDHYVvnbMfiWiIlhTFdezJDmTz88IbLAV','2019-05-13 12:32:23','2019-05-13 12:58:40');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle`
--

DROP TABLE IF EXISTS `vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `brand` varchar(255) NOT NULL,
  `model` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `numberPlate` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vehicle_numberplate_unique` (`numberPlate`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle`
--

LOCK TABLES `vehicle` WRITE;
/*!40000 ALTER TABLE `vehicle` DISABLE KEYS */;
INSERT INTO `vehicle` VALUES (1,'pixel','cube','electric','BC-386-JQ','2019-05-13 08:33:12','2019-05-13 08:33:12');
/*!40000 ALTER TABLE `vehicle` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-05-21 16:20:29
