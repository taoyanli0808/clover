
from clover.suite.models import SuiteModel
from clover.interface.models import InterfaceModel


class Submit(object): pass


class Context(object):

    def __init__(self):
        self.case = []
        self.submit = Submit()

    def build_context(self, data: dict):
        """
        :param data:
        :return:
        """
        id = data.get('id')
        type = data.get('type')
        if type == 'interface':
            self.case = [InterfaceModel.query.get(id)]
        elif type == 'suite':
            suite = SuiteModel.query.get(id)
            self.case = [InterfaceModel.query.get(case) for case in suite.cases]
        else:
            print("类型错误！")
        for key, value in data.get('user').items():
            setattr(self.submit, key, value)
