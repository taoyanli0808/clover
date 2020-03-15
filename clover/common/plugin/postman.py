import re

from clover.common.plugin import Pipeline


class Postman(Pipeline):

    def __init__(self):
        super(Postman, self).__init__()

    def change_postman_variable_to_clover(self, data):
        """
        :param data:
        :return:
        """
        # 这里如果data是空值或者变量没有设置则不处理。
        if not data:
            return data

        # 数据类型是字符串，目前只有host和path参数
        if isinstance(data, str):
            variables = re.findall(r'\{\{(.+?)\}\}', data)
            for variable in variables:
                if variable:
                    data = data.replace('{{' + variable + '}}', '${' + variable + '}')
            return data

        """
        # 数据类型是列表，目前只有header、params参数
        # 且参数值均为字典，{key: xxx, value: xxx}
        """
        if isinstance(data, list):
            for item in data:
                variables = re.findall(r'\{\{(.+?)\}\}', item['value'])
                for variable in variables:
                    if variable:
                        item['value'] = item['value'].replace('{{' + variable + '}}', '${' + variable + '}')
            return data

        """
        # 数据类型是列表，目前只有body参数
        # 且参数值均为字典，{mode: xxx, data: xxx}
        # 这里注意body的data参数较为复杂
        # 若mode为raw则data为文本
        # 若mode为formdata或urlencoded则data为列表
        """
        if isinstance(data, dict):
            if data['mode'] in ['formdata', 'urlencoded']:
                for item in data['data']:
                    variables = re.findall(r'\{\{(.+?)\}\}', item['value'])
                    for variable in variables:
                        if variable:
                            item['value'] = item['value'].replace('{{' + variable + '}}', '${' + variable + '}')
                return data
            elif data['mode'] in ['file']:
                return data
            else:
                variables = re.findall(r'\{\{(.+?)\}\}', data['data'])
                for variable in variables:
                    if variable:
                        data['data'] = data['data'].replace('{{' + variable + '}}', '${' + variable + '}')
                return data

    def handle_collection(self, content, type):
        """
        :param content:
        :param type:
        :return:
        """
        # 这里确保数据长度满足数据库字段长度要求
        if len(content['info']['name']) < 64:
            self.suite = content['info']['name']
        else:
            self.suite = content['info']['name'][0:64]

        for item in content['item']:
            # 注意这里是直接取postman数据，不改变数据类型，因此body是dict。
            if len(item['name']) < 64:
                name = item['name']
            else:
                name = item['name'][0:64]

            header = item['request']['header']
            method = item['request']['method'].lower()

            host = item['request']['url']['protocol'] + '://' + \
                   '.'.join(item['request']['url']['host'])
            if 'port' in item['request']['url']:
                host += ':' + item['request']['url']['port']

            # path默认是首页请求，如果不是则进行拼接
            path = '/'
            if 'path' in item['request']['url']:
                path += '/'.join(item['request']['url']['path'])

            if 'query' in item['request']['url']:
                params = item['request']['url']['query']
            else:
                params = []

            if 'body' in item['request']:
                if item['request']['body']['mode'] == 'formdata':
                    body = {
                        'mode': item['request']['body']['mode'],
                        'data': item['request']['body']['formdata']
                    }
                elif item['request']['body']['mode'] == 'urlencoded':
                    body = {
                        'mode': item['request']['body']['mode'],
                        'data': item['request']['body']['urlencoded']
                    }
                elif item['request']['body']['mode'] == 'file':
                    body = {
                        'mode': item['request']['body']['mode'],
                        'data': item['request']['body']['file']
                    }
                else:
                    body = {
                        'mode': item['request']['body']['mode'],
                        'data': item['request']['body']['raw']
                    }
            else:
                body = {}

            host = self.change_postman_variable_to_clover(host)
            path = self.change_postman_variable_to_clover(path)
            header = self.change_postman_variable_to_clover(header)
            params = self.change_postman_variable_to_clover(params)
            body = self.change_postman_variable_to_clover(body)

            interface = {
                'name': name,
                'method': method,
                'host': host,
                'path': path,
                'header': header,
                'params': params,
                'body': body,
                'verify': [],
                'extract': [],
            }
            self.interfaces.append(interface)

    def handle_variable(self, content):
        """
        :param content:
        :return:
        """
        for item in content['values']:
            self.variables.append({
                'name': item['key'],
                'value': item['value'],
                'enable': 0 if item['enabled'] else 1
            })

    def parse(self, content, type=None):
        """
        # 处理时需要注意postman的数据长度可能超过MySQL数据库的字段长度。
        :param content:
        :param type:
        :return:
        """
        # 先判断是collection文件，还是变量文件（variable、environment）
        # 变量存在跟节点values
        if 'values' in content:
            self.handle_variable(content)
        # 集合存在根节点info
        if 'info' in content:
            self.handle_collection(content, type)
