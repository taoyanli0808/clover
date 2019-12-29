# Mac安装MySQL数据库
1. 使用homebrew包管理器安装mysql最新版本  
`brew install mysql`
2. 初始化配置MySQL  
    ```shell script
    mysql.server start
    mysql_secure_installation
    ```
3. 创建数据库  
    ```mysql
    CREATE DATABASE clover;
    CREATE DATABASE IF NOT EXISTS my_db default charset utf8 COLLATE utf8_general_ci;
    ```
4. 创建表team表  
    ```mysql
    SET NAMES utf8mb4;
    SET FOREIGN_KEY_CHECKS = 0;
    DROP TABLE IF EXISTS `team`;
    CREATE TABLE `team` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
      `team` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
      `project` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
      `owner` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
      `enable` tinyint(4) DEFAULT '1' NULL COMMENT '0:已软删除; 1:正常可用状态',
      `created` datetime DEFAULT NULL,
      `updated` datetime DEFAULT NULL,
      PRIMARY KEY (`id`,`_id`) USING BTREE
    ) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    
    SET FOREIGN_KEY_CHECKS = 1;
    ```

5. 创建variable表  
    ```mysql
    SET NAMES utf8mb4;
    SET FOREIGN_KEY_CHECKS = 0;
    DROP TABLE IF EXISTS `variable`;
    CREATE TABLE `variable` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
      `name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
      `value` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
      `enable` tinyint(4) DEFAULT '1' COMMENT '0:已软删除; 1:正常可用状态',
      `created` datetime DEFAULT NULL,
      `updated` datetime DEFAULT NULL,
      `team` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
      `project` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
      `owner` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
      PRIMARY KEY (`id`,`_id`) USING BTREE
    ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    
    SET FOREIGN_KEY_CHECKS = 1;
    ```

6. 创建interface表  
    ```mysql

    ```

# 可视化工具连接数据库  
    - Navicat for MySQL
    - sqlyog

# NOTES  
    - 使用前请确认并修改config.py配置文件中的database配置