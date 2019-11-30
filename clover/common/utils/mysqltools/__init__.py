#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql

from config import DB_CONFIG


class MysqlHelper(object):
    """
    mysqltools --> username:root password:admin123456
    """
    def __init__(self, host=None, port=None, user=None, pwd=None, dbname=None, charset=None) -> None:
        # init datebase from config.py
        host = DB_CONFIG.get('HOST') if host is None else host
        port = DB_CONFIG.get('PORT') if port is None else port
        user = DB_CONFIG.get('USERNAME') if user is None else user
        pwd = DB_CONFIG.get('PASSWORD') if pwd is None else pwd
        dbname = DB_CONFIG.get('DBNAME') if dbname is None else dbname
        charset = DB_CONFIG.get('CHARSET') if charset is None else charset
        # connect datebase
        try:
            self.conn = pymysql.Connect(
                host=host,
                port=port,
                user=user,
                password=pwd,
                db=dbname,
                charset=charset
            )
            # get cursor
            self.cur = self.conn.cursor()
            print('connect success')
        except Exception as e:
            print(e)
        super().__init__()

    def __del__(self):
        try:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(e)

    def fetchone(self, sql, params=None):
        """
        根据sql和参数获取一行数据
        :param sql: sql语句
        :param params: sql语句对象的参数元组，默认值为None
        :return: 查询的一行数据, rtype = tuple
        """
        data_one = None
        try:
            count = self.cur.execute(sql, params)
            if count != 0:
                data_one = self.cur.fetchone()
        except Exception as e:
            print(e)
        # finally:
        #     self.close()
        return data_one

    def fetchall(self, sql, params=None):
        """
        根据sql和参数获取所有数据
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 查询的所有数据， rtype = tuple
        """
        data_all = None
        try:
            count = self.cur.execute(sql, params)
            if count != 0:
                data_all = self.cur.fetchall()
        except Exception as e:
            print(e)
        # finally:
        #     self.close()
        return data_all

    def __item(self, sql, params=None):
        """
        执行增删改
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 受影响的行数
        """
        count = 0
        try:
            count = self.cur.execute(sql, params)
            self.conn.commit()
        except Exception as e:
            print(e)
        # finally:
        #     self.close()
        return count

    def update(self, sql, params=None):
        """
        执行修改
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 受影响的行数
        """
        return self.__item(sql, params)

    def insert(self, sql, params=None):
        """
        执行新增
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 受影响的行数
        """
        return self.__item(sql, params)

    def delete(self, sql, params=None):
        """
        执行删除
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 受影响的行数
        """
        return self.__item(sql, params)

    def close(self):
        """
        关闭执行工具和连接对象
        """
        try:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    db = MysqlHelper()
    # 测试查询，并返回一条数据
    sqls = 'select * from test'
    # paramss = [2]  # 对应语句中 =号 右侧的 %s 按顺序匹配
    print(type(db.fetchall(sqls)))
    sql_name = 'update test set password=%s where case_id=%s'
    paramss = ['abcdefg', 3]
    print(db.update(sql_name, paramss))


"""
CREATE TABLE `test` (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `case_id` int(11) DEFAULT NULL,
  `username` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL COMMENT '结束时间or最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
"""