
from sqlalchemy import func

from clover.exts import db
from clover.models import query_to_dict
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
        team = TeamModel.query.with_entities(
            TeamModel.team
        ).filter(
            TeamModel.enable == 0
        ).distinct().count()

        project = TeamModel.query.with_entities(
            TeamModel.project
        ).filter(
            TeamModel.enable == 0
        ).distinct().count()

        interface = InterfaceModel.query.with_entities(
            InterfaceModel
        ).filter(
            InterfaceModel.enable == 0
        ).distinct().count()

        suite = SuiteModel.query.with_entities(
            SuiteModel
        ).filter(
            SuiteModel.enable == 0
        ).distinct().count()

        variable = VariableModel.query.with_entities(
            VariableModel
        ).filter(
            VariableModel.enable == 0
        ).distinct().count()

        keyword = KeywordModel.query.with_entities(
            KeywordModel
        ).filter(
            KeywordModel.enable == 0
        ).distinct().count()

        count = {
            'team': team,
            'project': project,
            'interface': interface,
            'suite': suite,
            'variable': variable,
            'keyword': keyword,
        }
        return count
