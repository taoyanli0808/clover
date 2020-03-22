import re

from clover.common.plugin import Pipeline
from urllib.parse import urlparse

class Charles(Pipeline):

    def __init__(self):
        super(Charles, self).__init__()

    def change_charles_variable_to_clover(self, data):
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
        if len(content['log']['creator']['name']) < 64:
            self.suite = content['log']['creator']['name']
        else:
            self.suite = content['log']['creator']['name'][0:64]

        for item in content['log']['entries']:
            # 注意这里是直接取charles数据，不改变数据类型，因此body是dict。
            name = item['request']['url']

            old_headers = item['request']['headers']
            header=[]
            for headerone in old_headers:
                headerone["key"] = headerone.pop("name")
                header.append(headerone)

            method = item['request']['method'].lower()

            # urlparse.path方法会算出url后面跟的path
            url = item['request']['url']
            host = urlparse(url).scheme +"://"+urlparse(url).netloc
            path=urlparse(url).path
            if 'postData' in item['request']:
                param_old=item['request']['postData']['params']
                params=[]
                for paramsone in param_old:
                   paramsone["key"]=paramsone.pop("name")
                   params.append(paramsone)
            else:
                params=[]

            # if 'body' in item['request']:
            #     if item['request']['body'].get('mode') == 'formdata':
            #         body = {
            #             'mode': item['request']['body']['mode'],
            #             'data': item['request']['body']['formdata']
            #         }
            #     elif item['request']['body'].get('mode') == 'urlencoded':
            #         body = {
            #             'mode': item['request']['body']['mode'],
            #             'data': item['request']['body']['urlencoded']
            #         }
            #     elif item['request']['body'].get('mode') == 'file':
            #         body = {
            #             'mode': item['request']['body']['mode'],
            #             'data': item['request']['body']['file']
            #         }
            #     else:
            #         body = {
            #             'mode': item['request']['body'].get('mode') or 'raw',
            #             'data': item['request']['body'].get('raw') or ''
            #         }
            # else:
            body = {
                    'mode': 'raw',
                    'data': ''
                }

            host = self.change_charles_variable_to_clover(host)
            path = self.change_charles_variable_to_clover(path)
            header = self.change_charles_variable_to_clover(header)
            params = self.change_charles_variable_to_clover(params)
            body = self.change_charles_variable_to_clover(body)

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

   #上传的只能是脚本，不可能是变量，所以直接处理就可以了
    def parse(self, content, type=None):
        self.handle_collection(content, type)
