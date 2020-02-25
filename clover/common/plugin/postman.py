from clover.common.plugin import Pipeline


class PostmanPlugin(): pass


class Postman(Pipeline):

    def __init__(self):
        super(Postman, self).__init__()

    def handle_body(self, body):
        """
        :param body:
        :return:
        """
        if body['mode'] == 'raw':
            return [{'key': 'raw', 'value': body['raw']}]

    def handle_varify(self, verify):
        """
        :param verify:
        :return:
        """
        pass

    def handle_extract(self, extract):
        """
        :param extract:
        :return:
        """
        pass

    def parse(self, content, type=None):
        """
        # 处理时需要注意postman的数据长度可能超过MySQL数据库的字段长度。
        :param content:
        :param type:
        :return:
        """
        self.suite = content['info']['name'] if len(content['info']['name']) < 64 else content['info']['name'][0:64]
        for item in content['item']:
            host = item['request']['url']['protocol'] + '://' + \
                   '.'.join(item['request']['url']['host'])
            path = '/' + '/'.join(item['request']['url']['path'])
            interface = {
                'name': item['name'] if len(item['name']) < 64 else item['name'][0:64],
                'method': item['request']['method'],
                'host': host,
                'path': path,
                'header': item['request']['header'],
                'params': item['request']['url']['query'],
                'body': self.handle_body(item['request']['body']),
                'verify': [],
                'extract': [],
            }
            self.interfaces.append(interface)
