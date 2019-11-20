
from clover.common.utils.mongo import Mongo
from clover.common.automation.driver import Driver
from clover.common.utils import get_friendly_id as get_case_id

# from worker.tasks import run_automation


class Service(object):

    def __init__(self):
        self.db = Mongo()

    def debug(self, data):
        """
        :param data:
        :return:
        """
        driver = Driver()
        driver.run(data['commands'])

    def create(self, data):
        """
        :param data:
        :return:
        """
        data.setdefault('_id', get_case_id())
        id = self.db.insert("clover", "automation", data)
        return id

    def delete(self, data):
        """
        :param data:
        :return:
        """
        self.db.delete("clover", "automation", {'_id': data.get('id')})

    def run_task(self, data):
        """
        :param data:
        :return:
        """
        task_id = data.get('task_id')
        run_automation.delay(task_id)
