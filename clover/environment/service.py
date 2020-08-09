
import datetime

from clover.exts import db
from clover.models import query_to_dict, soft_delete
from clover.environment.models import TeamModel
from clover.environment.models import VariableModel
from clover.core.exception import catch_database_exception


class TeamService(object):

    @catch_database_exception
    def create(self, data):
        """
        :param data:
        :return:
        """
        status=0
        filter = {
            "enable": 0,
            "team": data["team"],
            "project": data["project"]
        }
        count = TeamModel.query.filter_by(**filter).count()
        if count == 0:
            model = TeamModel(**data)
            db.session.add(model)
            db.session.commit()
            return status
        status = 1
        return status

    @catch_database_exception
    def detele(self, data):
        """
        :param data:
        :return:
        """
        model = TeamModel.query.get(data['id'])
        if model is not None:
            soft_delete(model)
        return model.id

    @catch_database_exception
    def update(self, data):
        """
        # 判断传的团队名和项目名是否存在，不存在则更新
        #存在直接返回
        :param data:
        :return:
        """
        status = 0
        filter = {"team": data["team"], "project": data["project"], "enable": 0}
        result = TeamModel.query.filter_by(**filter).first()  # 查询前端传来的参数在数据库里的数据
        print(result)
        count = TeamModel.query.filter_by(**filter).count()  # 查询查询到的总数
        old_model = TeamModel.query.get(data['id'])
        if count >= 1 and result.id != data['id']:  # 数据已在库中并且不是本次修改的本条数据
            status = 1
            return status
        else:
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
                return status

    @catch_database_exception
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

        results = TeamModel.query.filter_by(
            **filter
        ).order_by(
            TeamModel.created.desc()
        ).offset(offset).limit(limit)
        results = query_to_dict(results)
        count = TeamModel.query.filter_by(**filter).count()
        return count, results

    @catch_database_exception
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
            results = TeamModel.query. \
                with_entities(TeamModel.team, TeamModel.project). \
                filter(TeamModel.enable == 0). \
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
                results = TeamModel.query.with_entities(TeamModel.team). \
                    filter(TeamModel.enable == 0). \
                    distinct().all()
                return [r[0] for r in results]
            elif data['key'] == 'owner':
                results = TeamModel.query.with_entities(TeamModel.owner). \
                    filter(TeamModel.enable == 0). \
                    distinct().all()
                return [r[0] for r in results]
            else:
                return []

    @catch_database_exception
    def navigation(self, data):
        """
        {
            $team: [$project...],
            $team: [$project...]
        }
        :param data:
        :return: 所有数据
        """
        results = TeamModel.query.filter(TeamModel.enable == 0)

        options = {}
        for result in results:
            if result.team not in options:
                options.setdefault(result.team, [result.project])
            else:
                options[result.team].append(result.project)

        return options


class VariableService(object):

    @catch_database_exception
    def create(self, data):
        """
        :param data:
        :return:
        """
        # 查询数据库name值，存在已有变量就返回变量名存在
        filter = {
            "enable": 0,
            "name": data["name"],
            "project": data["project"]
        }
        count = VariableModel.query.filter_by(**filter).count()
        if not count:
            model = VariableModel(**data)
            db.session.add(model)
            db.session.commit()
        return count

    @catch_database_exception
    def detele(self, data):
        """
        :param data:
        :return:
        """
        model = VariableModel.query.get(data['id'])
        if model is not None:
            soft_delete(model)

    @catch_database_exception
    def update(self, data):
        """
        # 使用id作为条件，更新数据库重的数据记录。
        # 通过id查不到数据时增作为一条新的记录存入。
        :param data:
        :return:
        """
        status = 0
        filter = {"name": data["name"], "project": data["project"], "enable": 0}
        result = VariableModel.query.filter_by(**filter).first() #查询前端传来的参数在数据库里的数据
        count = VariableModel.query.filter_by(**filter).count() #查询查询到的总数
        old_model = VariableModel.query.get(data['id'])
        if count >= 1 and result.id != data['id']: #数据已在库中并且不是本次修改的本条数据
            status = 1
            return status
        else:
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
                return status

    @catch_database_exception
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

        results = VariableModel.query.filter_by(
            **filter
        ).order_by(
            VariableModel.created.desc()
        ).offset(offset).limit(limit)
        results = query_to_dict(results)
        count = VariableModel.query.filter_by(**filter).count()
        return count, results
