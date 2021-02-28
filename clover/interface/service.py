#coding=utf-8

import datetime

from clover.exts import db
from clover.core.context import Context
from clover.core.producer import Producer
from clover.core.executor import Executor

from clover.models import soft_delete
from clover.models import query_to_dict
from clover.interface.models import InterfaceModel


class InterfaceService(object):

    def create(self, data):
        """
        # 将页面数据保存到数据库。
        :param data:
        :return:
        """
        model = InterfaceModel(**data)
        db.session.add(model)
        db.session.commit()

        context = Context()
        context.build_context({
            'type': 'interface',
            'id': model.id,
            'user': data
        })
        executor = Executor('debug')
        status, message, data = executor.execute(context)

        return model.id, status, message, data

    def delete(self, data):
        """
        :param data:
        :return:
        """
        id_list = data.pop('id_list')
        for id in id_list:
            result = InterfaceModel.query.get(id)
            soft_delete(result)

    def update(self, data):
        """
        # 使用id作为条件，更新数据库重的数据记录。
        # 通过id查不到数据时增作为一条新的记录存入。
        :param data:
        :return:
        """
        old_model = InterfaceModel.query.get(data['id'])
        if old_model is None:
            model = InterfaceModel(**data)
            db.session.add(model)
            db.session.commit()
            old_model = model
        else:
            {setattr(old_model, k, v) for k, v in data.items()}
            old_model.updated = datetime.datetime.now()
            db.session.commit()

        context = Context()
        context.build_context({
            'type': 'interface',
            'id': data['id'],
            'user': data
        })
        executor = Executor('debug')
        status, message, data = executor.execute(context)

        return old_model.id, status, message, data

    def search(self, data):
        """
        :param data:
        :return:
        """
        filter = {'enable': 0}

        # 如果按照id查询则返回唯一的数据或None
        if 'id' in data and data['id']:
            filter.setdefault('id', data.get('id'))
            result = InterfaceModel.query.get(data['id'])
            count = 1 if result else 0
            result = result.to_dict() if result else None
            return count, result

        if 'team' in data and data['team']:
            filter.setdefault('team', data.get('team'))

        if 'project' in data and data['project']:
            filter.setdefault('project', data.get('project'))

        try:
            offset = int(data.get('offset', 0))
        except TypeError:
            offset = 0

        try:
            limit = int(data.get('limit', 10))
        except TypeError:
            limit = 10

        if 'caseName' in data and data['caseName']:
            results = InterfaceModel.query.filter_by(
                **filter
            ).filter(
                InterfaceModel.name.like('%' + data['caseName'] + '%')
            ).order_by(
                InterfaceModel.created.desc()
            ).offset(offset).limit(limit)
        else:
            results = InterfaceModel.query.filter_by(
                **filter
            ).order_by(
                InterfaceModel.created.desc()
            ).offset(offset).limit(limit)

        results = query_to_dict(results)

        for result in results:
            if result['status'] == None:
                result['status'] = True

        if 'caseName' in data and data['caseName']:
            count = InterfaceModel.query.filter_by(**filter).filter(
                InterfaceModel.name.like('%' + data['caseName'] + '%')
            ).count()
        else:
            count = InterfaceModel.query.filter_by(**filter).count()

        return count, results

    def trigger(self, data):
        """
        :param data:
        :return:
        """
        producer = Producer()
        producer.send({
            'type': 'interface',
            'sub_type': 'interface',
            'id': data.get('id'),
            'name': data.get('name'),
            'user': data,
        })
        return

    def switch(self, data):
        """
        :param data:
        :return:
        """
        old_model = InterfaceModel.query.get(data['id_list'])
        {setattr(old_model, k, v) for k, v in data.items()}
        old_model.updated = datetime.datetime.now()
        db.session.commit()
        return

    def tree(self, data):
        """
        # 使用element ui的tree控件展示团队，项目与接口的关系，
        # 数据结构文档详见：https://element.eleme.cn/#/zh-CN/component/tree
        [
            {
                label: ${team name},
                team: ${team name},
                children: [
                    {
                        label: ${project name},
                        project: ${project name},
                        children: [
                            {
                                id: ${case id},
                                label: ${case name}
                            },
                            {
                                id: ${case id},
                                label: ${case name}
                            },
                        ]
                    }
                ]
            }
        ]
        :param data:
        :return: 所有数据
        """
        results = db.session.query(
            InterfaceModel.id,
            InterfaceModel.team,
            InterfaceModel.project,
            InterfaceModel.name
        ).filter(
            InterfaceModel.enable == 0
        )

        # 将数据转化为字典形式
        results = [dict(zip(result.keys(), result)) for result in results]

        # 第一次组合数据，使用字典层级嵌套
        trees = {}
        for result in results:
            if result['team'] not in trees:
                trees.setdefault(result['team'], {})

            if result['project'] not in trees[result['team']]:
                trees[result['team']].setdefault(result['project'], [])

            trees[result['team']][result['project']].append({
                'id': result['id'],
                'name': result['name'],
                'label': result['name'],
            })

        # data为符合element ui的tree控件要求的数据格式
        data = []
        for t, v in trees.items():
            team = {
                'label': t,
                'team': t,
                'children': []
            }
            for p, v in v.items():
                project = {
                    'label': p,
                    'project': p,
                    'children': v
                }
                team['children'].append(project)
            data.append(team)

        return data
