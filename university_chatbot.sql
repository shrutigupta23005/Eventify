-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: university_chatbot
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `admin_id` int NOT NULL,
  `admin_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'Juhi','juhipanda902@gmail.com','200507Jj#'),(2,'Sanvi','sanvijain1703@gmail.com','1703Ss#'),(3,'Divyanjali','divyanjalinegii@gmail.com','3Dd#'),(4,'Riya','reyapandey42@gmail.com','42Rr#'),(5,'Muskan','muskaangupta23005@gmail.com','23005Mm#');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certificates`
--

DROP TABLE IF EXISTS `certificates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificates` (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(150) NOT NULL,
  `course_type` varchar(50) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `exam_fees` decimal(10,2) DEFAULT NULL,
  `form_location` varchar(255) DEFAULT NULL,
  `admin_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`course_id`),
  KEY `admin_id` (`admin_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `certificates_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`),
  CONSTRAINT `certificates_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=188 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificates`
--

LOCK TABLES `certificates` WRITE;
/*!40000 ALTER TABLE `certificates` DISABLE KEYS */;
INSERT INTO `certificates` VALUES (100,'Certificate in Dancing (Kathak Pratham)','Certificate','Dance - Kathak',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(101,'Certificate in Dancing (Kathak Madhyama)','Certificate','Dance - Kathak',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(102,'Diploma in Dance (Kathak Uttama-I)','Diploma','Dance - Kathak',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(103,'Diploma in Dance (Kathak Uttama-II)','Diploma','Dance - Kathak',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(104,'Diploma in Dance (Kathak Uttama-III)','Diploma','Dance - Kathak',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(105,'Diploma in Dance (Kathak Nishanat-I)','Diploma','Dance - Kathak',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(106,'Diploma in Dance (Kathak Nishanat-II)','Diploma','Dance - Kathak',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(107,'Diploma in Dance (Kathak Nishanat-III)','Diploma','Dance - Kathak',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(108,'Certificate in Dance (Manipuri Pratham)','Certificate','Dance - Manipuri',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(109,'Certificate in Dance (Manipuri Madhyama)','Certificate','Dance - Manipuri',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(110,'Diploma in Dance (Manipuri Uttama-I)','Diploma','Dance - Manipuri',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(111,'Diploma in Dance (Manipuri Uttama-II)','Diploma','Dance - Manipuri',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(112,'Diploma in Dance (Manipuri Uttama-III)','Diploma','Dance - Manipuri',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(113,'Diploma in Dance (Manipuri Nishanat-I)','Diploma','Dance - Manipuri',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(114,'Diploma in Dance (Manipuri Nishanat-II)','Diploma','Dance - Manipuri',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(115,'Certificate in Dancing (Bharatnatyam Pratham)','Certificate','Dance - Bharatnatyam',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(116,'Certificate in Dancing (Bharatnatyam Madhyama)','Certificate','Dance - Bharatnatyam',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(117,'Diploma in Dance (Bharatnatyam Uttama-I)','Diploma','Dance - Bharatnatyam',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(118,'Diploma in Dance (Bharatnatyam Uttama-II)','Diploma','Dance - Bharatnatyam',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(119,'Diploma in Dance (Bharatnatyam Uttama-III)','Diploma','Dance - Bharatnatyam',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(120,'Diploma in Dance (Bharatnatyam Nishanat-I)','Diploma','Dance - Bharatnatyam',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(121,'Diploma in Dance (Bharatnatyam Nishanat-II)','Diploma','Dance - Bharatnatyam',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(122,'Diploma in Dance (Bharatnatyam Nishanat-III)','Diploma','Dance - Bharatnatyam',1500.00,'Nupur Mandir / Kala Mandir',1,NULL),(123,'Certificate in Music (Inst.) SAROD (Pratham)','Certificate','Music - Sarod',1500.00,'Sur Mandir',1,NULL),(124,'Certificate in Music (Inst.) SAROD (Madhyama)','Certificate','Music - Sarod',1500.00,'Sur Mandir',1,NULL),(125,'Diploma in Music (Inst.) SAROD (Visharad Part-I)','Diploma','Music - Sarod',1500.00,'Sur Mandir',1,NULL),(126,'Diploma in Music (Inst.) SAROD (Visharad Part-II)','Diploma','Music - Sarod',1500.00,'Sur Mandir',1,NULL),(127,'Diploma in Music (Inst.) SAROD (Visharad Part-III)','Diploma','Music - Sarod',1500.00,'Sur Mandir',1,NULL),(128,'Certificate in Music (Inst.) SITAR (Pratham)','Certificate','Music - Sitar',1500.00,'Sur Mandir',1,NULL),(129,'Certificate in Music (Inst.) SITAR (Madhyama)','Certificate','Music - Sitar',1500.00,'Sur Mandir',1,NULL),(130,'Diploma in Music (Inst.) SITAR (Visharad Part-I)','Diploma','Music - Sitar',1500.00,'Sur Mandir',1,NULL),(131,'Diploma in Music (Inst.) SITAR (Visharad Part-II)','Diploma','Music - Sitar',1500.00,'Sur Mandir',1,NULL),(132,'Diploma in Music (Inst.) SITAR (Visharad Part-III)','Diploma','Music - Sitar',1500.00,'Sur Mandir',1,NULL),(133,'Certificate in Music (Inst.) TABLA (Pratham)','Certificate','Music - Tabla',1500.00,'Sur Mandir',1,NULL),(134,'Certificate in Music (Inst.) TABLA (Madhyama)','Certificate','Music - Tabla',1500.00,'Sur Mandir',1,NULL),(135,'Diploma in Music (Inst.) TABLA (Visharad Part-I)','Diploma','Music - Tabla',1500.00,'Sur Mandir',1,NULL),(136,'Diploma in Music (Inst.) TABLA (Visharad Part-II)','Diploma','Music - Tabla',1500.00,'Sur Mandir',1,NULL),(137,'Diploma in Music (Inst.) TABLA (Visharad Part-III)','Diploma','Music - Tabla',1500.00,'Sur Mandir',1,NULL),(138,'Certificate in Music (Inst.) VIOLIN (Pratham)','Certificate','Music - Violin',1500.00,'Sur Mandir',1,NULL),(139,'Certificate in Music (Inst.) VIOLIN (Madhyama)','Certificate','Music - Violin',1500.00,'Sur Mandir',1,NULL),(140,'Diploma in Music (Inst.) VIOLIN (Visharad Part-I)','Diploma','Music - Violin',1500.00,'Sur Mandir',1,NULL),(141,'Diploma in Music (Inst.) VIOLIN (Visharad Part-II)','Diploma','Music - Violin',1500.00,'Sur Mandir',1,NULL),(142,'Diploma in Music (Inst.) VIOLIN (Visharad Part-III)','Diploma','Music - Violin',1500.00,'Sur Mandir',1,NULL),(143,'Certificate in Music (Vocal) Pratham','Certificate','Music - Vocal',1500.00,'Sur Mandir',1,NULL),(144,'Certificate in Music (Vocal) Madhyama','Certificate','Music - Vocal',1500.00,'Sur Mandir',1,NULL),(145,'Diploma in Music (Vocal) Visharad Part-I','Diploma','Music - Vocal',1500.00,'Sur Mandir',1,NULL),(146,'Diploma in Music (Vocal) Visharad Part-II','Diploma','Music - Vocal',1500.00,'Sur Mandir',1,NULL),(147,'Diploma in Music (Vocal) Visharad Part-III','Diploma','Music - Vocal',1500.00,'Sur Mandir',1,NULL),(148,'Certificate in Music (Inst.) GUITAR (Pratham)','Certificate','Music - Guitar',1500.00,'Sur Mandir',1,NULL),(149,'Certificate in Music (Inst.) GUITAR (Madhyama)','Certificate','Music - Guitar',1500.00,'Sur Mandir',1,NULL),(150,'Diploma in Music (GUITAR) Visharad Part-I','Diploma','Music - Guitar',1500.00,'Sur Mandir',1,NULL),(151,'Diploma in Music (GUITAR) Visharad Part-II','Diploma','Music - Guitar',1500.00,'Sur Mandir',1,NULL),(152,'Diploma in Music (GUITAR) Visharad Part-III','Diploma','Music - Guitar',1500.00,'Sur Mandir',1,NULL),(153,'Craft Certificate in Shibori (Tie & Dye)','Certificate','Craft - Textile',1500.00,'Shilp Mandir, Room No. 108',1,NULL),(154,'Craft Certificate in Batik (Dyeing & Painting)','Certificate','Craft - Textile',1500.00,'Shilp Mandir, Room No. 108',1,NULL),(155,'Craft Certificate in Surface Ornamentations','Certificate','Craft - Textile',1500.00,'Shilp Mandir, Room No. 108',1,NULL),(156,'Craft Certificate in Block Printing','Certificate','Craft - Textile',1500.00,'Shilp Mandir, Room No. 108',1,NULL),(157,'Craft Certificate in Macrame & Knotting','Certificate','Craft - Textile',1500.00,'Shilp Mandir, Room No. 108',1,NULL),(158,'Certificate in FRENCH','Certificate','French',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(159,'Diploma in FRENCH','Diploma','French',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(160,'Advance Diploma in FRENCH','Advanced Diploma','French',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(161,'Certificate in GERMAN','Certificate','German',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(162,'Diploma in GERMAN','Diploma','German',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(163,'Advance Diploma in GERMAN','Advanced Diploma','German',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(164,'Certificate in GERMAN FOR CONVERSATION (Elementary)','Certificate','German',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(165,'Certificate in GERMAN FOR CONVERSATION (Advanced)','Certificate','German',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(166,'Certificate in SANSKRIT','Certificate','Sanskrit',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(167,'Degree in SANSKRIT','Degree','Sanskrit',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(168,'Advance Diploma in SANSKRIT','Advanced Diploma','Sanskrit',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(169,'Shastri I Year','Degree','Sanskrit',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(170,'Shastri II Year','Degree','Sanskrit',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(171,'Shastri III Year','Degree','Sanskrit',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(172,'Certificate in ENGLISH FOR CONVERSATION (Elementary) (July to Dec.)','Certificate','English',1500.00,'Admin Office (Vani Mandir) / Online Form',1,NULL),(173,'Certificate in Computer Programming and Application','Certificate','Computer Science',7000.00,'AAPJI Institute Office',1,NULL),(174,'Diploma in Internet and Web Application','Diploma','Computer Science',7000.00,'AAPJI Institute Office',1,NULL),(175,'Diploma in .NET (ASP, C#, AJAX)','Diploma','Computer Science',7000.00,'AAPJI Institute Office',1,NULL),(176,'Diploma in Computer Hardware & Maintenance','Diploma','Computer Science',7000.00,'AAPJI Institute Office',1,NULL),(177,'Advance Diploma in Computer Networking (CCNA, CISCO)','Advanced Diploma','Networking',7000.00,'AAPJI Institute Office',1,NULL),(178,'Certificate in Statistical Techniques and Application','Certificate','Statistics',7000.00,'AAPJI Institute Office',1,NULL),(179,'Certificate in Actuarial Science','Certificate','Actuarial Science',7000.00,'AAPJI Institute Office',1,NULL),(180,'Diploma in Medical Image Processing','Diploma','Medical Imaging',7000.00,'AAPJI Institute Office',1,NULL),(181,'Advance Diploma in Medical Image Processing','Advanced Diploma','Medical Imaging',7000.00,'AAPJI Institute Office',1,NULL),(182,'Application Development with Android','Certificate','Mobile Development',3500.00,'AAPJI Institute Office',1,NULL),(183,'Certificate Course in Python Programming','Certificate','Programming',3500.00,'AAPJI Institute Office',1,NULL),(184,'Certificate in Radio Production - RJing & Anchoring','Certificate','Media & Communication',7000.00,'Vigyan Mandir FM Radio Office',1,NULL),(185,'Diploma in Audio Engineering','Diploma','Media & Communication',7000.00,'Vigyan Mandir FM Radio Office',1,NULL),(186,'Diploma in Broadcast Journalism (Radio)','Diploma','Media & Communication',7000.00,'Vigyan Mandir FM Radio Office',1,NULL),(187,'Diploma in Advertising and Public Relations','Diploma','Media & Communication',7000.00,'Vigyan Mandir FM Radio Office',1,NULL);
/*!40000 ALTER TABLE `certificates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clubs`
--

DROP TABLE IF EXISTS `clubs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clubs` (
  `club_id` int NOT NULL AUTO_INCREMENT,
  `club_name` varchar(100) NOT NULL,
  `club_type` varchar(50) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `contact_person` varchar(100) DEFAULT NULL,
  `contact_number` varchar(50) DEFAULT NULL,
  `social_link` varchar(255) DEFAULT NULL,
  `venue` varchar(100) DEFAULT NULL,
  `admin_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`club_id`),
  KEY `admin_id` (`admin_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `clubs_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`),
  CONSTRAINT `clubs_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=509 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clubs`
--

LOCK TABLES `clubs` WRITE;
/*!40000 ALTER TABLE `clubs` DISABLE KEYS */;
INSERT INTO `clubs` VALUES (500,'Freezy Freaks','Non-Official','Dance','Kanika','6350459117','https://www.instagram.com/freezyfreaks?igsh=MWhsMHc5b2Q4Ymw4aQ==','Shri Shanta Neri',5,NULL),(501,'Black Illuminators','Non-Official','Dance','Shreyanshi','9569890529','https://www.instagram.com/black_illiuminators_?igsh=d1JpbWt6MWNwaGJi','Shri Shanta Uthjam',5,NULL),(502,'ACM Chapter','Unofficial','Coding','Neelam Sharma Madam','acmchapter@banasthali.in','https://www.instagram.com/acmchapter_bv?igsh=MTltYmgzYm91MGlseA==','Aapaji Institute',5,NULL),(503,'MSC-BV','Official','Microsoft','Anushka','9149128554','https://www.instagram.com/msc_bv?igsh=MWpvMTlhejh1YTRzcA==','Nav Mandir',5,NULL),(504,'E-Cell','Official','Entrepreneurship','Sanskriti Sharma Madam','sanskritisharma@banasthali.in','https://www.instagram.com/ecell_banasthali?igsh=MWhxYmU5cHRpMWR2Yg==','Nav Mandir',5,NULL),(505,'IEEE','Non-Official','Electrical, Electronics, Computer Science, IT, Robotics, Aerospace, Biomedical, AI','Adwika Singh','6264823812','https://www.instagram.com/ieee_banasthali?igsh=cGE1d2JraHdxOW56','Automation',5,NULL),(506,'Street Dancers','Non-Official','Dance','Yashvi','+919426189809','https://www.instagram.com/streetdancersbv?igsh=bHNsZGppMXU4bGZi','Shri Shanta Saudh',5,NULL),(507,'Therav','Official','Poetry','Muskaan Vaswani','8058681767','https://www.instagram.com/thehravshabdonka/','Ratan Mandir',5,NULL),(508,'Expressio','Official','Public Speaking','Alankritaa Saxena','8103603589','https://www.instagram.com/expressio_banasthali_?igsh=MXNtbmRpZmo4amp0bw==','Nav Mandir Audi 1 and Prabha Mandir Audi 1',5,NULL);
/*!40000 ALTER TABLE `clubs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fests`
--

DROP TABLE IF EXISTS `fests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fests` (
  `fest_id` int NOT NULL AUTO_INCREMENT,
  `fest_name` varchar(100) NOT NULL,
  `category` varchar(500) DEFAULT NULL,
  `venue` varchar(100) DEFAULT NULL,
  `admin_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`fest_id`),
  KEY `admin_id` (`admin_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `fests_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`),
  CONSTRAINT `fests_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=508 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fests`
--

LOCK TABLES `fests` WRITE;
/*!40000 ALTER TABLE `fests` DISABLE KEYS */;
INSERT INTO `fests` VALUES (300,'Adhyaay','education, economics, journalism and mass communication, english and modern european languages, hindi and modern indian languages, earth sciences, history and indian culture, performing arts, political sciences, political science and public administration, psychology, sanskrit philosophy and vedic studies, sociology, design, visual arts, architecture and planning','Wisdom pandal',3,NULL),(301,'Mayukh','computer science, automation, mathematics and statistics, physical sciences','Surya mandir',3,NULL),(302,'Xeron','Chemical engineering and Chemistry','Gyan mandir',3,NULL),(303,'Navortkash 2n0','legal studies, commerce and management','Wisdom pandal',3,NULL),(304,'Cosmos','earth science','Wisdom Pandal',3,NULL),(305,'Janus','bioscience and biotechnology','Wisdom pandal',3,NULL),(306,'HUE','Home science','Gyan Mandir',3,NULL),(500,'Xeron','Chemical Engineering, Chemistry',NULL,5,NULL),(501,'Mayukh','Computer Science, Automation, Mathematics and Statistics, Physical Sciences',NULL,5,NULL),(502,'Adhyay','Education, Economics, Journalism and Mass Communication, English and Modern European Languages, Hindi and Modern Indian Languages, History and Indian Culture, Performing Arts, Political Science and Public Administration, Psychology, Sanskrit Philosophy and Vedic Studies, Sociology, Design, Visual Arts, Architecture and Planning',NULL,5,NULL),(503,'Navotkash 2n0','Legal Studies, Commerce and Management',NULL,5,NULL),(504,'Karvaan','Journalism and Mass Communication',NULL,5,NULL),(505,'Cosmos','Earth Sciences',NULL,5,NULL),(506,'Janus','Bioscience & Biotechnology, Pharmacy',NULL,5,NULL),(507,'HUE','Home Science',NULL,5,NULL);
/*!40000 ALTER TABLE `fests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `five_fold`
--

DROP TABLE IF EXISTS `five_fold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `five_fold` (
  `activity_id` int NOT NULL AUTO_INCREMENT,
  `activity_name` varchar(100) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `venue` varchar(100) DEFAULT NULL,
  `admin_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`activity_id`),
  KEY `admin_id` (`admin_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `five_fold_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`),
  CONSTRAINT `five_fold_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=263 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `five_fold`
--

LOCK TABLES `five_fold` WRITE;
/*!40000 ALTER TABLE `five_fold` DISABLE KEYS */;
INSERT INTO `five_fold` VALUES (200,'Classical Dance (Bharatnatyam/Kathak/Manipuri)','AESTHETIC EDUCATION','Nupur Mandir / Kala Mandir',2,NULL),(201,'Folk Dance','AESTHETIC EDUCATION','Nupur Mandir / Kala Mandir',2,NULL),(202,'Creative Art','AESTHETIC EDUCATION','Kala Mandir/Shilp Mandir',2,NULL),(203,'Music-Instrumental (Guitar/Orchestra/Sarod/Sitar/Tabla/Violin)','AESTHETIC EDUCATION','Sur Mandir Evening (4.00 PM to 6.00PM)',2,NULL),(204,'Music-Vocal','AESTHETIC EDUCATION','Sur Mandir Evening (4.00 PM to 6.00PM)',2,NULL),(205,'Theatre','AESTHETIC EDUCATION','Sur Mandir Evening (4.00 PM to 6.00PM)',2,NULL),(206,'Banasthali Band','AESTHETIC EDUCATION','Sur Mandir Evening (4.00 PM to 6.00PM)',2,NULL),(207,'Aerobics','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(208,'Archery','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(209,'Athletics','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(210,'Badminton','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(211,'Basketball','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(212,'Cricket','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(213,'Equestrian','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(214,'Handball','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(215,'Hockey','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(216,'Martial Arts','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(217,'Kabaddi','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(218,'Kho-Kho','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(219,'Net Ball','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(220,'Rope Mallakhamb','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(221,'Shooting','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(222,'Soft Ball','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(223,'Football','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(224,'Gymnastics','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(225,'Swimming','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(226,'Table Tennis','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(227,'Tennis','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(228,'Throwball','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(229,'Volleyball','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(230,'Weight Training','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(231,'Yoga','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(232,'Combative Sports','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(233,'Pol Mallakhamb','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(234,'Squash','PHYSICAL EDUCATION','Room No. 10, Gyan Mandir / Vidula Maidan / Fly Club Office (Vidhya Mandir)',2,NULL),(235,'Art and Craft with Ornamental Design (2D and 3D)','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(236,'Art and Craft with Ornamental Design (Ropes)','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(237,'Art and Crafts with Fabric','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(238,'Craft and Design Methods','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(239,'Design for Commercially Profitable Project','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(240,'Digital Art Lab','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(241,'Fabric Construction in Textile','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(242,'Hand Embroidery','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(243,'Jewellery Design','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(244,'Modernization of Ancient Art by Block Printing','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(245,'Photography Lab','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(246,'Soft Material Studies Lab','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(247,'Stencil Printing','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(248,'Surface Ornamentation','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(249,'Woven Design','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(250,'Yarn Craft','PRACTICAL EDUCATION','Room No. 108, Department of Design (Shilp Mandir)',2,NULL),(251,'Extension Programs for Women Empowerment','PRACTICAL EDUCATION','Vani Mandir',2,NULL),(252,'FM Radio','PRACTICAL EDUCATION','FM Radio, Vigyan Mandir',2,NULL),(253,'Informal Education','PRACTICAL EDUCATION','Anopcharik Shiksha Kendra',2,NULL),(254,'Nutri Gardening and Post-Harvest value Addition','PRACTICAL EDUCATION','Department of Home Science (Gyan Mandir)',2,NULL),(255,'Life Skills','PRACTICAL EDUCATION','Department of Psychology (Vani Mandir)',2,NULL),(256,'Social Intelligence and Conflict Resolution','PRACTICAL EDUCATION','Department of Commerce and Management (Pragya Mandir)',2,NULL),(257,'Personal Finance Advisory-I','PRACTICAL EDUCATION','Department of Commerce and Management (Pragya Mandir)',2,NULL),(258,'Personal Finance Advisory-II','PRACTICAL EDUCATION','Department of Commerce and Management (Pragya Mandir)',2,NULL),(259,'Banasthali Seva Dal (BSD)','SERVICE & LEADERSHIP','In front of Vani Mandir',2,NULL),(260,'National Service Scheme (NSS)','SERVICE & LEADERSHIP','NSS Office, Vidya Mandir',2,NULL),(261,'National Cadet Corps (NCC)','SERVICE & LEADERSHIP','Selected Students',2,NULL),(262,'Banasthali Campus Ethics','MORAL EDUCATION','Vidyapith Campus Wide',2,NULL);
/*!40000 ALTER TABLE `five_fold` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `status` enum('Active','Restricted','Removed') DEFAULT 'Active',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workshops`
--

DROP TABLE IF EXISTS `workshops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workshops` (
  `workshop_id` int NOT NULL AUTO_INCREMENT,
  `workshop_name` varchar(100) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `venue` varchar(100) DEFAULT NULL,
  `admin_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`workshop_id`),
  KEY `admin_id` (`admin_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `workshops_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`),
  CONSTRAINT `workshops_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=406 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workshops`
--

LOCK TABLES `workshops` WRITE;
/*!40000 ALTER TABLE `workshops` DISABLE KEYS */;
INSERT INTO `workshops` VALUES (400,'Litiwts','Orientation on 1 August 2025 at 5:00 PM','Prabha Mandir Audi-1',4,NULL),(401,'Adhyay','Book Cafe on 25 August 2025 at 9:00 AM','Ratan Mandir',4,NULL),(402,'Expressio','Panel Discussion on 25 August 2025 at 6:00 PM','Nav Mandir',4,NULL),(403,'Aayam','Orientation on 6 September 2025 at 6:00 PM','Room No. 119, Ratan Mandir',4,NULL),(404,'Sarokar','Bharat: A Land of Political Innovations on 8 September 2025 at 10:00 AM','Gyan Mandir Auditorium',4,NULL),(405,'Tag der Deutschen Sprache','German Language Day on 15 September 2025 at 5:00 PM','Gyan Mandir Auditorium',4,NULL);
/*!40000 ALTER TABLE `workshops` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-27 20:53:12