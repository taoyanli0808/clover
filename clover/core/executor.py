"""
执行任务
"""

import datetime

from clover.common import friendly_datetime

from clover.core.notify import Notify
from clover.core.logger import Logger
from clover.core.report import Report
from clover.core.request import Request
from clover.core.keyword import Keyword
from clover.core.variable import Variable
from clover.core.validator import Validator
from clover.core.exception import ResponseException

from clover.history.service import HistoryService


class Executor():

    def __init__(self, type='trigger'):
        self.type = type
        # 这个status值为error、failed、skipped或passed，
        # 传递给notify用于判断是否需要发送运行结果的通知。
        self.status = 'passed'

    def _set_status(self, status):
        """
        # 考虑到套件内有多个接口和接口有多个断言，程序执行时会动态
        # 覆盖掉状态。次函数放置状态被覆盖。
        # 状态优先级：error > failed > skipped > passed
        # 如果当前状态为failed，传递skipped则状态不被修改。
        :param context:
        :return:
        """
        if self.status == 'error':
            return
        elif self.status == 'failed':
            if status != 'error':
                return
            self.status = status
        elif self.status == 'skipped':
            if status not in ['error', 'failed']:
                return
            self.status = status
        else:
            self.status = status

    def save_interface_run_history(self, trigger, suite, case, response, validator):
        """
        :param trigger:
        :param suite:
        :param case:
        :param response:
        :param validator:
        :return:
        """
        # 先通过联合主键sid和cid查找接口运行历史，找到则更新
        service = HistoryService()

        history = {
            'sid': suite.id,
            'cid': case.id,
            'sname': suite.name,
            'cname': case.name,
            'team': case.team,
            'project': case.project,
            'type': case.type,
            'sub_type': case.sub_type,
            'success': validator.status == 'passed',
            'error': validator.status == 'error',
            'failed': validator.status == 'failed',
            'skiped': validator.status == 'skiped',
            'valid': trigger.trigger != 'clover'
        }
        return service.create(history)

    def execute(self, suite, trigger):
        """
        :param suite:
        :param trigger:
        :return:
        """
        # 注意需要在执行最前端实例化report，report初始化时会记录开始时间点。
        cookies, report, details = None, Report(), []
        """
        # 注意，变量对象必须在循环外被实例化，变量声明周期与执行器相同。
        # 使用团队和项目属性查询平台预置的自定义变量，通过触发时传递。
        # trigger参数为触发时用户添加的变量，优先级高于平台预置变量。
        """
        keyword = Keyword('')
        variable = Variable(suite, trigger)

        # 因为是类属性存储日志，使用前先清理历史日志数据。
        Logger.clear()
        Logger.log("团队：{}，项目：{}".format(suite.team, suite.project), "开始执行")
        for case in suite.cases:
            detail = {'name': case.name}
            detail.setdefault('start', friendly_datetime(datetime.datetime.now()))

            request = Request(case, cookies)
            response = None
            validator = Validator()

            variable.replace_variable(request)
            keyword.call_keyword(request, 'before_request')
            try:
                # 当用例设置跳过时不进行接口请求。
                if case.status:
                    response = request.send_request()
                    cookies = response.cookies

                # 当用例跳过或接口请求异常时，response是None，此时设置elapsed为0
                elapsed = response.elapsed if response is not None else 0
                detail.setdefault('elapsed', elapsed)
            except ResponseException:
                Logger.log("请求异常，状态码：{}".format(request.status), "发送请求", 'error')
                Logger.log(request.message, "发送请求", 'error')
                self._set_status('error')
                validator.status = 'error'

            validator.verify(case, response, variable)
            detail.setdefault('status', validator.status)
            detail.setdefault('result', validator.result)

            self._set_status(validator.status)

            validator.performance(response)
            detail.setdefault('threshold', validator.threshold)
            detail.setdefault('performance', validator.level)

            variable.extract_variable_from_response(case, response)
            detail.setdefault('end', friendly_datetime(datetime.datetime.now()))

            self.save_interface_run_history(trigger, suite, case, response, validator)
            details.append(detail)

            # 这里是调试模式，需要返回数据给前端页面。
            if self.type == 'debug':
                return 0, "debug", response.get_response()

        # print(Logger.logs)

        # 存储运行的测试报告到数据库。
        data = report.save(suite, trigger, details, Logger)

        notify = Notify()
        notify.send_message(data, self.status)
