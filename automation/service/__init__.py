
from common.automation.driver import Driver


class Service(object):

    def debug(self, commands):
        """
        :param commands:
        :return:
        """
        driver = Driver()
        driver.run(commands)
