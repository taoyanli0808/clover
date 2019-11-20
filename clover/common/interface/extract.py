
import re
import json


class Extract():

    @staticmethod
    def extract_by_re(data, pattern):
        """
        # 使用由特定分隔符组成的表达式提取数据，默认分隔符为英文句号。
        :param data: 需要处理的数据
        :param pattern: 正则表达式
        :return: None如果提取失败
        """
        # 如果表达式编译失败会返回None
        if re.compile(pattern) is None:
            return None

        # 如果findall找不到匹配数据返回空列表
        # 这里统一解析失败的返回值为None
        match = re.findall(pattern, data)
        return match[0] if match else None


    @staticmethod
    def extract_by_delimiter(data, expression, separator='.'):
        """
        # 使用由特定分隔符组成的表达式提取数据，默认分隔符为英文句号。
        :param data: 需要处理的数据
        :param expression: 提取数据的表达式
        :param separator: 指定的分隔符
        :return: None如果提取失败
        """

        # 表达式必须是字符串，否则无法继续处理
        if not isinstance(expression, str):
            return None
        expression = expression.split(separator)

        # 如果data是字符串则默认是json数据，转为python对象。
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.decoder.JSONDecodeError:
                return None

        # 下面的处理逻辑用来区分数据是列表还是字典
        # 如果数据是列表则索引是整数
        # 如果数据是字典则索引是字符串
        # 其它情况暂时按照错误处理
        for expr in expression:
            try:
                expr = int(expr)
                data = data[expr]
            except ValueError:
                data = data.get(expr, None)

            # data是None说明解析出错或者解析结束，退出循环
            if data is None:
                break

        return data


if __name__ == '__main__':
    extract = Extract()
    data = '{"status": 0, "message": "ok", "data": [{"price": "13"}, {"price": "15"}]}'
    print(extract.extract_by_delimiter(data, "data.-1.price"))
    print(extract.extract_by_re(data, r'\"status\": (.*?),'))