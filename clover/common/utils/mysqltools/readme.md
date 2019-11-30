# Mac安装MySQL数据库
1. 使用homebrew包管理器安装mysql最新版本  
`brew install mysql`
2. 初始化配置MySQL  
`mysql.server start`
`mysql_secure_installation`
3. 创建数据库  
    ```mysql
    CREATE DATABASE test;
    CREATE DATABASE IF NOT EXISTS my_db default charset utf8 COLLATE utf8_general_ci;
    ```
4. 创建表  
    ```mysql
    CREATE TABLE `test` (
      `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
      `case_id` int(11) DEFAULT NULL,
      `username` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
      `password` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
      `start_time` datetime DEFAULT NULL,
      `end_time` datetime DEFAULT NULL COMMENT '结束时间or最后更新时间',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ```
5. 可视化工具连接数据库  
    - Navicat for MySQL
    - sqlyog
