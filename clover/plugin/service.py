
import os

from werkzeug.utils import import_string


class PluginService(object):

    def create(self, data):
        """
        :param data:
        :return:
        """
        team = data.get('team')
        project = data.get('project')
        plugin = data.get('plugin')

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

        # 创建插件
        # 这里需要解析文件并创建相应参数。
        object.create()
