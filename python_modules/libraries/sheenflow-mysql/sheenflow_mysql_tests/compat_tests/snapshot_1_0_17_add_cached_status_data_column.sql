-- MySQL dump 10.13  Distrib 8.0.31, for macos12.6 (x86_64)
--
-- Host: localhost    Database: test_2
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('958a9495162d');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asset_event_tags`
--

DROP TABLE IF EXISTS `asset_event_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asset_event_tags` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `event_id` int DEFAULT NULL,
  `asset_key` text NOT NULL,
  `key` text NOT NULL,
  `value` text,
  `event_timestamp` timestamp(6) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_asset_event_tags_event_id` (`event_id`),
  KEY `idx_asset_event_tags` (`asset_key`(64),`key`(64),`value`(64)),
  CONSTRAINT `asset_event_tags_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event_logs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asset_event_tags`
--

LOCK TABLES `asset_event_tags` WRITE;
/*!40000 ALTER TABLE `asset_event_tags` DISABLE KEYS */;
INSERT INTO `asset_event_tags` VALUES (1,14,'[\"upstream_asset\"]','sheenflow/code_version','b2f62146-f2f9-4e21-816c-813d40face9b','2022-11-17 08:32:39.217428'),(2,14,'[\"upstream_asset\"]','sheenflow/logical_version','a6b37da4cf9895227adf8c3a20507d9b465c1e39b159429582c07db0db6fd1fa','2022-11-17 08:32:39.217428');
/*!40000 ALTER TABLE `asset_event_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asset_keys`
--

DROP TABLE IF EXISTS `asset_keys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asset_keys` (
  `id` int NOT NULL AUTO_INCREMENT,
  `asset_key` varchar(512) DEFAULT NULL,
  `last_materialization` text,
  `last_run_id` varchar(255) DEFAULT NULL,
  `asset_details` text,
  `wipe_timestamp` timestamp(6) NULL DEFAULT NULL,
  `last_materialization_timestamp` timestamp(6) NULL DEFAULT NULL,
  `tags` text,
  `create_timestamp` datetime(6) DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `asset_key` (`asset_key`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asset_keys`
--

LOCK TABLES `asset_keys` WRITE;
/*!40000 ALTER TABLE `asset_keys` DISABLE KEYS */;
INSERT INTO `asset_keys` VALUES (1,'[\"upstream_asset\"]','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"StepMaterializationData\", \"asset_lineage\": [], \"materialization\": {\"__class__\": \"AssetMaterialization\", \"asset_key\": {\"__class__\": \"AssetKey\", \"path\": [\"upstream_asset\"]}, \"description\": null, \"metadata_entries\": [{\"__class__\": \"EventMetadataEntry\", \"description\": null, \"entry_data\": {\"__class__\": \"PathMetadataEntryData\", \"path\": \"/Users/claire/dagster_home_mysql/storage/upstream_asset\"}, \"label\": \"path\"}], \"partition\": null, \"tags\": {\"sheenflow/code_version\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"sheenflow/logical_version\": \"a6b37da4cf9895227adf8c3a20507d9b465c1e39b159429582c07db0db6fd1fa\"}}}, \"event_type_value\": \"ASSET_MATERIALIZATION\", \"logging_tags\": {\"pipeline_name\": \"__ASSET_JOB\", \"pipeline_tags\": \"{\'.dagster/grpc_info\': \'{\\\"host\\\": \\\"localhost\\\", \\\"socket\\\": \\\"/var/folders/lr/mcmhlx2177953tcj5m7v8l3h0000gn/T/tmpxpq1vx51\\\"}\', \'dagster/step_selection\': \'upstream_asset\'}\", \"resource_fn_name\": \"None\", \"resource_name\": \"None\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"solid_name\": \"upstream_asset\", \"step_key\": \"upstream_asset\"}, \"message\": \"Materialized value upstream_asset.\", \"pid\": 48179, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}, \"step_handle\": {\"__class__\": \"StepHandle\", \"key\": \"upstream_asset\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}}, \"step_key\": \"upstream_asset\", \"step_kind_value\": \"COMPUTE\"}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": \"upstream_asset\", \"timestamp\": 1668645159.217428, \"user_message\": \"Materialized value upstream_asset.\"}','b2f62146-f2f9-4e21-816c-813d40face9b',NULL,NULL,'2022-11-17 08:32:39.217428',NULL,'2022-11-16 16:32:31.142155');
/*!40000 ALTER TABLE `asset_keys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bulk_actions`
--

DROP TABLE IF EXISTS `bulk_actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bulk_actions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `key` varchar(32) NOT NULL,
  `status` varchar(255) NOT NULL,
  `timestamp` timestamp(6) NOT NULL,
  `body` text,
  `action_type` varchar(32) DEFAULT NULL,
  `selector_id` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `idx_bulk_actions_action_type` (`action_type`),
  KEY `idx_bulk_actions` (`key`),
  KEY `idx_bulk_actions_selector_id` (`selector_id`(64)),
  KEY `idx_bulk_actions_status` (`status`(32))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bulk_actions`
--

LOCK TABLES `bulk_actions` WRITE;
/*!40000 ALTER TABLE `bulk_actions` DISABLE KEYS */;
/*!40000 ALTER TABLE `bulk_actions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daemon_heartbeats`
--

DROP TABLE IF EXISTS `daemon_heartbeats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daemon_heartbeats` (
  `daemon_type` varchar(255) NOT NULL,
  `daemon_id` varchar(255) DEFAULT NULL,
  `timestamp` timestamp(6) NOT NULL,
  `body` text,
  UNIQUE KEY `daemon_type` (`daemon_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daemon_heartbeats`
--

LOCK TABLES `daemon_heartbeats` WRITE;
/*!40000 ALTER TABLE `daemon_heartbeats` DISABLE KEYS */;
/*!40000 ALTER TABLE `daemon_heartbeats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_logs`
--

DROP TABLE IF EXISTS `event_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `run_id` varchar(255) DEFAULT NULL,
  `event` text NOT NULL,
  `dagster_event_type` text,
  `timestamp` timestamp(6) NULL DEFAULT NULL,
  `step_key` text,
  `asset_key` text,
  `partition` text,
  PRIMARY KEY (`id`),
  KEY `idx_events_by_run_id` (`run_id`(64),`id`),
  KEY `idx_step_key` (`step_key`(32)),
  KEY `idx_event_type` (`dagster_event_type`(64),`id`),
  KEY `idx_events_by_asset` (`asset_key`(64),`dagster_event_type`(64),`id`),
  KEY `idx_events_by_asset_partition` (`asset_key`(64),`dagster_event_type`(64),`partition`(64),`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_logs`
--

LOCK TABLES `event_logs` WRITE;
/*!40000 ALTER TABLE `event_logs` DISABLE KEYS */;
INSERT INTO `event_logs` VALUES (1,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"AssetMaterializationPlannedData\", \"asset_key\": {\"__class__\": \"AssetKey\", \"path\": [\"upstream_asset\"]}}, \"event_type_value\": \"ASSET_MATERIALIZATION_PLANNED\", \"logging_tags\": {}, \"message\": \"__ASSET_JOB intends to materialize asset [\\\"upstream_asset\\\"]\", \"pid\": null, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": null, \"step_handle\": null, \"step_key\": null, \"step_kind_value\": null}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": null, \"timestamp\": 1668645151.1392808, \"user_message\": \"\"}','ASSET_MATERIALIZATION_PLANNED','2022-11-17 08:32:31.139281',NULL,'[\"upstream_asset\"]',NULL),(2,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": null, \"event_type_value\": \"PIPELINE_STARTING\", \"logging_tags\": {}, \"message\": null, \"pid\": null, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": null, \"step_handle\": null, \"step_key\": null, \"step_kind_value\": null}, \"error_info\": null, \"level\": 20, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": null, \"timestamp\": 1668645151.1452742, \"user_message\": \"\"}','PIPELINE_STARTING','2022-11-17 08:32:31.145274',NULL,NULL,NULL),(3,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"EngineEventData\", \"error\": null, \"marker_end\": null, \"marker_start\": null, \"metadata_entries\": [{\"__class__\": \"EventMetadataEntry\", \"description\": null, \"entry_data\": {\"__class__\": \"TextMetadataEntryData\", \"text\": \"48176\"}, \"label\": \"pid\"}]}, \"event_type_value\": \"ENGINE_EVENT\", \"logging_tags\": {}, \"message\": \"Started process for run (pid: 48176).\", \"pid\": null, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": null, \"step_handle\": null, \"step_key\": null, \"step_kind_value\": null}, \"error_info\": null, \"level\": 20, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": null, \"timestamp\": 1668645153.2225559, \"user_message\": \"\"}','ENGINE_EVENT','2022-11-17 08:32:33.222556',NULL,NULL,NULL),(4,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": null, \"event_type_value\": \"PIPELINE_START\", \"logging_tags\": {}, \"message\": \"Started execution of run for \\\"__ASSET_JOB\\\".\", \"pid\": 48176, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": null, \"step_handle\": null, \"step_key\": null, \"step_kind_value\": null}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": null, \"timestamp\": 1668645155.6940742, \"user_message\": \"Started execution of run for \\\"__ASSET_JOB\\\".\"}','PIPELINE_START','2022-11-17 08:32:35.694074',NULL,NULL,NULL),(5,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"EngineEventData\", \"error\": null, \"marker_end\": null, \"marker_start\": null, \"metadata_entries\": [{\"__class__\": \"EventMetadataEntry\", \"description\": null, \"entry_data\": {\"__class__\": \"TextMetadataEntryData\", \"text\": \"48176\"}, \"label\": \"pid\"}, {\"__class__\": \"EventMetadataEntry\", \"description\": null, \"entry_data\": {\"__class__\": \"TextMetadataEntryData\", \"text\": \"[\'upstream_asset\']\"}, \"label\": \"step_keys\"}]}, \"event_type_value\": \"ENGINE_EVENT\", \"logging_tags\": {}, \"message\": \"Executing steps using multiprocess executor: parent process (pid: 48176)\", \"pid\": 48176, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": null, \"step_handle\": null, \"step_key\": null, \"step_kind_value\": null}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": null, \"timestamp\": 1668645155.747735, \"user_message\": \"Executing steps using multiprocess executor: parent process (pid: 48176)\"}','ENGINE_EVENT','2022-11-17 08:32:35.747735',NULL,NULL,NULL),(6,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"EngineEventData\", \"error\": null, \"marker_end\": null, \"marker_start\": \"step_process_start\", \"metadata_entries\": []}, \"event_type_value\": \"STEP_WORKER_STARTING\", \"logging_tags\": {\"pipeline_name\": \"__ASSET_JOB\", \"pipeline_tags\": \"{\'.dagster/grpc_info\': \'{\\\"host\\\": \\\"localhost\\\", \\\"socket\\\": \\\"/var/folders/lr/mcmhlx2177953tcj5m7v8l3h0000gn/T/tmpxpq1vx51\\\"}\', \'dagster/step_selection\': \'upstream_asset\'}\", \"resource_fn_name\": \"None\", \"resource_name\": \"None\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"solid_name\": \"upstream_asset\", \"step_key\": \"upstream_asset\"}, \"message\": \"Launching subprocess for \\\"upstream_asset\\\".\", \"pid\": 48176, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}, \"step_handle\": {\"__class__\": \"StepHandle\", \"key\": \"upstream_asset\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}}, \"step_key\": \"upstream_asset\", \"step_kind_value\": \"COMPUTE\"}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": \"upstream_asset\", \"timestamp\": 1668645155.774718, \"user_message\": \"Launching subprocess for \\\"upstream_asset\\\".\"}','STEP_WORKER_STARTING','2022-11-17 08:32:35.774718','upstream_asset',NULL,NULL),(7,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"EngineEventData\", \"error\": null, \"marker_end\": \"step_process_start\", \"marker_start\": null, \"metadata_entries\": [{\"__class__\": \"EventMetadataEntry\", \"description\": null, \"entry_data\": {\"__class__\": \"TextMetadataEntryData\", \"text\": \"48179\"}, \"label\": \"pid\"}]}, \"event_type_value\": \"STEP_WORKER_STARTED\", \"logging_tags\": {}, \"message\": \"Executing step \\\"upstream_asset\\\" in subprocess.\", \"pid\": 48179, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": null, \"step_handle\": null, \"step_key\": \"upstream_asset\", \"step_kind_value\": null}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": \"upstream_asset\", \"timestamp\": 1668645159.118706, \"user_message\": \"Executing step \\\"upstream_asset\\\" in subprocess.\"}','STEP_WORKER_STARTED','2022-11-17 08:32:39.118706','upstream_asset',NULL,NULL),(8,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"EngineEventData\", \"error\": null, \"marker_end\": null, \"marker_start\": \"resources\", \"metadata_entries\": []}, \"event_type_value\": \"RESOURCE_INIT_STARTED\", \"logging_tags\": {}, \"message\": \"Starting initialization of resources [io_manager].\", \"pid\": 48179, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": null, \"step_handle\": {\"__class__\": \"StepHandle\", \"key\": \"upstream_asset\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}}, \"step_key\": \"upstream_asset\", \"step_kind_value\": null}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": \"upstream_asset\", \"timestamp\": 1668645159.127358, \"user_message\": \"Starting initialization of resources [io_manager].\"}','RESOURCE_INIT_STARTED','2022-11-17 08:32:39.127358','upstream_asset',NULL,NULL),(9,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"EngineEventData\", \"error\": null, \"marker_end\": \"resources\", \"marker_start\": null, \"metadata_entries\": [{\"__class__\": \"EventMetadataEntry\", \"description\": null, \"entry_data\": {\"__class__\": \"PythonArtifactMetadataEntryData\", \"module\": \"dagster._core.storage.fs_io_manager\", \"name\": \"PickledObjectFilesystemIOManager\"}, \"label\": \"io_manager\"}, {\"__class__\": \"EventMetadataEntry\", \"description\": null, \"entry_data\": {\"__class__\": \"TextMetadataEntryData\", \"text\": \"0.14ms\"}, \"label\": \"io_manager:init_time\"}]}, \"event_type_value\": \"RESOURCE_INIT_SUCCESS\", \"logging_tags\": {}, \"message\": \"Finished initialization of resources [io_manager].\", \"pid\": 48179, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": null, \"step_handle\": {\"__class__\": \"StepHandle\", \"key\": \"upstream_asset\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}}, \"step_key\": \"upstream_asset\", \"step_kind_value\": null}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": \"upstream_asset\", \"timestamp\": 1668645159.1342359, \"user_message\": \"Finished initialization of resources [io_manager].\"}','RESOURCE_INIT_SUCCESS','2022-11-17 08:32:39.134236','upstream_asset',NULL,NULL),(10,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"ComputeLogsCaptureData\", \"external_url\": null, \"log_key\": \"qrqrjkzj\", \"step_keys\": [\"upstream_asset\"]}, \"event_type_value\": \"LOGS_CAPTURED\", \"logging_tags\": {}, \"message\": \"Started capturing logs in process (pid: 48179).\", \"pid\": 48179, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": null, \"step_handle\": null, \"step_key\": null, \"step_kind_value\": null}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": null, \"timestamp\": 1668645159.166634, \"user_message\": \"Started capturing logs in process (pid: 48179).\"}','LOGS_CAPTURED','2022-11-17 08:32:39.166634',NULL,NULL,NULL),(11,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": null, \"event_type_value\": \"STEP_START\", \"logging_tags\": {\"pipeline_name\": \"__ASSET_JOB\", \"pipeline_tags\": \"{\'.dagster/grpc_info\': \'{\\\"host\\\": \\\"localhost\\\", \\\"socket\\\": \\\"/var/folders/lr/mcmhlx2177953tcj5m7v8l3h0000gn/T/tmpxpq1vx51\\\"}\', \'dagster/step_selection\': \'upstream_asset\'}\", \"resource_fn_name\": \"None\", \"resource_name\": \"None\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"solid_name\": \"upstream_asset\", \"step_key\": \"upstream_asset\"}, \"message\": \"Started execution of step \\\"upstream_asset\\\".\", \"pid\": 48179, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}, \"step_handle\": {\"__class__\": \"StepHandle\", \"key\": \"upstream_asset\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}}, \"step_key\": \"upstream_asset\", \"step_kind_value\": \"COMPUTE\"}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": \"upstream_asset\", \"timestamp\": 1668645159.1786811, \"user_message\": \"Started execution of step \\\"upstream_asset\\\".\"}','STEP_START','2022-11-17 08:32:39.178681','upstream_asset',NULL,NULL),(12,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"StepOutputData\", \"metadata_entries\": [], \"step_output_handle\": {\"__class__\": \"StepOutputHandle\", \"mapping_key\": null, \"output_name\": \"result\", \"step_key\": \"upstream_asset\"}, \"type_check_data\": {\"__class__\": \"TypeCheckData\", \"description\": null, \"label\": \"result\", \"metadata_entries\": [], \"success\": true}, \"version\": null}, \"event_type_value\": \"STEP_OUTPUT\", \"logging_tags\": {\"pipeline_name\": \"__ASSET_JOB\", \"pipeline_tags\": \"{\'.dagster/grpc_info\': \'{\\\"host\\\": \\\"localhost\\\", \\\"socket\\\": \\\"/var/folders/lr/mcmhlx2177953tcj5m7v8l3h0000gn/T/tmpxpq1vx51\\\"}\', \'dagster/step_selection\': \'upstream_asset\'}\", \"resource_fn_name\": \"None\", \"resource_name\": \"None\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"solid_name\": \"upstream_asset\", \"step_key\": \"upstream_asset\"}, \"message\": \"Yielded output \\\"result\\\" of type \\\"Any\\\". (Type check passed).\", \"pid\": 48179, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}, \"step_handle\": {\"__class__\": \"StepHandle\", \"key\": \"upstream_asset\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}}, \"step_key\": \"upstream_asset\", \"step_kind_value\": \"COMPUTE\"}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": \"upstream_asset\", \"timestamp\": 1668645159.187447, \"user_message\": \"Yielded output \\\"result\\\" of type \\\"Any\\\". (Type check passed).\"}','STEP_OUTPUT','2022-11-17 08:32:39.187447','upstream_asset',NULL,NULL),(13,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": null, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": \"upstream_asset\", \"timestamp\": 1668645159.19417, \"user_message\": \"Writing file at: /Users/claire/dagster_home_mysql/storage/upstream_asset\"}',NULL,'2022-11-17 08:32:39.194170','upstream_asset',NULL,NULL),(14,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"StepMaterializationData\", \"asset_lineage\": [], \"materialization\": {\"__class__\": \"AssetMaterialization\", \"asset_key\": {\"__class__\": \"AssetKey\", \"path\": [\"upstream_asset\"]}, \"description\": null, \"metadata_entries\": [{\"__class__\": \"EventMetadataEntry\", \"description\": null, \"entry_data\": {\"__class__\": \"PathMetadataEntryData\", \"path\": \"/Users/claire/dagster_home_mysql/storage/upstream_asset\"}, \"label\": \"path\"}], \"partition\": null, \"tags\": {\"dagster/code_version\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"dagster/logical_version\": \"a6b37da4cf9895227adf8c3a20507d9b465c1e39b159429582c07db0db6fd1fa\"}}}, \"event_type_value\": \"ASSET_MATERIALIZATION\", \"logging_tags\": {\"pipeline_name\": \"__ASSET_JOB\", \"pipeline_tags\": \"{\'.dagster/grpc_info\': \'{\\\"host\\\": \\\"localhost\\\", \\\"socket\\\": \\\"/var/folders/lr/mcmhlx2177953tcj5m7v8l3h0000gn/T/tmpxpq1vx51\\\"}\', \'dagster/step_selection\': \'upstream_asset\'}\", \"resource_fn_name\": \"None\", \"resource_name\": \"None\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"solid_name\": \"upstream_asset\", \"step_key\": \"upstream_asset\"}, \"message\": \"Materialized value upstream_asset.\", \"pid\": 48179, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}, \"step_handle\": {\"__class__\": \"StepHandle\", \"key\": \"upstream_asset\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}}, \"step_key\": \"upstream_asset\", \"step_kind_value\": \"COMPUTE\"}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": \"upstream_asset\", \"timestamp\": 1668645159.217428, \"user_message\": \"Materialized value upstream_asset.\"}','ASSET_MATERIALIZATION','2022-11-17 08:32:39.217428','upstream_asset','[\"upstream_asset\"]',NULL),(15,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"HandledOutputData\", \"manager_key\": \"io_manager\", \"metadata_entries\": [{\"__class__\": \"EventMetadataEntry\", \"description\": null, \"entry_data\": {\"__class__\": \"PathMetadataEntryData\", \"path\": \"/Users/claire/dagster_home_mysql/storage/upstream_asset\"}, \"label\": \"path\"}], \"output_name\": \"result\"}, \"event_type_value\": \"HANDLED_OUTPUT\", \"logging_tags\": {\"pipeline_name\": \"__ASSET_JOB\", \"pipeline_tags\": \"{\'.dagster/grpc_info\': \'{\\\"host\\\": \\\"localhost\\\", \\\"socket\\\": \\\"/var/folders/lr/mcmhlx2177953tcj5m7v8l3h0000gn/T/tmpxpq1vx51\\\"}\', \'dagster/step_selection\': \'upstream_asset\'}\", \"resource_fn_name\": \"None\", \"resource_name\": \"None\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"solid_name\": \"upstream_asset\", \"step_key\": \"upstream_asset\"}, \"message\": \"Handled output \\\"result\\\" using IO manager \\\"io_manager\\\"\", \"pid\": 48179, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}, \"step_handle\": {\"__class__\": \"StepHandle\", \"key\": \"upstream_asset\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}}, \"step_key\": \"upstream_asset\", \"step_kind_value\": \"COMPUTE\"}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": \"upstream_asset\", \"timestamp\": 1668645159.244406, \"user_message\": \"Handled output \\\"result\\\" using IO manager \\\"io_manager\\\"\"}','HANDLED_OUTPUT','2022-11-17 08:32:39.244406','upstream_asset',NULL,NULL),(16,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"StepSuccessData\", \"duration_ms\": 82.88181700000008}, \"event_type_value\": \"STEP_SUCCESS\", \"logging_tags\": {\"pipeline_name\": \"__ASSET_JOB\", \"pipeline_tags\": \"{\'.dagster/grpc_info\': \'{\\\"host\\\": \\\"localhost\\\", \\\"socket\\\": \\\"/var/folders/lr/mcmhlx2177953tcj5m7v8l3h0000gn/T/tmpxpq1vx51\\\"}\', \'dagster/step_selection\': \'upstream_asset\'}\", \"resource_fn_name\": \"None\", \"resource_name\": \"None\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"solid_name\": \"upstream_asset\", \"step_key\": \"upstream_asset\"}, \"message\": \"Finished execution of step \\\"upstream_asset\\\" in 82ms.\", \"pid\": 48179, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}, \"step_handle\": {\"__class__\": \"StepHandle\", \"key\": \"upstream_asset\", \"solid_handle\": {\"__class__\": \"SolidHandle\", \"name\": \"upstream_asset\", \"parent\": null}}, \"step_key\": \"upstream_asset\", \"step_kind_value\": \"COMPUTE\"}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": \"upstream_asset\", \"timestamp\": 1668645159.269, \"user_message\": \"Finished execution of step \\\"upstream_asset\\\" in 82ms.\"}','STEP_SUCCESS','2022-11-17 08:32:39.269000','upstream_asset',NULL,NULL),(17,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"EngineEventData\", \"error\": null, \"marker_end\": null, \"marker_start\": null, \"metadata_entries\": [{\"__class__\": \"EventMetadataEntry\", \"description\": null, \"entry_data\": {\"__class__\": \"TextMetadataEntryData\", \"text\": \"48176\"}, \"label\": \"pid\"}]}, \"event_type_value\": \"ENGINE_EVENT\", \"logging_tags\": {}, \"message\": \"Multiprocess executor: parent process exiting after 3.89s (pid: 48176)\", \"pid\": 48176, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": null, \"step_handle\": null, \"step_key\": null, \"step_kind_value\": null}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": null, \"timestamp\": 1668645159.664862, \"user_message\": \"Multiprocess executor: parent process exiting after 3.89s (pid: 48176)\"}','ENGINE_EVENT','2022-11-17 08:32:39.664862',NULL,NULL,NULL),(18,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": null, \"event_type_value\": \"PIPELINE_SUCCESS\", \"logging_tags\": {}, \"message\": \"Finished execution of run for \\\"__ASSET_JOB\\\".\", \"pid\": 48176, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": null, \"step_handle\": null, \"step_key\": null, \"step_kind_value\": null}, \"error_info\": null, \"level\": 10, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": null, \"timestamp\": 1668645159.675392, \"user_message\": \"Finished execution of run for \\\"__ASSET_JOB\\\".\"}','PIPELINE_SUCCESS','2022-11-17 08:32:39.675392',NULL,NULL,NULL),(19,'b2f62146-f2f9-4e21-816c-813d40face9b','{\"__class__\": \"EventLogEntry\", \"dagster_event\": {\"__class__\": \"DagsterEvent\", \"event_specific_data\": {\"__class__\": \"EngineEventData\", \"error\": null, \"marker_end\": null, \"marker_start\": null, \"metadata_entries\": []}, \"event_type_value\": \"ENGINE_EVENT\", \"logging_tags\": {}, \"message\": \"Process for run exited (pid: 48176).\", \"pid\": null, \"pipeline_name\": \"__ASSET_JOB\", \"solid_handle\": null, \"step_handle\": null, \"step_key\": null, \"step_kind_value\": null}, \"error_info\": null, \"level\": 20, \"message\": \"\", \"pipeline_name\": \"__ASSET_JOB\", \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"step_key\": null, \"timestamp\": 1668645159.717071, \"user_message\": \"\"}','ENGINE_EVENT','2022-11-17 08:32:39.717071',NULL,NULL,NULL);
/*!40000 ALTER TABLE `event_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instance_info`
--

DROP TABLE IF EXISTS `instance_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instance_info` (
  `run_storage_id` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instance_info`
--

LOCK TABLES `instance_info` WRITE;
/*!40000 ALTER TABLE `instance_info` DISABLE KEYS */;
INSERT INTO `instance_info` VALUES ('e6b1355e-a85f-44f5-87bc-3c8b20fc836b');
/*!40000 ALTER TABLE `instance_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instigators`
--

DROP TABLE IF EXISTS `instigators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instigators` (
  `id` int NOT NULL AUTO_INCREMENT,
  `selector_id` varchar(255) DEFAULT NULL,
  `repository_selector_id` varchar(255) DEFAULT NULL,
  `status` varchar(63) DEFAULT NULL,
  `instigator_type` varchar(63) DEFAULT NULL,
  `instigator_body` text,
  `create_timestamp` datetime(6) DEFAULT CURRENT_TIMESTAMP(6),
  `update_timestamp` datetime(6) DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `selector_id` (`selector_id`),
  KEY `ix_instigators_instigator_type` (`instigator_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instigators`
--

LOCK TABLES `instigators` WRITE;
/*!40000 ALTER TABLE `instigators` DISABLE KEYS */;
/*!40000 ALTER TABLE `instigators` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_ticks`
--

DROP TABLE IF EXISTS `job_ticks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_ticks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `job_origin_id` varchar(255) DEFAULT NULL,
  `selector_id` varchar(255) DEFAULT NULL,
  `status` varchar(63) DEFAULT NULL,
  `type` varchar(63) DEFAULT NULL,
  `timestamp` timestamp(6) NULL DEFAULT NULL,
  `tick_body` text,
  `create_timestamp` datetime(6) DEFAULT CURRENT_TIMESTAMP(6),
  `update_timestamp` datetime(6) DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `idx_job_tick_timestamp` (`job_origin_id`,`timestamp`),
  KEY `idx_tick_selector_timestamp` (`selector_id`,`timestamp`),
  KEY `ix_job_ticks_job_origin_id` (`job_origin_id`),
  KEY `idx_job_tick_status` (`job_origin_id`(32),`status`(32))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_ticks`
--

LOCK TABLES `job_ticks` WRITE;
/*!40000 ALTER TABLE `job_ticks` DISABLE KEYS */;
/*!40000 ALTER TABLE `job_ticks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `job_origin_id` varchar(255) DEFAULT NULL,
  `selector_id` varchar(255) DEFAULT NULL,
  `repository_origin_id` varchar(255) DEFAULT NULL,
  `status` varchar(63) DEFAULT NULL,
  `job_type` varchar(63) DEFAULT NULL,
  `job_body` text,
  `create_timestamp` datetime(6) DEFAULT CURRENT_TIMESTAMP(6),
  `update_timestamp` datetime(6) DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `job_origin_id` (`job_origin_id`),
  KEY `ix_jobs_job_type` (`job_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kvs`
--

DROP TABLE IF EXISTS `kvs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kvs` (
  `key` text NOT NULL,
  `value` text,
  UNIQUE KEY `idx_kvs_keys_unique` (`key`(64))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kvs`
--

LOCK TABLES `kvs` WRITE;
/*!40000 ALTER TABLE `kvs` DISABLE KEYS */;
/*!40000 ALTER TABLE `kvs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `run_tags`
--

DROP TABLE IF EXISTS `run_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `run_tags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `run_id` varchar(255) DEFAULT NULL,
  `key` text,
  `value` text,
  PRIMARY KEY (`id`),
  KEY `run_id` (`run_id`),
  KEY `idx_run_tags` (`key`(64),`value`(64)),
  CONSTRAINT `run_tags_ibfk_1` FOREIGN KEY (`run_id`) REFERENCES `runs` (`run_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `run_tags`
--

LOCK TABLES `run_tags` WRITE;
/*!40000 ALTER TABLE `run_tags` DISABLE KEYS */;
INSERT INTO `run_tags` VALUES (1,'b2f62146-f2f9-4e21-816c-813d40face9b','.sheenflow/repository','upstream_assets_repository@sheenflow_test.toys.repo'),(2,'b2f62146-f2f9-4e21-816c-813d40face9b','sheenflow/step_selection','upstream_asset'),(3,'b2f62146-f2f9-4e21-816c-813d40face9b','.sheenflow/grpc_info','{\"host\": \"localhost\", \"socket\": \"/var/folders/lr/mcmhlx2177953tcj5m7v8l3h0000gn/T/tmpxpq1vx51\"}');
/*!40000 ALTER TABLE `run_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `runs`
--

DROP TABLE IF EXISTS `runs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `runs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `run_id` varchar(255) DEFAULT NULL,
  `snapshot_id` varchar(255) DEFAULT NULL,
  `pipeline_name` text,
  `mode` text,
  `status` varchar(63) DEFAULT NULL,
  `run_body` text,
  `partition` text,
  `partition_set` text,
  `create_timestamp` datetime(6) DEFAULT CURRENT_TIMESTAMP(6),
  `update_timestamp` datetime(6) DEFAULT CURRENT_TIMESTAMP(6),
  `start_time` double DEFAULT NULL,
  `end_time` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `run_id` (`run_id`),
  KEY `fk_runs_snapshot_id_snapshots_snapshot_id` (`snapshot_id`),
  KEY `idx_run_partitions` (`partition_set`(64),`partition`(64)),
  KEY `idx_run_range` (`status`(32),`update_timestamp`,`create_timestamp`),
  KEY `idx_run_status` (`status`(32)),
  CONSTRAINT `fk_runs_snapshot_id_snapshots_snapshot_id` FOREIGN KEY (`snapshot_id`) REFERENCES `snapshots` (`snapshot_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `runs`
--

LOCK TABLES `runs` WRITE;
/*!40000 ALTER TABLE `runs` DISABLE KEYS */;
INSERT INTO `runs` VALUES (1,'b2f62146-f2f9-4e21-816c-813d40face9b','be10d19e5c8d18d6b7adb5124f5bfa4746f41bbc','__ASSET_JOB',NULL,'SUCCESS','{\"__class__\": \"PipelineRun\", \"asset_selection\": {\"__frozenset__\": [{\"__class__\": \"AssetKey\", \"path\": [\"upstream_asset\"]}]}, \"execution_plan_snapshot_id\": \"5fda2f5076f6375c2f0e7bd89296103ade204651\", \"external_pipeline_origin\": {\"__class__\": \"ExternalPipelineOrigin\", \"external_repository_origin\": {\"__class__\": \"ExternalRepositoryOrigin\", \"repository_location_origin\": {\"__class__\": \"ManagedGrpcPythonEnvRepositoryLocationOrigin\", \"loadable_target_origin\": {\"__class__\": \"LoadableTargetOrigin\", \"attribute\": null, \"executable_path\": null, \"module_name\": \"sheenflow_test.toys.repo\", \"package_name\": null, \"python_file\": null, \"working_directory\": null}, \"location_name\": \"sheenflow_test.toys.repo\"}, \"repository_name\": \"upstream_assets_repository\"}, \"pipeline_name\": \"__ASSET_JOB\"}, \"has_repository_load_data\": false, \"mode\": \"default\", \"parent_run_id\": null, \"pipeline_code_origin\": {\"__class__\": \"PipelinePythonOrigin\", \"pipeline_name\": \"__ASSET_JOB\", \"repository_origin\": {\"__class__\": \"RepositoryPythonOrigin\", \"code_pointer\": {\"__class__\": \"ModuleCodePointer\", \"fn_name\": \"upstream_assets_repository\", \"module\": \"sheenflow_test.toys.repo\", \"working_directory\": \"/Users/claire/sheenflow\"}, \"container_context\": {}, \"container_image\": null, \"entry_point\": [\"sheenflow\"], \"executable_path\": \"/Users/claire/.virtualenvs/sheenflow-dev/bin/python\"}}, \"pipeline_name\": \"__ASSET_JOB\", \"pipeline_snapshot_id\": \"be10d19e5c8d18d6b7adb5124f5bfa4746f41bbc\", \"root_run_id\": null, \"run_config\": {}, \"run_id\": \"b2f62146-f2f9-4e21-816c-813d40face9b\", \"solid_selection\": null, \"solids_to_execute\": null, \"status\": {\"__enum__\": \"PipelineRunStatus.SUCCESS\"}, \"step_keys_to_execute\": null, \"tags\": {\".sheenflow/grpc_info\": \"{\\\"host\\\": \\\"localhost\\\", \\\"socket\\\": \\\"/var/folders/lr/mcmhlx2177953tcj5m7v8l3h0000gn/T/tmpxpq1vx51\\\"}\", \"sheenflow/step_selection\": \"upstream_asset\"}}',NULL,NULL,'2022-11-16 16:32:31.136468','2022-11-17 00:32:39.692435',1668645155.740731,1668645159.692435);
/*!40000 ALTER TABLE `runs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `secondary_indexes`
--

DROP TABLE IF EXISTS `secondary_indexes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `secondary_indexes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `create_timestamp` datetime(6) DEFAULT CURRENT_TIMESTAMP(6),
  `migration_completed` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `secondary_indexes`
--

LOCK TABLES `secondary_indexes` WRITE;
/*!40000 ALTER TABLE `secondary_indexes` DISABLE KEYS */;
INSERT INTO `secondary_indexes` VALUES (1,'run_partitions','2022-11-16 16:32:16.471525','2022-11-16 16:32:16.465316'),(2,'run_repo_label_tags','2022-11-16 16:32:16.489310','2022-11-16 16:32:16.485745'),(3,'bulk_action_types','2022-11-16 16:32:16.523751','2022-11-16 16:32:16.519118'),(4,'run_start_end_overwritten','2022-11-16 16:32:16.576582','2022-11-16 16:32:16.571836'),(5,'asset_key_table','2022-11-16 16:32:16.833904','2022-11-16 16:32:16.828432'),(6,'asset_key_index_columns','2022-11-16 16:32:16.870300','2022-11-16 16:32:16.847210'),(7,'schedule_jobs_selector_id','2022-11-16 16:32:17.139400','2022-11-16 16:32:17.132622'),(8,'schedule_ticks_selector_id','2022-11-16 16:32:17.193070','2022-11-16 16:32:17.189040');
/*!40000 ALTER TABLE `secondary_indexes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `snapshots`
--

DROP TABLE IF EXISTS `snapshots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `snapshots` (
  `id` int NOT NULL AUTO_INCREMENT,
  `snapshot_id` varchar(255) NOT NULL,
  `snapshot_body` blob NOT NULL,
  `snapshot_type` varchar(63) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `snapshot_id` (`snapshot_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `snapshots`
--

LOCK TABLES `snapshots` WRITE;
/*!40000 ALTER TABLE `snapshots` DISABLE KEYS */;
INSERT INTO `snapshots` VALUES (1,'be798c95a00e2f274e9cca79fe0502fc356f02b8',_binary 'x�\�]is\�\��+(\�C�*[\�58\��l\�Y%��ei+��T\�=\"\� �\0�lƥ���DPC��(G�eK s�~\�\�\�s�G/�xB�\"�z��\�\�!$q\n)��\�2z<Ke|�\Z\�7�?\�\�}W����;O�$j\�PGl}�qU�q:\�\�r<����P\�<�q�b�t�$�!��AtK�\�e��y��o!�R:\0U�j?�[�<ũh:QU�Ї\�\�G\�g�\�\�aقӄ\�Q\�J\�F���!\�\�@��m\\?\�s:>�\�\�!��\0l\�3�\�%�i\"L&(|\�\�\�a\�\�\����Ic�\�6B���r\�v���\�\�x-\�?\�\�\�\�\���\�<No/���\�!;�oW�\�\rTH�Ͳd6m\�\�t��G�q^�;�x�i\�@��uQ��\�{{~��z�[o?$\�p\��nn�\�\�y�0|�x~|�\0�\�QP�M1h�v��\�\�C\���\���5__@�\�\�#D+`N�G]�ip*�pKz\�\�-��p��ۼ\�\�B\�ׂ?��\�\��l=�\�j��]�^�N�2\�1\nӤ�N`�\�\�y(��s\�C���H�Z��;!�M��s�L\�\��}�\' \�\�\�i\�!}KX6\�\��\�A`:<\��縖/L\�&!�\�z�s\�4r��\�M=�O\����P���5e�e��\�f۶\�s�j\Z\�\�aض�;�sM��\�;W˨}\�b�Y�O�����z~HB�\�\�\�D�=\�\�\�;\�祕~P_Ok�t��\�0\�nc\n�2�\�7U\�-�?�,��2W5��\�\�R\\D9�g\�Ue�&���\�D\\P�\�W-\�-3*\�_P\'�\0��\��M� C\�V�T\n4`f�\�yxc�t+C�~@�\�&��|<ywy�\�{0^�t\�&>\�k��(�q\\\��e:�\�\� �kz�\�ǃb|+\�U�hZҠEñ)+n\�1�60ڒ\�u��v��4�Th��P\�,?`�\�ڶ�^(!(�T߯Z���\�\�X�\�\�w\��$FQ°0\�ԠF�RN��\�9\�Q\�A�QSx�q]i��b�PP}{��-\��\�8�M,�[�x\�\�\�*3\�Gyi��1_�\��\�+\�*\�R�[\�أM\��n��W�\'-\�q=.�>ȀJ\�[\�a�\����允2__1�u`��8V 	�Ha\�(\�!Y\�\���gLO�\��)\�2\�Տr0\�>�$0��W�e�\�yi#\�|	�1R\�i|�Y����\�/\Z,��\�\�P�A�\�lSHǲ=\�?0\n6=SZ\�\rMaw\�\�\�*�\�[��QUp_^�6\�\���O&��\�\�\���j�k;�%�zp\"\�\n�Ð�\�\�=�7֘��k\�	��#�*[�\�]h�\�\�S.\�P\�\'\����\�j\�F5����nn}-a��\�\��\�|\�\�\�\�f����[_Hچr>\�\�r�(\�n�s\�l\�\�����Ėԡ�m\�!�\�T�Tr*��>\�\�\�\�ƾh\�i�6\�uy�O�K[�\'�\��I�\�\�i \�9Ε>5-���\�\����^\��\�F�t*R��US[\����D\��r�\�y�\�ɤ�8�!�\�9�e��v\�A\�NB��wz\�\����$�~\�#\�nn �sa���~��,9�%pI�?�\�����7E	y\�T/վ\�q6ʛ\�i�����{��t9}�\�\�\�et\�\�\�o\'�ൄ�!�\�qmʹ�\"d��`XhK\�\r���>;^���\�P�Ӷ<W��JJ\�g�,[VRdi\�0x�dH��Y���O�,7\�ڔ\�d��,\�\�0+`\�XQi�\�$�\�J_\�Dr\�Y H\�a\��\��q�����:keO.\�.qP\�֔�6\�{��MM$�iv ���eqa��\��Ե������fL�Idf��\��\�ƺ\�\�.=�h\�d�L\�\�)�gk!\�\�\�J;i��\�\�b\�\�\�D\�a?-z�ߟ�\�\�\�\�\�\�\��k�-a4�\nyTf\�Ŭ\�\�Lw�Wn~\�\�_}(��\�\�9�\�`4/Yn�Yyd��N֫e\�4\\�\�Nm\�\�M��-��ܻ�P\�r<��>a�\�#\���ms\���\�\�B밌\�N\���\�]&}Jh��_J\�f���͹Ѳ�� ^\�}Zog\�O!\�\�\�\�a\�L\�F1\�q�\�3�\'�23�9$jϵ�f��\�\�8WҷX5�~�j�)�e�jC(�\��\���XN�Veq\�j��qv2Ne\�\��:�`��1\�-\�<Nr2\�mޯZ4\n�~�?0�\�Ib0h�\�ԇ-\�E�4\�/m���)�\�\�ؔ��\�\�K\�\�\�\�\�\�\�\�\��+\�raАK�J�U�\�\�\���\�\��MbE��\�l�~\��,�Q1\�\��\�3]s6\�^l�ٙ���\�t�u?�\��|����@B��\�|H>J5Z�w-\�h��O�\�\\Q\'qiwz�\�bM,�J�#AH0\�\��	\�,\\\�{\�u�M�o�4��]{��!���X=�ݎ�|�ū\�J����**��\�9�Tk)2�\�r\�t\r�8�pv�3vP�c;\�\�U/΢MQ\�y�O3J��L}�\�\��W\�Z�\��0�\�\���5�h9l!�&s)	VH\�\�\�A\�\�!�\�m�(0\�\�N,i[\�\�ڃ<$�h}���]oGqR�F\�\���1\�\�qzn4E\����ѱbZ*�\���\Z��>S-R\�/:�&\nб��#\�1N[�{e��5�)=�M#\��Y�cTǃ\�e(���\�B�\�,~(8���ǈ&}��W�h�!ۑ�҂N��{�N�\�M\�v�а<IVm\�9��E\���Q9�]�\�z�z�B�X���n@pH�\�Ω��ftl�\�\��I\n]�\�J\n\�[\0�:��ٵ�k4`\�\�f��LA���g;�c\'ӬG2�_j\�`�P�4t8TƐ\�g\�\�\r\�i\��j�\�fS�̇��g\��\�:\�\�\�3/�Ԭ���,ѭ�D�\�Y�\�c�\�^�\0\�赖*k;�Ps�@M.\��*p\�\��\�\��\�\�h8.�Yz�\�7o�7I\�r��\�,��_�?!J�^�1N{]\�a\�z�2˄Nޤ*\�\�;\�׾h@\�8j��}\�Mo\�\�=h\�\��KCg�Ɲ[b\�\�W�*�\��\�\�\�[̞쾼Ŏ��Ζ\�Ӿ}\��\�N�լ\�DU\�jX�\�V\�?\�,�ޟ�\�\�!��T\�6\�jW\nI\�\�0�\�Ż\�\�d0��\�\�D�q��L�s�W\�Qy{�c\�\�К\�1�S�\�o�c;\�^\�Ko\nr{�\�\n�W^)�\�=X�\�Vn\�\�\�\�P��\�\�zS\�\'\�î@\�U֏���\�\�\n�\�`��\�>\�M\�o.�]��;��\�7\�\�\n�\�t%\�g�Z\�Y\�l\n}[\�j�gJi�\�\��\�\�֫X&��3\� 6�\���.wmS`�\��\n\\p\�\�\�\�\��+rN��T\n��C�8�\�+}B* \�㋶\���SeB�8�\�8U��k\�\�O\\����r��\�t8*��3\�׵,\��\�h@�ù\�n��{��.�b%^\�\�w]L�\�\�?\�N_\\�\\F?�*Q�l\r���U�L@\�f\Z�\�\�A�dz�e`e5�\"3\�	ߨN\\���\"��CX���6\�\�b��\n�\'\�F\�\�r\��J�~j\n=�L�v?\�}!\�`�{ɚv%�<\�\�\�ߍ\�l�Ü\��\�\�l\�i�W�0���|?-:��c\r�Y�hw&�p\�v.�����3\�	W�:*l����\'�zj%z\�U�Y\�=\�\�G\�]�l&��A�\�\�\��Yڔ�&\�d2�ߟئ���\�\�\�','PIPELINE'),(2,'be10d19e5c8d18d6b7adb5124f5bfa4746f41bbc',_binary 'x�\�]�s\�\��W0\�mgb�p�M�\�F�+e,e:�H\�cOD,\0\�f<�߻�Oԑ\")\�U2�\�p�o�\�\�\�{�k/�E\�\�2�{?Z�_�!�I���\��`\�D��\�&.E,.\'\��h}]|\�m]\�.6�>K\�xR��8\�\��\�g㮊.\�ú�\n	�(�a�\�\�Fi�B6\Zķ,A9�P%�ʹ\�\��8c\�5\�\�\�æ\�\�S�ɶu�K}��>:>�O\�˖����\�W\�6*,Y�z\\�\�u\�\�`㣋>\�H���!	q}\�\�!\�\�\�(t=( =�9�IYY���jn+$\�\�&@nٮ\�?o��o�\r;r=\'��H��\�K��fw\�N\�\�bM5o\�<\��\�F۴6\�\�\�`�o�?\\1\�Uo]\�%\�\�ޜ��\�\�\�\�\�i\�:-\�\�Ah���0{\�#\�?�_>�\�iv@tc3&O{D\�\�\�\�7�\�p`G���. Q\�\�\"�q�B0\�D�\0�)\�E\�Q�C\�\�pv[�;\��F\�ǿ����mfv&ھy׮��S�\�l�Ҷ��١\�BAU@�\\JC\�3�|\�\�=\�l\�\��\�gj�6\�\�=�>φ\�hH)��#�	m\�\�(�=E�\'\�|\'�v\�g!�\�z�w\�r\�\�M3�\�\���$*)ղf\�u\\;\�=\�]\�\�C�PM#7x�m\�\�\�]@3�m\�\�52��\�pŝ d��F6cAH	\�\�l:\\F\" ����\'����\�\��\�Y���\�*�m\"A#S#����=fe�{�gqY���w�]Jʸ������L��ԵM|�����\��	3j\�_2�2�@�}nK\�%�+P��Q�)�̦Z�\�ol�\�dh\�\�\�\�\�2U��\'o/\�W�c\�\�\�N�$\�x�*�\�E<\�8�\�:>a\�\��v*||V��r-ږh\�rlƊ\�{�h����A=��=���\�\0�#S\�?\�D��(\'��$\�$�m\�U�\0��W�\�W���\�\�VX�\�\��\n,��VY����\�bV�RN�\�\��\�Q\�A�dq[x�\�}\��Lb*���D�} \��`�\�<\�%�د}�\�\r\������\��\�?X\�\�L\�k\�j\�2�[&أK7�n�N֢�\�\�!��!��)\�=W�4�\�\�0p\Zٔ�\�i��T\�\�s\"E�BZH�ĈH\�)�\"$z��ɣoO1Wq��~T�U\���\'�5�\�ªrd+*�\�\�K(��VO\�ʋ?J(n��d��Y\�\r\�D!�ܵ�\�7\0��`;��\�}jK��\�`T9d�3�ꂇ\�\�~H|\�0�zA��N�\�x衶��9R�� \��ȓ�R�i\�n�1{\�0�\�=���ly`:wa��;O�\�B5�8����/��լs\�ƺ�\�]\�\�\'�_t\�E7\���\�z��r\�|!i\��ċ/\�����Q\�M��;_�ډvW1�\�=GR\�\�#\�~\�\����!	�畍}\�\�\'\�Nc��\�\�dW��@*)�9\�Y�\"Ε!����.���^\����l\�T�76���B5k�ؑ\�?<N�\�#ŕt��#Qx\�q)��=\��\�\�$�~\�;={~\�[�V�샕\�77P����~e?O�A�_�S���\�\�\��UO�����sH��z_\�8\��\�T�\�ҽڌA����x�\�2��\����G\�ZA\�O��.B1I9.9N]�8�\�\�\�׫\r\�:\�\�z1WK��lʕU\�J�,m�\�\���?�2O��7\�)�\�fޘ�3�\�A\�D+�P�\�\�}*�(�$�\\q�\�v;?.s��b�\�_g�\�\�\�%z؆r7F��rw������ȍ$r0t!]�ْ�.�0p��So�[bn7�l���\�<l�Ì)\�29(S\�w\n훵\�ka���0]\�h�\�\�q;��鎰\��\�ޝ�\�\�\�\�\�\�ɻk�-a����ʱ�y\�\�\�w�\�\�6�Կ�P\���\�\�s+�j_�\�\�\�\�\�\�z3�8Y?�*g\�b�ouj�\�nbCm1\�\�������\�AJ�\�\0���+|�f/�\�\�2�{ݳ�\�\�6v�\�)a�a)a�EzN�\�o΍U�G\�ƐZ\�f;3�A\�N�\�D$U:�\�!�D��}���8yT�5, ͙\�{�\�7���Gֹ��>\'�i�\�sM\�9�\�B�\�4\�ol%jZ�.��V\�l���u�\�&\�5�\�\��[�Yi\�\�q�SE>�X�~ݢU\�\�S\�\�9IS�ä�m}\�BS\�S���4)��sE�۲q\��{)\����\��7c\�A�T�2r?\�\r�r�\�y�/�\�\�,\�������4\�ĩ�·�g�\�\�\�\�`\�h3ӵg\�Ŧ۝iX\�\�\�6Z\�\�\�\�q�\�WkN;H$tկχ�̀�\�{I\��q���;\�5M2��`�T\�\0qg7h,6Ģ�d5Q�q@ mP�gQ\�0P�\�\\\�C;�\�>\��\��GC�P�z���>8�*A�W�/T\Z&mcQUtPWcrF�\�Jd#\�D�\�\Z\"\��\npv�\�7��q�=s䪗\�\�e(��է9�4R�>\��e�\�\�_�W\�`�\�\0uvs՚V�\Z6\n�\�=O\�H�CI\�<Wz\�zķ��E9Ɖ%c|\�y�x�\�\�/\�\�\�dכQ�V��0*����z`��[-Gѽ`\�\�`t���\�6\�ŧ\�\�iN\�ԋ\���\���t�i�\�Hf�3�\�Agl��KOd\�H}qV\�\�\�`O	E�, \�:\�R)��ba8F\�c,��\�\��ٞ�tƝ<(t\���\�4o�\r��d\�f�g��\�8����+�\�l5\�\�R\�t7\r��k�w*\�[-L\�F�\����\���\�D\n\�\�\�\�\�5\Zptfs5�LA���g;`c\'Y��G:^\\j\�`�\��4t8tƐ7g\�\�\rY\�\�j?\�gS�,��X\�\��\�\�&\�\�3/\�Ԭ���,\�m�Dw\�Y�\�c�\�_�\�V:k;�P{�@C.��.p\�Wհ�\�\�k��\�h8��yv�7��\�i\�V�_/��_\rҿ *�R��0N{U\�a\�j�2˥Iޤ.7\�;\�7�h�\�8\Z��C\�mo\�\�=h\�\�\�\�KC\�\�]Xb2\�W�j�\��\�\�\�\�[̞쾼\�l�Ύ\�3�}\��\�N�ծ\�\�u\�zX�\�\�\�?\�.\�ޟM�/\�C�P�\�m\�sծ�L\�a\�\�\�w��\�\�:=�d��\�\��\�V. �ף�\�e\�\�\�?@kZ$N�\�]\�&\�v�ƽ�k��\�\�\�\r�kP^{�\�2\�s\�`5\�;�Uw_\�O�څ}ǵ\�ۂ?�v\r�믲~���5w_�O\�%��\�io{\�\Z\�\�ݡ�跾w_��fka?\�\�r\�\n�d[\�\'�����\�\�/�x�d\�v�Ķ��^v!\�\�m\�l\�_�\�.\�c���ۀ\�E\�\�pWJ�qv`�����x��C\�$db|1)=\�\�ԙ\�8\�ns�����z\�\��\�\�\�D\�I6Uqݙɋ׍,\����x��Å\�i��{��)�f%\�\�\�w]L�)ذ�\�N_\\�\\\��<�+\��l\r�Y\�\�?n\�y�\�\ruW\�&�l�\�\�\"�2�M�\�c�\�\�P{;\�f7\��.\r\�\��jڵ8\�\�8�4�0\�W��8e��*��\�*\�@\�ns\�\\\�|[\\�\�ޜ\�n�@��\Z�.\Z���Vś�k��P���\�t\�M\�^�\����>[>}�u\�S�u�`z_v\�.7٬�V�\�BO&ӧ݈|_{X\�_��_ˬ\�\�B�ho�\�cA\�Kfrj��,у+\�\�z�x7+����\r�y�Thp�3�¤�\�\�\�wΰ\'\\\�먰�W� \�����\�\�E\�\�|nc1\�\�5\�vV�\�\�-\�\�I���m�xjO�.\��}\��?I%=','PIPELINE'),(3,'5fda2f5076f6375c2f0e7bd89296103ade204651',_binary 'x��S�n\�0��\�\�a���\�v+��������-�*K�Dws���H[q��\�mG�|O\�\�\�\0��J	��|U\��ƺ#\�\�\�*�r*���\�\�U�\"�FՔ `L&j��\�!\'q@�N�(4mg\�\0��}�\�(6\�e\�\��_)\�\�\�^��\ZZ\rE�\�=�bjhU\�=&\�9TDG�묕h\�g\�)\����\r4�\"*݃\�(tc�[h�A���6\��\�yC.�g��4%�	h�CHY00\"NQa�A��p^\�\�\�V_W7JW\�\�㬙W��\�̮�YYU�L5A3;\�\�ÿO\�\' ��\�\�Eq\�-�\\H\�&\�M\�.\�t\��\�qy\�@��<!��q:˂�kGB\�Yp\����o\�\�\��ERZ�\�\nO\�Ge�\�\�\�Pv\�M�G�%\�!�v\�zI1�Ŋa��Iӹ��\�\�c��Y\�\�\�\'�;I-p�,(ھ)�\�kR~MW��\�M�5ʦ���3\�\��\�;�\��<%��y�b\�F\�V9m߸��d��\�W���n��|	��\�9{\�7X\�\�\�<~~\�6�g��\��\�\��\0\�C��','EXECUTION_PLAN');
/*!40000 ALTER TABLE `snapshots` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-16 16:36:08
