-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: new
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `assessment`
--

DROP TABLE IF EXISTS `assessment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assessment` (
  `user_id` int NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `assessment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `employee` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessment`
--

LOCK TABLES `assessment` WRITE;
/*!40000 ALTER TABLE `assessment` DISABLE KEYS */;
INSERT INTO `assessment` VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12),(13),(14),(15),(16),(17),(18),(20),(21),(22),(23),(24),(25),(26),(27),(28),(29),(30),(31),(32),(33),(34),(35),(36),(37),(38),(39),(40),(41),(42),(43),(44),(45),(46),(47),(48),(49),(50),(51),(52),(53),(55),(56),(57),(58),(59),(60),(61),(62),(63),(64),(65),(66),(67),(68),(69),(70),(71),(72),(73),(74),(75),(76),(77),(78),(79),(80),(81),(82),(83),(84),(85),(86),(87),(88),(89),(90),(91),(92),(93),(94),(95),(96),(97),(98),(99),(100),(101),(102),(103),(104),(105),(106),(107),(108),(109),(110),(111),(112),(113),(114),(116),(117),(118),(119),(120),(121),(122),(123),(124);
/*!40000 ALTER TABLE `assessment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assessment_marks`
--

DROP TABLE IF EXISTS `assessment_marks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assessment_marks` (
  `assessment_id` int NOT NULL AUTO_INCREMENT,
  `emp_id` int DEFAULT NULL,
  `course_name` varchar(255) NOT NULL,
  `marks_obtained` int DEFAULT NULL,
  `attempt_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`assessment_id`),
  KEY `emp_id_fk_marks_idx` (`emp_id`),
  CONSTRAINT `emp_id_fk_marks` FOREIGN KEY (`emp_id`) REFERENCES `employee` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessment_marks`
--

LOCK TABLES `assessment_marks` WRITE;
/*!40000 ALTER TABLE `assessment_marks` DISABLE KEYS */;
INSERT INTO `assessment_marks` VALUES (7,12,'Fundamentals of Javascript',8,'2025-08-09 13:23:40'),(9,12,'Introduction to testing',8,'2025-08-09 16:13:55');
/*!40000 ALTER TABLE `assessment_marks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `CourseID` int NOT NULL AUTO_INCREMENT,
  `CourseName` varchar(255) NOT NULL,
  `Domain` varchar(100) NOT NULL,
  `EstimatedTime` varchar(50) DEFAULT NULL,
  `CourseFile` varchar(255) NOT NULL,
  PRIMARY KEY (`CourseID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'Fundamentals of Javascript','Frontend Developer','2 Hours','js3.html'),(2,'Fundamentals of CSS','Frontend Developer','2 Hours','CSS.html'),(3,'Introduction to testing','Frontend Developer','1.5 Hours','testing.html'),(4,'Introduction to HTML Tags','Frontend Developer','1 Hour','HTMLTAGS.html'),(5,'Fundamentals of Java','Backend Developer','3 Hours','java.html'),(6,'Fundamentals of Python','Backend Developer','2.5 Hours','python.html'),(7,'Fundamentals of C','Backend Developer','3 Hours','c_course1.html'),(8,'Fundamentals of C++','Backend Developer','3.5 Hours','c++_course.html'),(9,'SQL Testing Course','Automation Tester','2 Hours','Sql_testing_course.html');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_assigned`
--

DROP TABLE IF EXISTS `course_assigned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_assigned` (
  `assignment_id` int NOT NULL AUTO_INCREMENT,
  `emp_id` int DEFAULT NULL,
  `course_name` varchar(255) NOT NULL,
  `status` varchar(45) NOT NULL DEFAULT 'Not Started',
  `progress` int NOT NULL DEFAULT '0',
  `assigned_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`assignment_id`),
  KEY `emp_id_fk_idx` (`emp_id`),
  CONSTRAINT `emp_id_fk` FOREIGN KEY (`emp_id`) REFERENCES `employee` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_assigned`
--

LOCK TABLES `course_assigned` WRITE;
/*!40000 ALTER TABLE `course_assigned` DISABLE KEYS */;
INSERT INTO `course_assigned` VALUES (1,12,'Fundamentals of Javascript','In Progress',10,'2025-08-09 14:10:46'),(2,12,'Introduction to testing','In Progress',10,'2025-08-09 14:57:24'),(3,1,'Fundamentals of Javascript','Not Started',0,'2025-08-09 15:55:58'),(4,12,'Fundamentals of CSS','In Progress',10,'2025-08-09 15:56:06'),(5,13,'Fundamentals of CSS','In Progress',10,'2025-08-10 06:30:15');
/*!40000 ALTER TABLE `course_assigned` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_completed`
--

DROP TABLE IF EXISTS `course_completed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_completed` (
  `completion_id` int NOT NULL AUTO_INCREMENT,
  `emp_id` int DEFAULT NULL,
  `course_name` varchar(255) NOT NULL,
  `completion_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`completion_id`),
  KEY `emp_id_completed_fk_idx` (`emp_id`),
  CONSTRAINT `emp_id_completed_fk` FOREIGN KEY (`emp_id`) REFERENCES `employee` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_completed`
--

LOCK TABLES `course_completed` WRITE;
/*!40000 ALTER TABLE `course_completed` DISABLE KEYS */;
INSERT INTO `course_completed` VALUES (3,12,'Fundamentals of Javascript','2025-08-09 13:19:29'),(5,12,'Introduction to testing','2025-08-09 16:13:55');
/*!40000 ALTER TABLE `course_completed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `credentials`
--

DROP TABLE IF EXISTS `credentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `credentials` (
  `cred_id` int NOT NULL AUTO_INCREMENT,
  `emp_id` int DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`cred_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `emp_id` (`emp_id`),
  CONSTRAINT `credentials_ibfk_1` FOREIGN KEY (`emp_id`) REFERENCES `employee` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=147 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credentials`
--

LOCK TABLES `credentials` WRITE;
/*!40000 ALTER TABLE `credentials` DISABLE KEYS */;
INSERT INTO `credentials` VALUES (1,1,'alice1','11','alice1@company.com',0),(2,2,'bob2','22','bob2@company.com',0),(3,3,'charlie3','33','charlie3@company.com',0),(4,4,'diana4','44','diana4@company.com',0),(5,5,'ethan5','55','ethan5@company.com',0),(6,6,'fiona6','66','fiona6@company.com',0),(7,7,'george7','77','george7@company.com',0),(8,8,'hannah8','88','hannah8@company.com',0),(9,9,'ivan9','99','ivan9@company.com',0),(10,10,'jaya10','1010','jaya10@company.com',0),(11,11,'admin11','1111','admin11@company.com',1),(12,12,'alice12','1212','alice12@company.com',0),(13,13,'bob13','1313','bob13@company.com',0),(14,14,'charlie14','1414','charlie14@company.com',0),(15,15,'vasanth15','1515','vasanth15@company.com',0),(16,16,'alice16','1616','alice16@company.com',0),(17,17,'bob17','1717','bob17@company.com',0),(18,18,'charlie18','1818','charlie18@company.com',0),(20,20,'ethan20','2020','ethan20@company.com',0),(21,21,'fiona21','2121','fiona21@company.com',0),(22,22,'george22','2222','george22@company.com',0),(23,23,'hannah23','2323','hannah23@company.com',0),(24,24,'ivan24','2424','ivan24@company.com',0),(25,25,'jaya25','2525','jaya25@company.com',0),(26,26,'alice26','2626','alice26@company.com',0),(27,27,'bob27','2727','bob27@company.com',0),(28,28,'charlie28','2828','charlie28@company.com',0),(29,29,'diana29','2929','diana29@company.com',0),(30,30,'ethan30','3030','ethan30@company.com',0),(31,31,'fiona31','3131','fiona31@company.com',0),(32,32,'george32','3232','george32@company.com',0),(33,33,'hannah33','3333','hannah33@company.com',0),(34,34,'ivan34','3434','ivan34@company.com',0),(35,35,'jaya35','3535','jaya35@company.com',0),(36,36,'admin36','3636','admin36@company.com',1),(37,37,'alice37','3737','alice37@company.com',0),(38,38,'bob38','3838','bob38@company.com',0),(39,39,'charlie39','3939','charlie39@company.com',0),(40,40,'vasanth40','4040','vasanth40@company.com',0),(41,41,'admin41','4141','admin41@company.com',1),(42,42,'alice42','4242','alice42@company.com',0),(43,43,'bob43','4343','bob43@company.com',0),(44,44,'charlie44','4444','charlie44@company.com',0),(45,45,'alice45','4545','alice45@company.com',0),(46,46,'bob46','4646','bob46@company.com',0),(47,47,'charlie47','4747','charlie47@company.com',0),(48,48,'diana48','4848','diana48@company.com',0),(49,49,'ethan49','4949','ethan49@company.com',0),(50,50,'fiona50','5050','fiona50@company.com',0),(51,51,'george51','5151','george51@company.com',0),(52,52,'hannah52','5252','hannah52@company.com',0),(53,53,'ivan53','5353','ivan53@company.com',0),(55,55,'alice55','5555','alice55@company.com',0),(56,56,'bob56','5656','bob56@company.com',0),(57,57,'charlie57','5757','charlie57@company.com',0),(58,58,'diana58','5858','diana58@company.com',0),(59,59,'ethan59','5959','ethan59@company.com',0),(60,60,'fiona60','6060','fiona60@company.com',0),(61,61,'george61','6161','george61@company.com',0),(62,62,'hannah62','6262','hannah62@company.com',0),(63,63,'ivan63','6363','ivan63@company.com',0),(64,64,'jaya64','6464','jaya64@company.com',0),(65,65,'alice65','6565','alice65@company.com',0),(66,66,'bob66','6666','bob66@company.com',0),(67,67,'charlie67','6767','charlie67@company.com',0),(68,68,'diana68','6868','diana68@company.com',0),(69,69,'ethan69','6969','ethan69@company.com',0),(70,70,'fiona70','7070','fiona70@company.com',0),(71,71,'george71','7171','george71@company.com',0),(72,72,'hannah72','7272','hannah72@company.com',0),(73,73,'ivan73','7373','ivan73@company.com',0),(74,74,'jaya74','7474','jaya74@company.com',0),(75,75,'admin75','7575','admin75@company.com',1),(76,76,'alice76','7676','alice76@company.com',0),(77,77,'bob77','7777','bob77@company.com',0),(78,78,'charlie78','7878','charlie78@company.com',0),(79,79,'alice79','7979','alice79@company.com',0),(80,80,'bob80','8080','bob80@company.com',0),(81,81,'charlie81','8181','charlie81@company.com',0),(82,82,'diana82','8282','diana82@company.com',0),(83,83,'ethan83','8383','ethan83@company.com',0),(84,84,'fiona84','8484','fiona84@company.com',0),(85,85,'george85','8585','george85@company.com',0),(86,86,'hannah86','8686','hannah86@company.com',0),(87,87,'ivan87','8787','ivan87@company.com',0),(88,88,'jaya88','8888','jaya88@company.com',0),(89,89,'admin89','8989','admin89@company.com',1),(90,90,'alice90','9090','alice90@company.com',0),(91,91,'bob91','9191','bob91@company.com',0),(92,92,'charlie92','9292','charlie92@company.com',0),(93,93,'alice93','9393','alice93@company.com',0),(94,94,'bob94','9494','bob94@company.com',0),(95,95,'charlie95','9595','charlie95@company.com',0),(96,96,'diana96','9696','diana96@company.com',0),(97,97,'ethan97','9797','ethan97@company.com',0),(98,98,'fiona98','9898','fiona98@company.com',0),(99,99,'george99','9999','george99@company.com',0),(100,100,'hannah100','100100','hannah100@company.com',0),(101,101,'ivan101','101101','ivan101@company.com',0),(102,102,'jaya102','102102','jaya102@company.com',0),(103,103,'alice103','103103','alice103@company.com',0),(104,104,'bob104','104104','bob104@company.com',0),(105,105,'charlie105','105105','charlie105@company.com',0),(106,106,'diana106','106106','diana106@company.com',0),(107,107,'ethan107','107107','ethan107@company.com',0),(108,108,'fiona108','108108','fiona108@company.com',0),(109,109,'george109','109109','george109@company.com',0),(110,110,'hannah110','110110','hannah110@company.com',0),(111,111,'ivan111','111111','ivan111@company.com',0),(112,112,'jaya112','112112','jaya112@company.com',0),(113,113,'admin113','113113','admin113@company.com',1),(114,114,'alice114','114114','alice114@company.com',0),(116,116,'charlie116','116116','charlie116@company.com',0),(117,117,'alice117','117117','alice117@company.com',0),(118,118,'bob118','118118','bob118@company.com',0),(119,119,'charlie119','119119','charlie119@company.com',0),(120,120,'diana120','120120','diana120@company.com',0),(121,121,'ethan121','121121','ethan121@company.com',0),(122,122,'fiona122','122122','fiona122@company.com',0),(123,123,'george123','123123','george123@company.com',0),(124,124,'hannah124','124124','hannah124@company.com',0),(131,131,'testuser','password123','test@example.com',0),(132,132,'mydeen132','pass132','mydeen132@company.com',0),(133,133,'kushal133','pass133','kushal133@company.com',0),(134,134,'loganathan134','pass134','loganathan134@company.com',0),(135,135,'marimuthu135','pass135','marimuthu135@company.com',0),(136,136,'lokesh136','pass136','lokesh136@company.com',0),(137,137,'logeshwaran137','pass137','logeshwaran137@company.com',0),(138,138,'manoj138','pass138','manoj138@company.com',0),(139,139,'mydeen139','pass139','mydeen139@company.com',0),(140,140,'kushal140','pass140','kushal140@company.com',0),(141,141,'loganathan141','pass141','loganathan141@company.com',0),(142,142,'marimuthu142','pass142','marimuthu142@company.com',0),(143,143,'lokesh143','pass143','lokesh143@company.com',0),(144,144,'logeshwaran144','pass144','logeshwaran144@company.com',0),(145,145,'manoj145','pass145','manoj145@company.com',0);
/*!40000 ALTER TABLE `credentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `NAME` varchar(50) DEFAULT NULL,
  `HTML` int DEFAULT NULL,
  `CSS` int DEFAULT NULL,
  `JAVASCRIPT` int DEFAULT NULL,
  `PYTHON` int DEFAULT NULL,
  `C` int DEFAULT NULL,
  `CPP` int DEFAULT NULL,
  `JAVA` int DEFAULT NULL,
  `SQL_TESTING` int DEFAULT NULL,
  `TOOLS_COURSE` int DEFAULT NULL,
  `domain` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=147 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'Alice',80,85,78,60,70,65,75,50,40,'Frontend Developer'),(2,'Bob',60,55,58,70,60,55,65,45,50,'Backend Developer'),(3,'Charlie',90,95,92,20,10,10,15,30,35,'Frontend Developer'),(4,'Diana',40,35,30,80,85,75,70,60,65,'Backend Developer'),(5,'Ethan',50,45,55,50,40,30,25,20,30,NULL),(6,'Fiona',10,15,20,90,95,85,80,70,75,NULL),(7,'George',85,88,90,25,20,15,10,5,10,NULL),(8,'Hannah',88,85,87,65,60,70,75,55,50,NULL),(9,'Ivan',25,30,35,45,50,55,60,65,70,NULL),(10,'Jaya',78,82,80,55,58,60,62,64,66,NULL),(11,'ADMIN',90,85,88,92,80,75,85,78,70,NULL),(12,'Alice',80,70,60,50,40,60,45,85,60,'Database Engineer'),(13,'Bob',60,65,70,55,50,40,50,90,50,'Database Engineer'),(14,'Charlie',85,88,82,75,65,70,80,88,75,NULL),(15,'vasanth',100,100,100,100,100,100,100,0,0,NULL),(16,'Alice',80,85,78,60,70,65,75,50,40,NULL),(17,'Bob',60,55,58,70,60,55,65,45,50,NULL),(18,'Charlie',90,95,92,20,10,10,15,30,35,NULL),(20,'Ethan',50,45,55,50,40,30,25,20,30,NULL),(21,'Fiona',10,15,20,90,95,85,80,70,75,NULL),(22,'George',85,88,90,25,20,15,10,5,10,NULL),(23,'Hannah',88,85,87,65,60,70,75,55,50,NULL),(24,'Ivan',25,30,35,45,50,55,60,65,70,NULL),(25,'Jaya',78,82,80,55,58,60,62,64,66,NULL),(26,'Alice',80,85,78,60,70,65,75,50,40,NULL),(27,'Bob',60,55,58,70,60,55,65,45,50,NULL),(28,'Charlie',90,95,92,20,10,10,15,30,35,NULL),(29,'Diana',40,35,30,80,85,75,70,60,65,NULL),(30,'Ethan',50,45,55,50,40,30,25,20,30,'Frontend Developer'),(31,'Fiona',10,15,20,90,95,85,80,70,75,NULL),(32,'George',85,88,90,25,20,15,10,5,10,NULL),(33,'Hannah',88,85,87,65,60,70,75,55,50,NULL),(34,'Ivan',25,30,35,45,50,55,60,65,70,NULL),(35,'Jaya',78,82,80,55,58,60,62,64,66,NULL),(36,'ADMIN',90,85,88,92,80,75,85,78,70,NULL),(37,'Alice',80,70,60,50,40,60,45,85,60,NULL),(38,'Bob',60,65,70,55,50,40,50,90,50,NULL),(39,'Charlie',85,88,82,75,65,70,80,88,75,NULL),(40,'vasanth',100,100,100,100,100,100,100,100,100,NULL),(41,'ADMIN',90,85,88,92,80,75,85,78,70,NULL),(42,'Alice',80,70,60,50,40,60,45,85,60,NULL),(43,'Bob',60,65,70,55,50,40,50,90,50,NULL),(44,'Charlie',85,88,82,75,65,70,80,88,75,NULL),(45,'Alice',80,85,78,60,70,65,75,50,40,NULL),(46,'Bob',60,55,58,70,60,55,65,45,50,NULL),(47,'Charlie',90,95,92,20,10,10,15,30,35,NULL),(48,'Diana',40,35,30,80,85,75,70,60,65,NULL),(49,'Ethan',50,45,55,50,40,30,25,20,30,NULL),(50,'Fiona',10,15,20,90,95,85,80,70,75,NULL),(51,'George',85,88,90,25,20,15,10,5,10,NULL),(52,'Hannah',88,85,87,65,60,70,75,55,50,NULL),(53,'Ivan',25,30,35,45,50,55,60,65,70,NULL),(55,'Alice',80,85,78,60,70,65,75,50,40,NULL),(56,'Bob',60,55,58,70,60,55,65,45,50,NULL),(57,'Charlie',90,95,92,20,10,10,15,30,35,NULL),(58,'Diana',40,35,30,80,85,75,70,60,65,NULL),(59,'Ethan',50,45,55,50,40,30,25,20,30,NULL),(60,'Fiona',10,15,20,90,95,85,80,70,75,NULL),(61,'George',85,88,90,25,20,15,10,5,10,NULL),(62,'Hannah',88,85,87,65,60,70,75,55,50,NULL),(63,'Ivan',25,30,35,45,50,55,60,65,70,NULL),(64,'Jaya',78,82,80,55,58,60,62,64,66,NULL),(65,'Alice',80,85,78,60,70,65,75,50,40,NULL),(66,'Bob',60,55,58,70,60,55,65,45,50,NULL),(67,'Charlie',90,95,92,20,10,10,15,30,35,NULL),(68,'Diana',40,35,30,80,85,75,70,60,65,NULL),(69,'Ethan',50,45,55,50,40,30,25,20,30,NULL),(70,'Fiona',10,15,20,90,95,85,80,70,75,NULL),(71,'George',85,88,90,25,20,15,10,5,10,NULL),(72,'Hannah',88,85,87,65,60,70,75,55,50,NULL),(73,'Ivan',25,30,35,45,50,55,60,65,70,NULL),(74,'Jaya',78,82,80,55,58,60,62,64,66,NULL),(75,'ADMIN',90,85,88,92,80,75,85,78,70,NULL),(76,'Alice',80,70,60,50,40,60,45,85,60,NULL),(77,'Bob',60,65,70,55,50,40,50,90,50,NULL),(78,'Charlie',85,88,82,75,65,70,80,88,75,NULL),(79,'Alice',80,85,78,60,70,65,75,50,40,NULL),(80,'Bob',60,55,58,70,60,55,65,45,50,NULL),(81,'Charlie',90,95,92,20,10,10,15,30,35,NULL),(82,'Diana',40,35,30,80,85,75,70,60,65,NULL),(83,'Ethan',50,45,55,50,40,30,25,20,30,NULL),(84,'Fiona',10,15,20,90,95,85,80,70,75,NULL),(85,'George',85,88,90,25,20,15,10,5,10,NULL),(86,'Hannah',88,85,87,65,60,70,75,55,50,NULL),(87,'Ivan',25,30,35,45,50,55,60,65,70,NULL),(88,'Jaya',78,82,80,55,58,60,62,64,66,NULL),(89,'ADMIN',90,85,88,92,80,75,85,78,70,NULL),(90,'Alice',80,70,60,50,40,60,45,85,60,NULL),(91,'Bob',60,65,70,55,50,40,50,90,50,NULL),(92,'Charlie',85,88,82,75,65,70,80,88,75,NULL),(93,'Alice',80,85,78,60,70,65,75,50,40,NULL),(94,'Bob',60,55,58,70,60,55,65,45,50,NULL),(95,'Charlie',90,95,92,20,10,10,15,30,35,NULL),(96,'Diana',40,35,30,80,85,75,70,60,65,NULL),(97,'Ethan',50,45,55,50,40,30,25,20,30,NULL),(98,'Fiona',10,15,20,90,95,85,80,70,75,NULL),(99,'George',85,88,90,25,20,15,10,5,10,NULL),(100,'Hannah',88,85,87,65,60,70,75,0,50,NULL),(101,'Ivan',25,30,35,45,50,55,60,65,70,NULL),(102,'Jaya',78,82,80,55,58,60,62,64,66,NULL),(103,'Alice',80,85,78,60,70,65,75,50,40,NULL),(104,'Bob',60,55,58,70,60,55,65,45,50,NULL),(105,'Charlie',90,95,92,20,10,10,15,30,35,NULL),(106,'Diana',40,35,30,80,85,75,70,60,65,NULL),(107,'Ethan',50,45,55,50,40,30,25,20,30,NULL),(108,'Fiona',10,15,20,90,95,85,80,70,75,NULL),(109,'George',85,88,90,25,20,15,10,5,10,NULL),(110,'Hannah',88,85,87,65,60,70,75,55,50,NULL),(111,'Ivan',25,30,35,45,50,55,60,65,70,NULL),(112,'Jaya',78,82,80,55,58,60,62,64,66,NULL),(113,'ADMIN',90,85,88,92,80,75,85,78,70,NULL),(114,'Alice',80,70,60,50,40,60,45,85,60,NULL),(116,'Charlie',85,88,82,75,65,70,80,88,75,NULL),(117,'Alice',80,85,78,60,70,65,75,50,40,NULL),(118,'Bob',60,55,58,70,60,55,65,45,50,NULL),(119,'Charlie',90,95,92,20,10,10,15,30,35,NULL),(120,'Diana',40,35,30,80,85,75,70,60,65,NULL),(121,'Ethan',50,45,55,50,40,30,25,20,30,NULL),(122,'Fiona',10,15,20,90,95,85,80,70,75,NULL),(123,'George',85,88,90,25,20,15,10,5,10,NULL),(124,'Hannah',88,85,87,65,60,70,75,55,50,NULL),(131,'TestUser',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Development'),(132,'mydeen',80,85,90,75,65,0,60,40,50,NULL),(133,'kushal',70,75,80,55,60,0,58,65,45,NULL),(134,'loganathan',60,55,50,40,45,0,52,70,30,NULL),(135,'marimuthu',10,20,15,55,60,0,70,85,90,NULL),(136,'lokesh',85,90,88,95,70,0,60,50,30,NULL),(137,'logeshwaran',20,25,30,35,40,0,60,90,80,NULL),(138,'manoj',75,78,80,85,88,0,90,60,40,NULL),(139,'mydeen',80,85,90,75,65,0,60,40,50,NULL),(140,'kushal',70,75,80,55,60,0,58,65,45,NULL),(141,'loganathan',60,55,50,40,45,0,52,70,30,NULL),(142,'marimuthu',10,20,15,55,60,0,70,85,90,NULL),(143,'lokesh',85,90,88,95,70,0,60,50,30,NULL),(144,'logeshwaran',20,25,30,35,40,0,60,90,80,NULL),(145,'manoj',75,78,80,85,88,0,90,60,40,NULL);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status` (
  `user_id` int NOT NULL,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `status_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `employee` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
INSERT INTO `status` VALUES (1,'Pending'),(2,'Pending'),(3,'Pending'),(4,'Pending'),(5,'Pending'),(6,'Pending'),(7,'Pending'),(8,'Pending'),(9,'Pending'),(10,'Pending'),(11,'Pending'),(12,'Pending'),(13,'Pending'),(14,'Pending'),(15,'Pending'),(16,'Pending'),(17,'Pending'),(18,'Pending'),(20,'Pending'),(21,'Pending'),(22,'Pending'),(23,'Pending'),(24,'Pending'),(25,'Pending'),(26,'Pending'),(27,'Pending'),(28,'Pending'),(29,'Pending'),(30,'Pending'),(31,'Pending'),(32,'Pending'),(33,'Pending'),(34,'Pending'),(35,'Pending'),(36,'Pending'),(37,'Pending'),(38,'Pending'),(39,'Pending'),(40,'Pending'),(41,'Pending'),(42,'Pending'),(43,'Pending'),(44,'Pending'),(45,'Pending'),(46,'Pending'),(47,'Pending'),(48,'Pending'),(49,'Pending'),(50,'Pending'),(51,'Pending'),(52,'Pending'),(53,'Pending'),(55,'Pending'),(56,'Pending'),(57,'Pending'),(58,'Pending'),(59,'Pending'),(60,'Pending'),(61,'Pending'),(62,'Pending'),(63,'Pending'),(64,'Pending'),(65,'Pending'),(66,'Pending'),(67,'Pending'),(68,'Pending'),(69,'Pending'),(70,'Pending'),(71,'Pending'),(72,'Pending'),(73,'Pending'),(74,'Pending'),(75,'Pending'),(76,'Pending'),(77,'Pending'),(78,'Pending'),(79,'Pending'),(80,'Pending'),(81,'Pending'),(82,'Pending'),(83,'Pending'),(84,'Pending'),(85,'Pending'),(86,'Pending'),(87,'Pending'),(88,'Pending'),(89,'Pending'),(90,'Pending'),(91,'Pending'),(92,'Pending'),(93,'Pending'),(94,'Pending'),(95,'Pending'),(96,'Pending'),(97,'Pending'),(98,'Pending'),(99,'Pending'),(100,'Pending'),(101,'Pending'),(102,'Pending'),(103,'Pending'),(104,'Pending'),(105,'Pending'),(106,'Pending'),(107,'Pending'),(108,'Pending'),(109,'Pending'),(110,'Pending'),(111,'Pending'),(112,'Pending'),(113,'Pending'),(114,'Pending'),(116,'Pending'),(117,'Pending'),(118,'Pending'),(119,'Pending'),(120,'Pending'),(121,'Pending'),(122,'Pending'),(123,'Pending'),(124,'Pending');
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-10 12:13:43
