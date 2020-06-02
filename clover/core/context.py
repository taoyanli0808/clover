
from clover.models import query_to_dict
from clover.suite.models import SuiteModel
from clover.interface.models import InterfaceModel


class Context(object):

    def __init__(self):
        self.data = []
        self.user = None

    def build_context(self, data):
        """
        :param data:
        :return:
        """
        id = data.get('id')
        type = data.get('type')
        if type == 'interface':
            self.data = query_to_dict([InterfaceModel.query.get(id)])
        elif type == 'suite':
            self.data = query_to_dict(SuiteModel.query.get(id))
        else:
            print("类型错误！")
        self.user = data.get('user')
