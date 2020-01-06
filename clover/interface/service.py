#coding=utf-8

import time

from clover.common.utils import get_timestamp

from clover.exts import db
from clover.models import query_to_dict
from clover.interface.models import InterfaceModel


class Service(object):

    def create(self, data):
        """
        # 将页面数据保存到数据库。
        :param data:
        :return:
        """
        model = InterfaceModel(**data)
        db.session.add(model)
        db.session.commit()
        return model.id

    def delete(self, data):
        """
        :param data:
        :return:
        """
        id_list = data.pop('id_list')
        for id in id_list:
            result = InterfaceModel.query.get(id)
            db.session.delete(result)
            db.session.commit()

    def search(self, data):
        """
        :param data:
        :return:
        """
        filter = {}

        if 'team' in data and data['team']:
            filter.setdefault('team', data.get('team'))

        if 'owner' in data and data['owner']:
            filter.setdefault('owner', data.get('owner'))

        try:
            offset = int(data.get('offset', 0))
        except TypeError:
            offset = 0

        try:
            limit = int(data.get('limit', 10))
        except TypeError:
            limit = 10

        results = InterfaceModel.query.filter_by(**filter).offset(offset).limit(limit)
        results = query_to_dict(results)
        count = InterfaceModel.query.filter_by(**filter).count()
        return count, results

    def trigger(self, data):
        """
        :param data:
        :return:
        """
        # 需要通过case_id先查询到数据库里的测试用例。
        # run_id是一次运行的记录，查测试报告时使用。
        run_id = 111
        cases = []
        ids = data['cases']
        for id in ids.split(','):
            results = self.db.search('interface', 'case', {'_id': id})
            if not results:
                continue
            cases.append(results[0])

        # 这个data是要存储到数据库的测试报告数据。
        data = {
            'run_id': run_id,
            'time': {
                'start': 0,
                'end': 0,
                'cost': 0,
            },
            'count': {
                'total': 0,
                'run': 0,
                'success': 0,
                'fail': 0,
                'skip': 0
            },
            'result': []
        }
        start = time.time()
        # 判断每一个测试用例是否通过。
        for case in cases:
            case.setdefault('status', 0)
            case.setdefault('message', '测试通过！')
            data['count']['total'] += 1
            data['count']['run'] += 1
            status, message, _ = self.execute(case)
            if status == 0:
                data['count']['success'] += 1
            else:
                data['count']['fail'] += 1
                case['status'] = status
                case['message'] = message
            data['result'].append(case)
        print("{0} {1} {2} {3}".format(data['count']['total'], data['count']['run'], \
                                       data['count']['success'], data['count']['fail']))
        end = time.time()
        # 通过start与end时间戳计算整个测试耗时
        data['time']['start'] = get_timestamp(start)
        data['time']['end'] = get_timestamp(end)
        data['time']['cost'] = "共执行{0:0.3}秒".format(end - start)
        print(data)
        # 将测试报告数据写入数据库。
        self.db.insert('interface', 'report', data)
        print(run_id)
        return run_id
