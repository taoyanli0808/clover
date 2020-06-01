
import datetime

from clover.common import get_system_info
from clover.common import friendly_datetime
from clover.report.service import ReportService

class Report():

    def __init__(self):
        """
        """
        self.start = datetime.datetime.now()

    def save(self, data, detail, log):
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
            'log': log,
        }

        service = ReportService()
        service.create(report)
