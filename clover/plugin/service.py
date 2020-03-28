
import os
import json

from werkzeug.utils import import_string


class PluginService(object):

    def create(self, data, upload):
        """
        :param data:
        :param upload:
        :return:
        """
        team = data.get('team')
        project = data.get('project')
        plugin = data.get('plugin')
        file = data.get('file')

        # 通过目录查找所有有效插件，每个插件是一个py文件
        directories = os.path.join(os.getcwd(), 'clover', 'common', 'plugin')
        plugin_file = [file for file in os.listdir(directories) if file != '__init__.py']
        plugins = list(map(lambda file: file.split('.')[0], plugin_file))

        if plugin not in plugins:
            return None

        # 创建pipeline对象，初始化团队与项目属性。
        module = "clover.common.plugin.{0}:{1}".format(plugin, plugin.capitalize())
        object = import_string(module)()
        object.team, object.project = team, project

        """
        # 这里根据plugin参数确定转换方法
        # 如果plugin是postman则直接读取json数据
        # 如果plugin是jmeter则将jmx转json数据
        # 然后调用插件的parse方法组装需要的数据
        """
        if plugin == 'postman':
            content = json.load(upload)
            object.parse(content)
        elif plugin == 'jmeter':
            content = ''
            object.parse(content)
        elif plugin == 'charles':
            content = json.load(upload)
            object.parse(content)
        else:
            return None

        # 创建插件
        object.create()


