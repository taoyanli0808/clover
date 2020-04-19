
import smtplib

from email.mime.text import MIMEText
from email.header import Header

from config import EMAIL


def render_html(data):
    print(data)
    template = '''
        <table border="1" cellspacing="0" cellpadding="0">
        <tr><td>类型</td><td>{type}</td></tr>
        <tr><td>团队</td><td>{team}</td></tr>
        <tr><td>项目</td><td>{project}</td></tr>
        <tr><td>名称</td><td>{name}</td></tr>
        <tr><td>接口</td><td>{interface[total]}个</td></tr>
        <tr><td>断言</td><td>{interface[verify]}个</td></tr>
        <tr><td>成功率</td><td>{interface[percent]}%%</td></tr>
        <tr><td>开始时间</td><td>{start}</td></tr>
        <tr><td>结束时间</td><td>{end}</td></tr>
        <tr><td>报告地址</td><td><a href="http://www.52clover.cn/report/detail?id={id}">测试报告-{id}</a></td></tr>
        </table>
    '''.format(**data)
    return template


def send_email(data):
    """
    :param data:
    :return:
    """
    try:
        content = render_html(data)

        message = MIMEText(content, 'html', 'utf-8')
        message['To'] = ','.join(EMAIL['receiver'])
        message['From'] = Header("Clover测试平台", 'utf-8')  # 发送者
        message['Subject'] = Header('Clover平台运行报告！', 'utf-8')

        smtp = smtplib.SMTP(EMAIL['smtp_host'])
        smtp.login(EMAIL['sender'], EMAIL['password'])
        smtp.sendmail(EMAIL['sender'], EMAIL['receiver'], message.as_string())

        print("邮件发送成功")
    except smtplib.SMTPException as error:
        print("Error: 无法发送邮件，错误码[{0}].".format(error.smtp_code))


if __name__ == '__main__':
    data = {
        'id': 2,
        'type': 'interface',
        'team': '质量部',
        'project': 'clover测试平台',
        'name': '变量和断言',
        'interface': 1,
        'verify': 2,
        'percent': '100.0%',
        'start': '2020-01-17 17:24:00',
        'end': '2020-01-17 17:24:00',
    }
    send_email(data)
