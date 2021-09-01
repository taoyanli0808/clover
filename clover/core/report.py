
import datetime

from clover.common import get_system_info
from clover.common import friendly_datetime
from clover.report.service import ReportService

class Report():

    def __init__(self):
        """
        """
        self.start = datetime.datetime.now()

    def get_log(self, suite, logger):
        """
        :param suite:
        :param logger:
        :return:
        """
        return {
            'type': suite.type,
            'sub_type': suite.sub_type,
            'case': suite.id,
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

    def save(self, suite, trigger, details, logger):
        """
        :param suite:
        :param trigger:
        :param details:
        :param logger:
        """
        end = datetime.datetime.now()
        report = {
            'team': suite.team,
            'project': suite.project,
            'name': trigger.report,
            'type': 'interface',
            'platform': get_system_info(),
            'start': friendly_datetime(self.start),
            'end': friendly_datetime(end),
            'duration': (end - self.start).total_seconds(),
            'interface': self.get_interface_statistics(details),
            'valid': trigger.trigger != 'clover',
            'detail': details,
            'log': self.get_log(suite, logger),
        }

        service = ReportService()
        result = service.create(report)
        return result
