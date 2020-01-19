
from sqlalchemy import func

from clover.exts import db
from clover.suite.models import SuiteModel
from clover.interface.models import InterfaceModel
from clover.environment.models import TeamModel
from clover.environment.models import VariableModel
from clover.environment.models import KeywordModel


class Service():

    def count(self):
        """
        :return:
        """
        count = {
            'team': TeamModel.query.with_entities(TeamModel.team).distinct().count(),
            'project': db.session.query(func.count(TeamModel.enable == 0)).scalar(),
            'interface': db.session.query(func.count(InterfaceModel.enable == 0)).scalar(),
            'suite': db.session.query(func.count(SuiteModel.enable == 0)).scalar(),
            'variable': db.session.query(func.count(VariableModel.enable == 0)).scalar(),
            'keyword': db.session.query(func.count(KeywordModel.enable == 0)).scalar(),
        }
        return count
