"""
# 用于记录任务执行的信息。
"""

import datetime

from clover.common import friendly_datetime


class Log(object):

    def __init__(self, report):
        self.log = {
            'report_id': report.id,
            'start': friendly_datetime(datetime.datetime.now()),
            'end': None,
            'init': {},
            'request': {},
            'variable': {
                'extract': [],
                'trigger': [],
                'default': [],
            },
            'replace': {},
            'response': {},
            'validator': {
                'status': None,
                'result': [],
            },
            'performance': {},
            'extractor': [],
        }

    def set_init_log(self, case):
        self.log.setdefault('team', case.team)
        self.log.setdefault('project', case.project)
        self.log.setdefault('interface_id', case.id)
        self.log.setdefault('interface_name', case.name)
        self.log.setdefault('start', friendly_datetime(datetime.datetime.now()))

    def set_request_log(self, request):
        self.log['request'].setdefault('method', request.method)
        self.log['request'].setdefault('host', request.host)
        self.log['request'].setdefault('path', request.path)
        self.log['request'].setdefault('url', request.url)
        self.log['request'].setdefault('header', request.header)
        self.log['request'].setdefault('parameter', request.parameter)
        self.log['request'].setdefault('body', str(request.body))
        self.log['request'].setdefault('mode', request.body_mode)
        self.log['request'].setdefault('timeout', str(request.timeout))
        self.log['request'].setdefault('retry', request.retry)

    def set_variable_log(self, variable):
        self.log['variable']['extract'] = variable.extract
        self.log['variable']['trigger'] = variable.trigger
        self.log['variable']['default'] = variable.variables

    def set_replace_log(self, request):
        self.log['replace'].setdefault('host', request.host)
        self.log['replace'].setdefault('path', request.path)
        self.log['replace'].setdefault('url', request.url)
        self.log['replace'].setdefault('header', request.header)
        self.log['replace'].setdefault('parameter', request.parameter)
        self.log['replace'].setdefault('body', str(request.body))

    def set_response_log(self, response):
        self.log['response'].setdefault('code', response.status)
        self.log['response'].setdefault('reason', response.reason)
        self.log['response'].setdefault('data', response.response)
        self.log['response'].setdefault('header', response.header)
        self.log['response'].setdefault('cookie', response.cookies)
        self.log['response'].setdefault('elapsed', response.elapsed)

    def set_validator_log(self, validator):
        self.log['validator']['status'] = validator.status
        self.log['validator']['result'].extend(validator.result)

    def set_performance_log(self, response, validator):
        self.log['performance'].setdefault('start', response.start)
        self.log['performance'].setdefault('end', response.end)
        self.log['performance'].setdefault('elapsed', response.elapsed)
        self.log['performance'].setdefault('threshold', validator.threshold)
        self.log['performance'].setdefault('status', validator.level)

    def set_extractor_log(self, extractor):
        self.log['extractor'].extend(extractor)
        # 最后一步记录接口处理的完成时间
        self.log['end'] = friendly_datetime(datetime.datetime.now())
