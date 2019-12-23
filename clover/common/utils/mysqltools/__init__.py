#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql

from config import DB_CONFIG
from clover.common.utils import get_timestamp, get_friendly_id


class MysqlHelper(object):
    """
    mysqltools --> username:root password:admin123456
    """
    def __init__(self) -> None:
        # init datebase from config.py
        host = DB_CONFIG.get('HOST') if DB_CONFIG.get('HOST') else '127.0.0.1'
        port = DB_CONFIG.get('PORT') if DB_CONFIG.get('PORT') else '3306'
        user = DB_CONFIG.get('USERNAME') if DB_CONFIG.get('USERNAME') else 'root'
        pwd = DB_CONFIG.get('PASSWORD') if DB_CONFIG.get('PASSWORD') else 'admin123456'
        dbname = DB_CONFIG.get('DBNAME') if DB_CONFIG.get('DBNAME') else 'clover'
        # connect datebase
        try:
            self.conn = pymysql.Connect(
                host=host,
                port=port,
                user=user,
                password=pwd,
                db=dbname,
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

    def update_sql(self, sql, params=None):
        """
        执行修改
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 受影响的行数
        """
        return self.__item(sql, params)

    def insert_sql(self, sql, params=None):
        """
        执行新增
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 受影响的行数
        """
        return self.__item(sql, params)

    def delete_sql(self, sql, params=None):
        """
        执行删除
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 受影响的行数
        """
        return self.__item(sql, params)

    def insert(self, data):
        """
        d = {
            'table': 'environment',
            'uuid': get_friendly_id(),
            'team': 't',
            'project': 'p',
            'owner': 'o',
        }
        :param data:
        :return: int 0 or 1
        """
        print(data)
        if 'table' not in data or not data['table']:
            return None
        table = data.pop('table')
        data.setdefault('id', 0)  # 自增id
        data.setdefault('enable', 1)  # 数据默认为可用状态
        data.setdefault('created_time', str(get_timestamp()))
        data.setdefault('updated_time', str(get_timestamp()))
        fields_str = fields = ''  # 字段的集合
        list_values = []  # values字段对应值的集合
        for key in data:
            fields_str = fields_str + "%s," % key
            list_values.append(data.get(key))
        fields = "(" + fields_str[0:len(fields_str)-1] + ")"  # 添加括号最终的字段集合
        values = tuple(list_values)  # 最终的字段值集合
        sql = 'insert into %s%s values %s' % (table, fields, values)
        print(sql)
        return self.__item(sql)

    def update(self, data, filter):
        """
        d = {
            'table': 'environment',
            'team': 't',
            'project': 'p',
            'owner': 'o',
        }
        :param filter:
        :param data:
        :return:
        """
        table = data.pop('table')
        terms = []
        for k, v in data.items():
            terms.append("{0}='{1}'".format(k, v))
        content = ",".join(terms).strip()
        terms2 = []
        for k, v in filter.items():
            terms2.append("{0}='{1}'".format(k, v))
        filter = ",".join(terms2).strip()
        # 暂不支持复杂where 例如and、or等
        sql = 'update {0} set {1} where {2}'.format(table, content, filter)
        return self.__item(sql)

    def delete(self):
        pass

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
    # sqls = 'select * from test'
    # # paramss = [2]  # 对应语句中 =号 右侧的 %s 按顺序匹配
    # print(type(db.fetchall(sqls)))
    # sql_name = 'update test set password=%s where case_id=%s'
    # paramss = ['abcdefg', 3]
    # print(db.update(sql_name, paramss))
    # sql_in = 'insert into %s (%s) values (%s)'
    # values = '3,23424,t,p,o,e,c,u'
    # params_in = ['environment', 'id,uuid,team,project,owner,enable,created_time,updated_time', values]
    # print(db.insert_sql(sql_in, params_in))
    d = {
        'table': 'environment',
        'team': 'tttt80000088',
        'project': 'pp565555pp',
        'owner': 'o8888',
    }
    print(d)
    res = db.update(d, {'uuid': '20191222162413_307cad0e'})
    print(res)

