
import datetime

from clover.common import get_system_info
from clover.common import friendly_datetime
from clover.report.service import ReportService

class Report():

    def __init__(self):
        """
        """
        self.start = datetime.datetime.now()

    def get_log(self, data, logger):
        """
        :param data:
        :param logger:
        :return:
        """
        case = data.get("id")
        type = data.get('type', 'interface')
        sub_type = data.get('sub_type', 'suite')
        data = {
            'type': type,
            'sub_type': sub_type,
            'case': case,
            'logs': logger.to_dict(),
        }
        print(50 * '*')
        print(data)
        print(50 * '*')
        return data

    def save(self, data, detail, logger):
        """
        :param data:
        :param detail:
        :param log:
        """
        if 'report' in data and data['report']:
            name = data.get('report')
        elif 'name' in data and data['name']:
            name = data.get('name')
        else:
            name = 'Clover测试平台报告'
        end = datetime.datetime.now()

        report = {
            'team': data.get('team'),
            'project': data.get('project'),
            'name': name,
            'type': 'interface',
            'platform': get_system_info(),
            'start': friendly_datetime(self.start),
            'end': friendly_datetime(end),
            'duration': (end - self.start).total_seconds(),
            'detail': detail,
            'log': self.get_log(data, logger),
        }

        service = ReportService()
        service.create(report)
