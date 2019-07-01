

class Browser():

    def __init__(self, driver):
        """
        :param driver:
        """
        self.driver = driver

    def get(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        url = parameter.get("url", "http://127.0.0.1:9999")
        self.driver.get(url)

    def forward(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        self.driver.forward()

    def back(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        self.driver.back()

    def refresh(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        self.driver.refresh()

    def quit(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        self.driver.quit()

    def switch_to_frame(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        self.driver.switch_to_frame()

    def switch_to_window(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        self.driver.switch_to_window()

    def maximize_window(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        self.driver.maximize_window()

    def minimize_window(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        self.driver.minimize_window()
