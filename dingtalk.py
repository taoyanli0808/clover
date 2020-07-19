import requests
import json
import urllib.request
from clover.report.models import ReportModel
from clover.models import query_to_dict
from time import sleep

class Dingtalk(object):

    def SendMessage(self,id):
        '''
        url需要更改为自己的群机器人Webhook.singleURL也需要修改
        :param report_rul:
        :return:
        '''
        url = "https://oapi.dingtalk.com/robot/send?access_token=eeaf8569dc3fc44b54b4a19e909f9d2c1c695ad14c25ef23dad767374749f79a"
        header = {
            'Content-Type': 'application/json'
        }
        data = {
          "actionCard": {
             "title": "clover平台通知",
             "text": "接口自动化测试报告",
             "btnOrientation": "0",
             "singleTitle": "查看报告详情",
             "singleURL" : "http://127.0.0.1:3000/report/detail?id={0}".format(id)
          },
            "msgtype": "actionCard"
        }
        requests.request('POST', url, data=json.dumps(data), headers=header)

    def searchid(self):
        '''
        查找数据库最后的一次报告id作为发送的id
        :return:
        '''
        results = ReportModel.query.order_by(ReportModel.id.desc()).limit(1)
        results = query_to_dict(results)
        return results[0]['id']
#
#     def getHtml(self,id):
#         '''
#         url网络链接，把链接的内容读取出来，存在html变量里
#         :param url:
#         :return:
#         '''
#         request = urllib.request.Request("http://127.0.0.1:3000/report/detail?id={0}".format(id))
#         sleep(2)
#         response = urllib.request.urlopen(request)
#         print(response)
#         html = response.read()
#         return html
#
#     def saveHtml(self,file_name, file_content):
#         '''
#          打开一个名为 file_name 的文件，把网页内容写进去
#         :param file_name:
#         :param file_content:
#         :return:
#         '''
#         with open(file_name.replace('/', '_') + '.html', 'wb') as f:
#             f.write(file_content)
#
# a=Dingtalk()
# html = a.getHtml(8)
# a.saveHtml("report", html)
# print("结束")