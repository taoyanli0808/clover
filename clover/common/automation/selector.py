

class Selector(object):

    def __init__(self, driver):
        """
        :param driver:
        """
        self.driver = driver

    def find_element_by_id(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        selector = parameter.get('selector', None)
        if selector is None:
            raise Exception("")
        return self.driver.find_element_by_id(selector)

    def find_element_by_name(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        selector = parameter.get('selector', None)
        if selector is None:
            raise Exception("")
        return self.driver.find_element_by_name(selector)

    def find_element_by_css_selector(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        selector = parameter.get('selector', None)
        if selector is None:
            raise Exception("")
        return self.driver.find_element_by_css_selector(selector)

    def find_element_by_class(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        selector = parameter.get('selector', None)
        if selector is None:
            raise Exception("")
        return self.driver.find_element_by_class(selector)

    def find_element_by_xpath(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        selector = parameter.get('selector', None)
        if selector is None:
            raise Exception("")
        return self.driver.find_element_by_xpath(selector)

    def find_element_by_tag(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        selector = parameter.get('selector', None)
        if selector is None:
            raise Exception("")
        return self.driver.find_element_by_tag(selector)

    def find_element_by_link_text(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        selector = parameter.get('selector', None)
        if selector is None:
            raise Exception("")
        return self.driver.find_element_by_link_text(selector)

    def find_element_by_partial_link_text(self, element=None, parameter={}):
        """
        :param parameter:
        :return:
        """
        selector = parameter.get('selector', None)
        if selector is None:
            raise Exception("")
        return self.driver.find_element_by_partial_link_text(selector)
