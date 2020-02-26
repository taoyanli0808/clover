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
            if variables:
                data = data.replace('{{', '${').replace('}}', '}')
            return data

        """
        # 数据类型是列表，目前只有header、params和body参数
        # 且参数值均为字典，{key: xxx, value: xxx}
        """
        if isinstance(data, list):
            for index, item in enumerate(data):
                variables = re.findall(r'\{\{(.+?)\}\}', item['value'])
                if variables:
                    item['value'] = item['value'].replace('{{', '${').replace('}}', '}')
        return data

    def handle_body(self, data):
        """
        # raw以外的数据类型也需要处理。
        :param data:
        :return:
        """
        body = []
        if 'mode' in data and data['mode'] == 'raw':
            body = [{'key': 'raw', 'value': data['raw']}]
            body = self.change_postman_variable_to_clover(body)
        return body

    def parse(self, content, type=None):
        """
        # 处理时需要注意postman的数据长度可能超过MySQL数据库的字段长度。
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
            method = item['request']['method'].lower()
            host = item['request']['url']['protocol'] + '://' + \
                   '.'.join(item['request']['url']['host'])
            path = '/' + '/'.join(item['request']['url']['path'])
            header = item['request']['header']
            params = item['request']['url']['query']
            if 'body' in item['request']:
                body = item['request']['body']
            else:
                body = {}

            host = self.change_postman_variable_to_clover(host)
            path = self.change_postman_variable_to_clover(path)
            header = self.change_postman_variable_to_clover(header)
            print(params)
            params = self.change_postman_variable_to_clover(params)
            print(params)
            body = self.handle_body(body)

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

            # 这里是将postman的脚本转为python，很难，先不动了！
            if 'event' in item:
                for event in item['event']:
                    listen = event['listen']
                    code = event['script']['exec']
