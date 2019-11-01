
import re


def derivation(data, results):
    """
    :param data:
    :param results:
    :return:
    """
    variable = re.findall(r'\{(.+?)\}', data)
    if variable is not None:
        variable = variable[0].strip()
        for result in results:
            if variable == result['name']:
                return result['value']
    else:
        return data
