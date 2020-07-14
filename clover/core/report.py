
import datetime

from clover.common import get_system_info
from clover.common import friendly_datetime
from clover.report.service import ReportService

class Report():

    def __init__(self):
        """
        """
        self.start = datetime.datetime.now()

    def get_log(self, context, logger):
        """
        :param context:
        :param logger:
        :return:
        """
        case = context.case[0].id
        type = context.case[0].type
        sub_type = context.case[0].sub_type
        return {
            'type': type,
            'sub_type': sub_type,
            'case': case,
            'logs': logger.to_dict(),
        }

    @staticmethod
    def get_interface_statistics(details):
        """
        :param details:
        :return:
        """
        interface = {'verify': 0, 'passed': 0, 'failed': 0, 'error': 0,
                     'skiped': 0, 'total': 0, 'percent': 0.0}
        verify = [len(detail['result']) for detail in details if 'result' in detail]
        interface['verify'] = sum(verify)
        for detail in details:
            if detail['status'] == 'error':
                interface['error'] += 1
            elif detail['status'] == 'failed':
                interface['failed'] += 1
            elif detail['status'] == 'skiped':
                interface['skiped'] += 1
            else:
                interface['passed'] += 1
        interface['total'] = len(details)
        try:
            percent = 100 * interface['passed'] / interface['total']
        except ZeroDivisionError:
            percent = 0.0
        interface['percent'] = round(percent, 2)
        return interface

    def save(self, context, details, logger):
        """
        :param context:
        :param details:
        :param logger:
        """
        if hasattr(context.submit, 'report') and context.submit.report:
            name = context.submit.report
        elif hasattr(context.submit, 'name') and context.submit.name:
            name = context.submit.name
        else:
            name = 'Clover测试平台报告'
        end = datetime.datetime.now()

        report = {
            'team': context.submit.team,
            'project': context.submit.project,
            'name': name,
            'type': 'interface',
            'platform': get_system_info(),
            'start': friendly_datetime(self.start),
            'end': friendly_datetime(end),
            'duration': (end - self.start).total_seconds(),
            'interface': self.get_interface_statistics(details),
            'detail': details,
            'log': self.get_log(context, logger),
        }

        service = ReportService()
        service.create(report)
