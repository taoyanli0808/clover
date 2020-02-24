
from werkzeug.utils import import_string


class Plugin(object):

    def __init__(self):
        self.type = None

    def create(self, **kwargs):
        """
        :return:
        """
        # 使用import_string寻找模型的类型，参数为str
        if not isinstance(self.type, str):
            raise ValueError("模型名必须为字符串。")

        # 实例化服务，保存到数据库
        service = import_string(self.type)()
        return service.create(kwargs)


class TeamPlugin(Plugin):

    def __init__(self):
        super(TeamPlugin, self).__init__()
        self.type = 'clover.environment.service:TeamService'


class VariablePlugin(Plugin):

    def __init__(self):
        super(VariablePlugin, self).__init__()
        self.type = 'clover.environment.service:VariableService'


class InterfacePlugin(Plugin):

    def __init__(self):
        super(InterfacePlugin, self).__init__()
        self.type = 'clover.interface.service:InterfaceService'


class SuitePlugin(Plugin):

    def __init__(self):
        super(SuitePlugin, self).__init__()
        self.type = 'clover.suite.service:SuiteService'


class Pipeline(Plugin):

    def __init__(self):
        super(Pipeline, self).__init__()

    def set_team(self, team):
        super(Pipeline).team = team

    def set_project(self, project):
        super(Pipeline).project = project

    def create(self, variables, interfaces):
        """
        :param variable:
        :param interfaces:
        :param suite:
        :return:
        """
        # 首先创建项目信息。
        team_plugin = TeamPlugin()
        team_plugin.create(team=self.team, project=self.project, owner='plugin')
        # 然后创建变量
        for variable in variables:
            variable_plugin = VariablePlugin()
            variable_plugin.create(team=self.team, project=self.project, owner='plugin', **variable)
        # 接着创建接口
        cases = []
        for interface in interfaces:
            interface_plugin = InterfacePlugin()
            id, _, _, _ = interface_plugin.create(team=self.team, project=self.project, **interface)
            cases.append(id)
        # 最后创建套件
        suite_plugin = SuitePlugin()
        suite_plugin.create(team=self.team, project=self.project, type='interface', cases=cases)


if __name__ == '__main__':
    pipeline = Pipeline()
    pipeline.team='大坏猫'
    pipeline.project='插件测试'
    variables = [
        {'name': 'pluginA', 'value': 123},
        {'name': 'pluginB', 'value': 'abc'},
    ]
    interfaces = [
        {
            'name': 'pluginA Interface',
            'method': 'get',
            'host': 'http://ditu.amap.com',
            'path': '/service/regeo',
            'header': [{"key": "", "value": ""}],
            'params': [
                {"key": "longitude", "value": "100.04925573429551"},
                {"key": "latitude", "value": "30.315590522490712"},
                {"key": "", "value": ""}
            ],
            'verify': [
                {"expected": "", "convertor": "", "extractor": "", "comparator": "", "expression": ""}
            ],
            'extract': [
                {"selector": "", "variable": "", "expression": ""}
            ],
        },
    ]
    pipeline.create(
        variables=variables,
        interfaces=interfaces,
    )
