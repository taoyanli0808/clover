import re
import json
import datetime

from clover.exts import db
from clover.models import query_to_dict, soft_delete
from clover.environment.models import TeamModel
from clover.environment.models import KeywordModel
from clover.environment.models import VariableModel


class TeamService(object):

    def create(self, data):
        """
        :param data:
        :return:
        """
        model = TeamModel(**data)
        db.session.add(model)
        db.session.commit()

    def detele(self, data):
        """
        :param data:
        :return:
        """
        model = TeamModel.query.get(data['id'])
        if model is not None:
            soft_delete(model)

    def update(self, data):
        """
        # 使用id作为条件，更新数据库重的数据记录。
        # 通过id查不到数据时增作为一条新的记录存入。
        :param data:
        :return:
        """
        old_model = TeamModel.query.get(data['id'])
        if old_model is None:
            model = TeamModel(**data)
            db.session.add(model)
            db.session.commit()
        else:
            old_model.team = data['team']
            old_model.project = data['project']
            old_model.owner = data['owner']
            old_model.updated = datetime.datetime.now()
            db.session.commit()

    def search(self, data):
        """
        type=team&team=team1
        limit=10&skip=0&type=team
        NOTE: 有两种传参查询方式，需要多data做相应处理
        :param data:
        :return:
        """
        filter = {'enable': 0}

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

        results = TeamModel.query.filter_by(**filter)\
                .offset(offset).limit(limit)
        results = query_to_dict(results)
        count = TeamModel.query.filter_by(**filter).count()
        return count, results

    def aggregate(self, data):
        """
        {'type': 'team', 'key': 'team'}
        {'type': 'team', 'key': 'owner'}
        # cascader: 按照element ui库cascader需要的数据格式返回数据。
        #           团队和项目配置数据不会特别多，因此无需过多关注性能。
        :param data:
        :return: 所有数据
        """
        if 'cascader' in data:
            cascader = {}
            results = TeamModel.query.\
                with_entities(TeamModel.team, TeamModel.project).\
                filter(TeamModel.enable == 0).\
                distinct().all()
            for team, project in results:
                if team not in cascader:
                    cascader.setdefault(team, {
                        'label': team,
                        'value': team,
                        'children': [{
                            'label': project,
                            'value': project
                        }],
                    })
                else:
                    labels = [item['label'] for item in cascader[team]['children']]
                    if project not in labels:
                        cascader[team]['children'].append({
                            'label': project,
                            'value': project
                        })
            return list(cascader.values())
        else:
            if data['key'] == 'team':
                results = TeamModel.query.with_entities(TeamModel.team).\
                    filter(TeamModel.enable == 0).\
                    distinct().all()
                return [r[0] for r in results]
            elif data['key'] == 'owner':
                results = TeamModel.query.with_entities(TeamModel.owner).\
                    filter(TeamModel.enable == 0).\
                    distinct().all()
                return [r[0] for r in results]
            else:
                return []


class VariableService(object):

    def create(self, data):
        """
        :param data:
        :return:
        """
        model = VariableModel(**data)
        db.session.add(model)
        db.session.commit()

    def detele(self, data):
        """
        :param data:
        :return:
        """
        model = VariableModel.query.get(data['id'])
        if model is not None:
            soft_delete(model)

    def update(self, data):
        """
        # 使用id作为条件，更新数据库重的数据记录。
        # 通过id查不到数据时增作为一条新的记录存入。
        :param data:
        :return:
        """
        old_model = VariableModel.query.get(data['id'])
        if old_model is None:
            model = VariableModel(**data)
            db.session.add(model)
            db.session.commit()
        else:
            old_model.team = data['team']
            old_model.project = data['project']
            old_model.owner = data['owner']
            old_model.name = data['name']
            old_model.value = data['value']
            old_model.updated = datetime.datetime.now()
            db.session.commit()

    def search(self, data):
        """
        type=team&team=team1
        limit=10&skip=0&type=team
        NOTE: 有两种传参查询方式，需要多data做相应处理
        :param data:
        :return:
        """
        filter = {'enable': 0}

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

        results = VariableModel.query.filter_by(**filter) \
                .offset(offset).limit(limit)
        results = query_to_dict(results)
        count = VariableModel.query.filter_by(**filter).count()
        return count, results


class KeywordService(object):

    def create(self, data):
        """
        # 暂时没有前端页面 -- SQL暂时不更换
        # 这里需要先提取函数名，然后关键字用函数名进行索引，存到数据库。
        # 如果数据库中函数名已经存在怎么办，是否需要先查询，重复则失败？
        :param data:
        :return:
        """
        team = data.get('team')
        project = data.get('project')
        mock = json.loads(data.get('mock'))
        keyword = data.get('keyword')
        func = re.findall(r'def\s+(.+?)\(', keyword)
        name = func[0] if func else ""
        data = {
            'team': team,
            'project': project,
            'name': name,
            'mock': mock,
            'snippet': keyword,
        }
        model = KeywordModel(**data)
        db.session.add(model)
        db.session.commit()
        return model.id

    def delete(self, data):
        """
        :param data:
        :return:
        """
        model = KeywordModel.query.get(data['id'])
        if model is not None:
            soft_delete(model)

    def update(self, data):
        """
        :param data:
        :return:
        """
        old_model = KeywordModel.query.get(data['id'])
        if old_model is None:
            model = TeamModel(**data)
            db.session.add(model)
            db.session.commit()
        else:
            old_model.team = data['team']
            old_model.project = data['project']
            old_model.owner = data['owner']
            old_model.name = data['name']
            old_model.keyword = data['keyword']
            old_model.mock = data['mock']
            old_model.updated = datetime.datetime.now()
            db.session.commit()

    def search(self, data):
        """
        :param data:
        :return:
        """
        filter = {'enable': 0}

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

        results = KeywordModel.query.filter_by(**filter) \
                .offset(offset).limit(limit)
        results = query_to_dict(results)
        count = KeywordModel.query.filter_by(**filter).count()
        return count, results

    def debug(self, data):
        """
        # 自定义关键字中提取函数名和参数，在后面拼接出调用请求，
        # 最后交给exec函数执行，如果提取函数名和参数失败则不处理。
        :param data:
        :return:
        """
        # 这里是否需要try except兜一下？
        mock = json.loads(data.get('mock'))
        keyword = data.get('keyword')
        func = re.findall(r'def\s+(.+?):', keyword)
        if func:
            keyword += '\n' + func[0]
            exec(keyword, {'data': mock})
        return mock
