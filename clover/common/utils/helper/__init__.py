
import re


def derivation(data, results):
    """
    :param data:
    :param results:
    :return:
    """
    # 这里如果data是空值或者变量没有设置则不处理。
    if not data or not results:
        return data

    variable = re.findall(r'\{(.+?)\}', data)
    if variable:
        print(variable)
        variable = variable[0].strip()
        for result in results:
            if variable == result.name:
                return result.value
    else:
        return data
