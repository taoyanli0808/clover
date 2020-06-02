
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

    def get_interface_statistics(self, details):
        """
        :param details:
        :return:
        """
        interface = {
            'verify': 0,
            'passed': 0,
            'failed': 0,
            'error': 0,
            'sikped': 0,
            'total': 0,
            'percent': 0.0,
        }

        interface['total'] = len(details)
        verify = [len(detail['result']) for detail in details if 'result' in detail]
        interface['verify'] = sum(verify)
        for detail in details:
            if detail['status'] == 'error':
                interface['error'] += 1
            elif detail['status'] == 'failed':
                interface['failed'] += 1
            elif detail['status'] == 'sikped':
                interface['sikped'] += 1
            else:
                interface['passed'] += 1
        percent = 100 * interface['passed'] / interface['total']
        interface['percent'] = round(percent, 2)
        return interface

    def save(self, context, details, logger):
        """
        :param context:
        :param detail:
        :param log:
        """
        if 'report' in context.user and context.user['report']:
            name = context.user.get('report')
        elif 'name' in context.user and context.user['name']:
            name = context.user.get('name')
        else:
            name = 'Clover测试平台报告'
        end = datetime.datetime.now()

        report = {
            'team': context.user.get('team'),
            'project': context.user.get('project'),
            'name': name,
            'type': 'interface',
            'platform': get_system_info(),
            'start': friendly_datetime(self.start),
            'end': friendly_datetime(end),
            'duration': (end - self.start).total_seconds(),
            'interface': self.get_interface_statistics(details),
            'detail': details,
            'log': [],#self.get_log(data, logger),
        }

        service = ReportService()
        service.create(report)
