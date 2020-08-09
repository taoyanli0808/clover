
from clover.models import CloverModel, query_to_dict
from clover.exts import engine


class DashboardService(object):
    """
    使用方法：
        obj.DashboardService()
        data_info = obj.get_info()
    """

    @property
    def _get_subclasses(self):
        """
        :return: 
        """
        all_subclasses = {}
        for subclass in CloverModel.__subclasses__():
            all_subclasses[subclass.__name__] = subclass
        return all_subclasses

    @property
    def _get_summary(self):
        filter = {'enable': 0}
        summary = dict()
        obj = self._get_subclasses
        if 'TeamModel' in obj:
            # a = obj['TeamModel'].query.filter_by(**filter).count(distinct(obj['TeamModel'].project))
            # print(a)
            # b = db.session.query(func.count(distinct(obj['TeamModel'].project))).scalar()
            # print(b)

            # 后续再研究更改为更优雅的写法(SQL直接查询)
            res = query_to_dict(obj['TeamModel'].query.filter_by(**filter).all())
            team = [key['team'] for key in res]
            project = [key['project'] for key in res]
            team_count = len(set(team))
            project_count = len(set(project))
            summary.setdefault('team', team_count)
            summary.setdefault('project', project_count)
        if 'InterfaceModel' in obj:
            interface_count = obj['InterfaceModel'].query.filter_by(**filter).count()
            summary.setdefault('interface', interface_count)
        if 'VariableModel' in obj:
            variable_count = obj['VariableModel'].query.filter_by(**filter).count()
            summary.setdefault('variable', variable_count)
        if 'KeywordModel' in obj:
            keyword_count = obj['KeywordModel'].query.filter_by(**filter).count()
            summary.setdefault('keyword', keyword_count)
        if 'SuiteModel' in obj:
            suite_count = obj['SuiteModel'].query.filter_by(**filter).count()
            summary.setdefault('suite', suite_count)
        return summary

    @property
    def _get_history(self):
        """近半年数据统计, 以创建时间为准 created, 只统计有效enable=0数据"""
        history = dict()
        sql = """
            SELECT
             DATE_FORMAT( created, '%%Y-%%m' ) as date_time, COUNT(*) as nums
            FROM
             {0}
            WHERE
             enable=0 AND DATE_SUB( CURDATE(), INTERVAL 6 MONTH ) <= DATE( created )
            GROUP BY
             date_time;
        """  # 其中 '%Y-%m' 与 python的参数%s冲突, 使用'%%Y-%%m'简单解决先
        interface_res = engine.execute(sql.format('interface')).fetchall()
        suite_res = engine.execute(sql.format('suite')).fetchall()
        for item in interface_res:
            history.setdefault(item[0], {'interface': item[1]})
        for item in suite_res:
            if item[0] in history:
                history.get(item[0]).setdefault('suite', item[1])
            else:
                history.setdefault(item[0], {'suite': item[1]})
        return history

    @property
    def _get_latest(self):
        """
        return: 近一个月的数据，以创建时间为准，无去重
        """
        sql = """
            SELECT
                COUNT(*) 
            FROM
                {0} 
            WHERE
                enable=0 AND DATE_SUB( CURDATE(), INTERVAL 1 MONTH ) <= DATE( created );
        """
        suite_count = engine.execute(sql.format('suite')).scalar()
        interface_count = engine.execute(sql.format('interface')).scalar()
        variable_count = engine.execute(sql.format('variable')).scalar()
        keyword_count = engine.execute(sql.format('keyword')).scalar()
        return dict(suite=suite_count, interface=interface_count, variable=variable_count, keyword=keyword_count)

    def get_info(self):
        """
        所有数据以创建时间为准created, 只统计有效enable=0数据
        """
        return {
            'summary': self._get_summary,
            'history': self._get_history,
            'latest': self._get_latest
        }


if __name__ == '__main__':
    obj = DashboardService()
    print(obj.get_info())
