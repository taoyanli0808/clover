
from clover.suite.models import SuiteModel
from clover.interface.models import InterfaceModel


class Submit(object): pass


class Context(object):

    def __init__(self):
        self.id = 0
        self.name = '默认套件名称'
        self.type = 'interface'
        self.cases = []
        self.submit = Submit()

    def build_context(self, data: dict):
        """
        :param data:
        :return:
        """
        self.id = data.get('id')
        self.name = data.get('name')
        self.type = data.get('type')
        if self.type == 'interface':
            self.cases = [InterfaceModel.query.get(self.id)]
        elif self.type == 'suite':
            suite = SuiteModel.query.get(self.id)
            # print(suite.to_dict())
            self.cases = [InterfaceModel.query.get(case['data']['id']) for case in suite.cases]
        else:
            print("类型错误！")
        for key, value in data.get('user').items():
            setattr(self.submit, key, value)
