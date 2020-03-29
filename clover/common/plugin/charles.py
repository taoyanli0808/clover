
from urllib.parse import urlparse
from werkzeug.utils import import_string

from clover.common.plugin import Pipeline

class Charles(Pipeline):

    def __init__(self):
        super(Charles, self).__init__()
        self.result = {
            'success': 0,
            'failed': 0,
            'total': 0
        }


    def handle_collection(self, content, type):
        """
        :param content:
        :param type:
        :return:
        """
        for item in content['log']['entries']:
            try:
                # 注意这里是直接取charles数据，不改变数据类型，因此body是dict。
                name = item['request']['url']

                old_headers = item['request']['headers']
                header=[]
                for headerone in old_headers:
                    headerone["key"] = headerone.pop("name")
                    if headerone['key'] !="Content-Length":
                        header.append(headerone)

                method = item['request']['method'].lower()

                # urlparse.path方法会算出url后面跟的path
                url = item['request']['url']
                host = urlparse(url).scheme +"://"+urlparse(url).netloc
                if '?' in name:
                    name=name.split("?")[0]
                path=urlparse(url).path

                if 'postData' in item['request']:
                    #取params
                    if 'params' in item['request']['postData']:
                        param_old=item['request']['postData']['params']
                        params=[]
                        for paramsone in param_old:
                           paramsone["key"]=paramsone.pop("name")
                           params.append(paramsone)
                    else:
                        params=[]
                    #取body
                    if 'text' in item['request']['postData']:
                        old_body = item['request']['postData']['text']
                        new_body = str(old_body).replace('\\','')
                        body={
                            'mode':"raw",
                            'data':new_body
                        }
                    else:
                        body = {
                            'mode': 'raw',
                            'data': ''
                        }
                elif "name" in str(item['request']['queryString']):
                   body={
                       'mode': 'raw',
                       'data': ''
                   }
                   param_old=item['request']['queryString']
                   params = []
                   for paramsone in param_old:
                       paramsone["key"] = paramsone.pop("name")
                       params.append(paramsone)

                else:
                    body = {
                        'mode': 'raw',
                        'data': ''
                    }
                    params=[]


                interface = {
                    'team': self.team,
                    'project': self.project,
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
                plugin = 'clover.interface.service:InterfaceService'
                service = import_string(plugin)()
                _, status, _, _ = service.create(interface)
                if status == 0:
                    self.result['success'] += 1
                else:
                    self.result['failed'] += 1
            except Exception:
                self.result['failed'] += 1
            self.result['total'] += 1

   #上传的只能是脚本，不可能是变量，所以直接处理就可以了
    def parse(self, content, type=None):
        self.handle_collection(content, type)
        return self.result
