-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: grocery_billing_system
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(255) DEFAULT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Vegetables','Carrots',1.50),(2,'Fruits','Apples',2.00),(3,'Dairy','Milk',3.50),(4,'Bakery','Bread',2.50),(5,'Snacks','Chips',1.75),(6,'Beverages','Soda',1.25),(7,'Vegetables','Broccoli',2.00),(8,'Vegetables','Tomatoes',1.75),(9,'Vegetables','Cucumbers',1.50),(10,'Vegetables','Bell Peppers',1.80),(11,'Vegetables','Spinach',2.25),(12,'Fruits','Bananas',1.20),(13,'Fruits','Oranges',1.50),(14,'Fruits','Grapes',2.50),(15,'Fruits','Strawberries',3.00),(16,'Fruits','Pineapple',2.75),(17,'Dairy','Cheese',4.50),(18,'Dairy','Yogurt',2.25),(19,'Dairy','Butter',3.00),(20,'Dairy','Eggs',1.80),(21,'Dairy','Cream',2.75),(22,'Bakery','Baguette',2.75),(23,'Bakery','Croissants',1.50),(24,'Bakery','Muffins',1.25),(25,'Bakery','Doughnuts',1.80),(26,'Bakery','Cookies',2.00),(27,'Snacks','Pretzels',1.50),(28,'Snacks','Popcorn',1.25),(29,'Snacks','Nuts',2.50),(30,'Snacks','Granola Bars',1.80),(31,'Snacks','Cheese Puffs',1.75),(32,'Beverages','Water',1.00),(33,'Beverages','Juice',2.25),(34,'Beverages','Tea',1.50),(35,'Beverages','Coffee',2.00),(36,'Beverages','Energy Drink',2.50),(37,'Electronics','Smartphone',500.00),(38,'Electronics','Laptop',1200.00),(39,'Electronics','Headphones',80.00),(40,'Electronics','Smartwatch',150.00),(41,'Electronics','TV',700.00),(42,'Clothing','T-Shirt',15.00),(43,'Clothing','Jeans',40.00),(44,'Clothing','Dress',35.00),(45,'Clothing','Sneakers',50.00),(46,'Clothing','Jacket',60.00);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-19 11:26:08
