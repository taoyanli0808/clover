
class Trigger(object):
    """
    # trigger对象代表用户触发的数据。
    # 如果用户直接在clover平台页面进行触发，则trigger对象为页面上用户触发填写的数据；
    # 如果使用Jenkins插件进行触发，则trigger对象为插件数据，包括插件版本号等相关信息；
    # 如果用户直接调用api触发运行，则trigger对象为api请求时所携带的数据。
    """

    def __init__(self):
        self.type = 'interface'
        self.sub_type = 'interface'
        self.id = 0
        self.name = '默认套件名称'
        self.variable = []
        self.trigger = 'clover'

    def make_trigger(self, data):
        """
        :param data[type]: 触发的类型，可选suite或interface。
        :param data[sub_type]: 触发的子类型，可选interface。
        :param data[id]: 用例或套件的ID
        :param data[name]: 用例或套件的名字
        :param data[variable]: 触发运行时的变量信息
        :param data[trigger]: 触发运行的来源，目前有Clover页面，Jenkins和API三种方式
        :reutrn: None
        """
        if 'type' in data and not data['type'] and data['type'] in ['interface', 'suite']:
            self.type = data.get('type', 'interface')

        if 'sub_type' in data and not data['sub_type'] and data['sub_type'] in ['interface']:
            self.sub_type = data.get('sub_type')

        if 'id' in data and not data['id']:
            self.id = data.get('id')

        if 'name' in data and not data['name']:
            self.name = data.get('name')

        if 'variable' in data and not data['variable'] and isinstance(data['variable'], (list,)):
            self.variable = data.get('variable')

        if 'trigger' in data and not data['trigger']:
            self.trigger = data.get('trigger', 'clover')
