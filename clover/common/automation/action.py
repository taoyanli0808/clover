

class Action():

    def __init__(self, driver):
        """
        :param driver:
        """
        self.driver = driver

    def send_keys(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        if element is None:
            raise Exception("")
        selector = parameter.get('selector', "")
        element.send_keys(selector)

    def click(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        if element is None:
            raise Exception("")
        element.click()

    def context_click(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        self.driver.context_click()

    def double_click(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        self.driver.double_click()

    def drag_and_drop(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        self.driver.drag_and_drop()

    def click_and_hold(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        self.driver.click_and_hold()

    def move_to_element(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        self.driver.move_to_element()

    def move_by_offset(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        self.driver.move_by_offset()
