"""
# https://github.com/cameronmaske/celery-once
"""
from celery_once import QueueOnce

from clover.exts import task
from clover.common import get_system_info
from clover.common.executor import Executor
from clover.report.service import ReportService


@task.task(base=QueueOnce, once={'graceful': True})
def interface_task(cases, data, report):
    from clover import app

    with app.test_request_context():

        executor = Executor()
        executor.execute(cases, data)

        name = data['report'] if 'report' in data and data['report'] else data['name']
        update_report = {
            'id': report['id'],
            'team': data['team'],
            'project': data['project'],
            'name': name,
            'type': 'interface',
            'start': executor.start,
            'end': executor.end,
            'duration': (executor.end - executor.start).total_seconds(),
            'platform': get_system_info(),
            'detail': executor.result,
            'log': executor.log,
        }
        report_service = ReportService()
        report_service.update(update_report)

    return report
