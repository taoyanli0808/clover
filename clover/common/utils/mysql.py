#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
from config import DB_CONFIG


class Mysql(object):

    def __init__(self):
        host = DB_CONFIG.get('HOST') if DB_CONFIG.get('HOST') else '127.0.0.1'
        port = DB_CONFIG.get('PORT') if DB_CONFIG.get('PORT') else '3306'
        user = DB_CONFIG.get('USERNAME') if DB_CONFIG.get('USERNAME') else 'root'
        password = DB_CONFIG.get('PASSWORD') if DB_CONFIG.get('PASSWORD') else 'admin123456'
        database = DB_CONFIG.get('DBNAME') if DB_CONFIG.get('DBNAME') else 'clover'
        charset = DB_CONFIG.get('CHARSET') if DB_CONFIG.get('CHARSET') else 'utf-8'
        try:
            self.conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                # charset=charset,
                cursorclass=pymysql.cursors.DictCursor,  # 以字典的形式返回操作结果
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)

    def __del__(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(e)

    def _item(self, sql):
        """
        执行SQL通用方式: insert update delete
        :return:
        """
        print('_item: {0}'.format(sql))
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        self.conn.commit()
        count = self.cursor.rowcount
        self.cursor.close()
        return count

    @classmethod
    def _where(cls, data, sql):
        """
        {
            'terms': {
                'great': {
                    '2': 1  # where 2>1 --> where col>num
                },
                'less': {
                    '2': 1  # where 2<1 --> where col2<num2
                },
                'key': value  # where key=value
            },
            'logic': 'and'  # and 或者 or  == where col<num and col2>num2
        }
        :return:
        """
        # 如果限制查询条件则填充sql语句
        terms = []
        if 'terms' not in data or not data['terms']:
            return None
        terms = []  # where表达式拼接列表
        for key, val in data['terms'].items():
            # 判断大于号
            if key == 'great':
                for col, value in data['terms']['great'].items():
                    terms.append(" {0}>'{1}' ".format(col, value))
                continue  # 取出'>'号表达式后继续遍历
            # 判断小于号
            if key == 'less':
                for col, value in data['terms']['less'].items():
                    terms.append(" {0}<'{1}' ".format(col, value))
                continue  # 取出'<'号表达式后继续遍历
            # 取出'='号表达式
            terms.append(" {0}='{1}' ".format(key, val))
        # 多个查询条件时会存在logic属性，此时用logic拼接，logic是and或or
        if 'logic' in data and data['logic']:
            logic = data['logic']
        else:
            logic = ""
        condition = logic.join(terms)
        sql += " where {0}".format(condition.strip())
        return sql

    def insert(self, **kwargs):
        """
        {
            'database': str,
            'table': str,
            'data': {
                'key': 'value',
            },
        }
        :param kwargs:
        :return:
        """
        # 如果指定数据库则选中数据库
        if 'database' in kwargs and kwargs['database']:
            self.conn.select_db(kwargs.pop('database'))

        # 插入数据必须指定插入到那个表中，否则返回空
        if 'table' not in kwargs or not kwargs['table']:
            return None
        table = kwargs.pop('table')

        # 如果没有要插入的数据或要插入的数据不是字典类型，则返回空
        if 'data' not in kwargs and not kwargs['data'] and not isinstance(kwargs['data'], dict):
            return None

        # 获取要插入的数据库的表字段
        fields = ",".join(kwargs['data'].keys())
        # 获取要插入的数据库的字段值，并转为str TODO 尝试使用原始值插入
        values = [str(value) for value in kwargs['data'].values()]
        values = "'" + "', '".join(values) + "'"
        sql = "insert into {0} ({1}) values ({2});".format(table, fields, values)

        count = self._item(sql)
        # cursor = self.conn.cursor()
        # try:
        #     cursor.execute(sql)
        # except pymysql.err.IntegrityError as error:
        #     print(error)
        # self.conn.commit()
        # count = cursor.rowcount
        # cursor.close()
        return count

    def delete(self, **kwargs):
        """
        {
            'database': str,
            'table': str,
            'where': {
                'terms': {
                    'key': value,  # where key=value
                },
                'logic': str,  # and or 连接terms项
            }
        }
        :param kwargs:
        :return:
        """
        # 如果指定数据库则选中数据库
        if 'database' in kwargs and kwargs['database']:
            self.conn.select_db(kwargs['database'])

        if 'table' not in kwargs or not kwargs['table']:
            return None
        table = kwargs.pop('table')
        sql = "delete from {0}".format(table)

        # 如果限制查询条件则填充sql语句
        if 'where' in kwargs and kwargs['where']:
            sql = self._where(kwargs['where'], sql)
            # terms = []
            # if 'terms' not in kwargs['where'] or not kwargs['where']['logic']:
            #     return None
            # for key, val in kwargs['where']['terms'].items():
            #     terms.append(" {0}='{1}' ".format(key, val))
            # # 多个查询条件时会存在logic属性，此时用logic拼接，logic是and或or
            # if 'logic' in kwargs['where'] and kwargs['where']['logic']:
            #     logic = kwargs['where']['logic']
            # else:
            #     logic = ""
            # condition = logic.join(terms)
            # sql += " where {0}".format(condition.strip())

        # cursor = self.conn.cursor()
        # cursor.execute(sql)
        # self.conn.commit()
        # count = cursor.rowcount
        # cursor.close()
        return self._item(sql)

    def update(self, **kwargs):
        """
        {
            'database': str,
            'table': str,
            'set': {
                'terms': {
                    'key': value,  # 可以多个set值 key=value
                }
            },
            'where': {
                'terms': {
                    'key': value,
                },
                'logic': str,  # and  or
            }
        }
        :param kwargs:
        :return:
        """
        # 如果指定数据库则选中数据库
        if 'database' in kwargs and kwargs['database']:
            self.conn.select_db(kwargs['database'])

        if 'table' not in kwargs:
            raise Exception("need table！")

        sql = "update {table}".format(**kwargs)

        # 设置更新的内容
        if 'set' in kwargs and kwargs['set']:
            terms = []
            for key, val in kwargs['set']['terms'].items():
                terms.append(" {0}='{1}' ".format(key, val))
            # 修改多项时用,连接多个值
            content = ",".join(terms)
            sql += " set {0}".format(content.strip())

        # 如果限制查询条件则填充sql语句
        if 'where' in kwargs and kwargs['where']:
            sql = self._where(kwargs['where'], sql)
            # terms = []
            # for key, val in kwargs['where']['terms'].items():
            #     terms.append(" {0}='{1}' ".format(key, val))
            # # 多个查询条件时会存在logic属性，此时用logic拼接，logic是and或or
            # if 'logic' in kwargs['where'] and kwargs['where']['logic']:
            #     logic = kwargs['where']['logic']
            # else:
            #     logic = ""
            # condition = logic.join(terms)
            # sql += " where {0}".format(condition.strip())

        # cursor = self.conn.cursor()
        # cursor.execute(sql)
        # self.conn.commit()
        # count = cursor.rowcount
        # cursor.close()
        return self._item(sql)

    def search(self, **kwargs):
        """
        {
            'database': str,
            'table': str,
            'fields': {
                'as': {
                    'key': 'value'  # id as _id
                }
                'col': []
            },
            'where': {
                'terms': {
                    'great': {
                        '2': 1  # where 2>1 --> where col>num
                    },
                    'less': {
                        '2': 1  # where 2<1 --> where col2<num2
                    },
                    'key': value  # where key=value
                },
                'logic': 'and'  # and 或者 or  == where col<num and col2>num2
            },
            'page': num,
            'size': num,
            'order': 'col',
            'reverse': 'DESC',
        }
        :param kwargs:
        :return:
        """
        # 如果指定数据库则选中数据库
        if 'database' in kwargs and kwargs['database']:
            self.conn.select_db(kwargs['database'])

        if 'table' not in kwargs or kwargs['table'] is None:
            raise Exception("need table！")
        sql = ''
        # 要查询显示的字段
        if 'fields' in kwargs and kwargs['fields'] and isinstance(kwargs['fields'], str):
            sql = "select {fields} from {table}".format(**kwargs)
        elif 'fields' in kwargs and kwargs['fields'] and isinstance(kwargs['fields'], dict):
            if 'as' in kwargs['fields'] and kwargs['fields']['as']:
                terms = []
                for key, val in kwargs['fields']['as'].items():
                    terms.append(" {0} as '{1}' ".format(key, val))
                condition = ','.join(terms)
                sql = "select {0} from {1}".format(condition.strip(), kwargs['table'])
            else:
                raise Exception("need as！")
        else:
            sql = "select * from {table}".format(**kwargs)

        # 如果限制查询条件则填充sql语句
        if 'where' in kwargs and kwargs['where']:
            sql = self._where(kwargs['where'], sql)

        # # 如果携带翻页参数则对其赋值，否则页码为0
        # try:
        #     page = int(kwargs.get('page', 0))
        # except TypeError:
        #     page = 0
        #
        # # 如果限制页码大小则对其赋值，否则限制为20
        # try:
        #     size = int(kwargs.get('size', 20))
        # except TypeError:
        #     size = 20

        # order by 子句判断
        if 'order' in kwargs:
            order = kwargs.get('order', 'id')
            reverse = kwargs.get('reverse', 'asc')  # DESC
            sql += " order by {0} {1}".format(order, reverse)

        # 拼接limit限制条件, 默认为10条
        if 'limit' in kwargs and kwargs['limit']:
            sql += " limit {0}".format(kwargs.get('limit', 10))
        print(sql)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.conn.commit()
        self.cursor.close()
        return results

    def filter(self, **kwargs):
        # TODO count() avg() 'grope by' 'join in'  and so on...
        pass

    """
    以下提供原始SQL方法，需要在业务层直接写SQL语句
    """
    def fetchone(self, sql, params=None):
        """
        根据sql和参数获取一行数据
        :param sql: sql语句
        :param params: sql语句对象的参数元组，默认值为None
        :return: 查询的一行数据, rtype = tuple
        """
        data_one = None
        try:
            count = self.cursor.execute(sql, params)
            if count != 0:
                data_one = self.cursor.fetchone()
        except Exception as e:
            print(e)
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
            count = self.cursor.execute(sql, params)
            if count != 0:
                data_all = self.cursor.fetchall()
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
            count = self.cursor.execute(sql, params)
            self.conn.commit()
        except Exception as e:
            print(e)
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


if __name__ == '__main__':
    data_search = {
        'database': 'clover',
        'table': 'team',
    }
    mysql = Mysql()
    # row = mysql.insert(**data_insert)
    row = mysql.search(**data_search)
    # row = mysql.delete(**data_delete)
    # row = mysql.update(**data_update)
    print(row)
