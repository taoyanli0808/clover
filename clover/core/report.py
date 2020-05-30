
import datetime

from clover.report.service import ReportService

class Report():

    def __init__(self, data):
        """
        :param data:
        """
        self.team = data.get('team')
        self.project = data.get('project')
        # 如果有传递报告名称则优先使用报告名称
        # 如果没有报告名称则优先使用套件名称或接口名称
        # 如果既没有套件名称也没有接口名称则使用
        if 'report' in data and data['report']:
            self.name = data.get('report')
        elif 'name' in data and data['name']:
            self.name = data.get('name')
        else:
            self.name = 'Clover测试平台报告'
        self.type = 'interface'
        self.start = datetime.datetime.now()
        self.end = None

    def update(self):
        self.end = datetime.datetime.now()
        self.duration = self.end - self.start
        print(self.__dict__)
        # self.platform =
        # service = ReportService()
        # service.update()
        # update_report = {
        #     'team': data['team'],
        #     'project': data['project'],
        #     'name': name,
        #     'type': 'interface',
        #     'interface': executor.interface,
        #     'start': executor.start,
        #     'end': executor.end,
        #     'duration': (executor.end - executor.start).total_seconds(),
        #     'platform': get_system_info(),
        #     'detail': executor.result,
        # }
        # report_service = ReportService()
        # report_service.update(update_report)