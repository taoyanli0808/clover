
import os
import sys
import time

from selenium import webdriver


class Driver():

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.classify = self.__loader()

    def __loader(self):
        """
        :return:
        """
        classifies = {}
        workspace = os.getcwd()
        command_path = os.path.join(workspace, 'common', 'automation')
        sys.path.append(command_path)
        modules = os.listdir(command_path)
        for name in modules:
            file = os.path.join(command_path, name)
            name = name.split('.')[0]
            if not os.path.isfile(file):
                continue
            if name in ['__pycache__', '__init__', 'driver']:
                continue
            print("load module[{0}] from path[{1}]".format(name, file))
            module = __import__(name)
            if not hasattr(module, name.capitalize()):
                raise Exception("这里异常啦！")
            object = getattr(module, name.capitalize())(self.driver)
            classifies.setdefault(name, object)
        return classifies

    def run(self, commands):
        element = None
        for command in commands:
            message = "driver load module[{0}] to run command[{1}] with parameter[{2}]"
            print(message.format(command['classify'], command['command'], command['parameter']))
            classify = self.classify.get(command['classify'])
            element = getattr(classify, command['command'])(element, command['parameter'])
            # for stable, stay 1 seconds...
            time.sleep(1.0)
