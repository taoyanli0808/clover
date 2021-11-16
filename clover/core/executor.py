"""
执行任务
"""

import datetime

from clover.core.log import Log
from clover.core.notify import Notify
from clover.core.report import Report
from clover.core.request import Request
from clover.core.response import Response
from clover.core.variable import Variable
from clover.core.validator import Validator
from clover.core.exception import ResponseException

from clover.log.service import LogService
from clover.history.service import HistoryService


class Executor(object):

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

    def save_interface_run_history(self, trigger, suite, case, validator):
        """
        :param trigger:
        :param suite:
        :param case:
        :param validator:
        :return:
        """
        # 先通过联合主键sid和cid查找接口运行历史，找到则更新
        service = HistoryService()

        history = {
            'suite_id': suite.id,
            'interface_id': case.id,
            'suite_name': suite.name,
            'interface_name': case.name,
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
        cookies, report, details = None, Report(suite, trigger), []
        """
        # 注意，变量对象必须在循环外被实例化，变量声明周期与执行器相同。
        # 使用团队和项目属性查询平台预置的自定义变量，通过触发时传递。
        # trigger参数为触发时用户添加的变量，优先级高于平台预置变量。
        """
        logid = []
        variable = Variable(suite, trigger)

        for case in suite.cases:
            # 字典log用于记录接口执行时必要的信息
            log = Log(report)
            log.set_init_log(case)

            request = Request(case, cookies)
            # 使用日志记录请求初始化数据
            log.set_request_log(request)

            log.set_variable_log(variable)

            variable.replace_variable(request)
            # 记录变量替换相关数据
            log.set_replace_log(request)

            # keyword.call_keyword(request, 'before_request')

            response, validator = Response(), Validator()
            try:
                # 当用例设置跳过时不进行接口请求。
                if case.status:
                    response = request.send_request()
                    cookies = response.cookies
            except ResponseException:
                self._set_status('error')
                validator.status = 'error'
            # 记录接口请求响应的相关数据信息
            log.set_response_log(response)

            validator.verify(case, response, variable, report)
            # 记录断言结果
            log.set_validator_log(validator)

            self._set_status(validator.status)
            validator.performance(response)
            # 开始时间、结束时间、接口耗时、时间基准、状态
            log.set_performance_log(response, validator)

            # 提取响应返回的数据传递给下一个接口使用
            extractor_log = variable.extract_variable_from_response(case, response)
            # 记录本次提取的过程和结果
            log.set_extractor_log(extractor_log)

            self.save_interface_run_history(trigger, suite, case, validator)

            # 这里是调试模式，需要返回数据给前端页面。
            if self.type == 'debug':
                return 0, "debug", response.get_response()

            log_service = LogService()
            _id = log_service.create(log.log)
            logid.append(_id)

        # 存储运行的测试报告到数据库。
        data = report.save(logid)

        notify = Notify()
        notify.send_message(data, self.status)
