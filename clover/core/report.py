
import datetime

from clover.common import get_system_info
from clover.common import friendly_datetime
from clover.report.service import ReportService


class Report(object):

    def __init__(self, suite, trigger):
        """
        """
        self.start = datetime.datetime.now()
        self.end = datetime.datetime.now()
        self.report = {
            'suite_id': suite.id,
            'suite_name': suite.name,
            'team': suite.team,
            'project': suite.project,
            'type': 'interface',
            'name': trigger.report,
            'platform': get_system_info(),
            'valid': trigger.trigger != 'clover',
            'start': friendly_datetime(self.start),
            'end': friendly_datetime(self.end),
            'interface': {
                "error": 0,
                "total": 0,
                "failed": 0,
                "passed": 0,
                "skiped": 0,
                "verify": 0,
                "percent": 0.0,
            }
        }
        self.service = ReportService()
        self.id = self.service.create(self.report)

    def save(self, logid):
        """
        :param suite:
        :param trigger:
        :param details:
        :param logger:
        """
        self.end = datetime.datetime.now()
        self.report['end'] = friendly_datetime(self.end)
        self.report['duration'] = (self.end - self.start).total_seconds()
        self.report['interface']['total'] = sum(self.report['interface'].values())
        try:
            percent = 100 * self.report['interface']['passed'] / self.report['interface']['total']
        except ZeroDivisionError:
            percent = 0.0
        self.report['interface']['percent'] = round(percent, 2)
        self.report.update({
            'id': self.id,
            'logid': logid,
        })
        print(self.report)
        result = self.service.update(self.report)
        return result
