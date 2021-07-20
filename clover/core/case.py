
from clover.suite.models import SuiteModel
from clover.interface.models import InterfaceModel


class Case(object):

    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.sub_type = 'interface'
        self.team = None
        self.project = None
        self.cases = []

    def build_cases(self, data: dict):
        """
        :param data:
        :return:
        """
        self.id = data.get('id')
        self.type = data.get('type')
        if self.type == 'interface':
            case = InterfaceModel.query.get(self.id)
            self.name = case.name
            self.cases = [case]
        elif self.type == 'suite':
            suite = SuiteModel.query.get(self.id)
            self.name = suite.name
            self.cases = [InterfaceModel.query.get(case['data']['id']) for case in suite.cases]
        else:
            print("类型错误！")

        if self.cases:
            self.team = self.cases[0].team
            self.project = self.cases[0].project
        # for key, value in data.get('user').items():
        #     setattr(self.user, key, value)
