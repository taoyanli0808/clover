
import json

import pymysql

from loguru import logger

from clover.config import MYSQL

from clover.suite.service import SuiteService


def all_integer(iterable):
    for element in iterable:
        if not isinstance(element, int):
            return False
    return True


def upgrade():
    logger.add("logs/upgrade.log")
    db = None
    # try:
    logger.info("Connect MySQL with configure: {}".format(MYSQL))
    db = pymysql.connect(**MYSQL)
    cursor = db.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT id, cases FROM suite")
    suites = cursor.fetchall()
    for suite in suites:
        cases = json.loads(suite['cases'])
        if not all_integer(cases):
            continue

        print("before upgrade suite: {} with cases : {} ".format(suite['id'], cases))
        upgrade_cases = []
        for index, case in enumerate(cases):
            cursor.execute("SELECT * FROM interface WHERE id='{}'".format(case))
            interface = cursor.fetchone()
            if 'created' in interface and not isinstance(interface['created'], str):
                interface['created'] = interface['created'].strftime('%Y-%m-%d %H:%M:%S')
            if 'updated' in interface and not isinstance(interface['updated'], str):
                interface['updated'] = interface['updated'].strftime('%Y-%m-%d %H:%M:%S')
            interface['body'] = json.loads(interface['body'])
            interface['params'] = json.loads(interface['params'])
            interface['header'] = json.loads(interface['header'])
            interface['verify'] = json.loads(interface['verify'])
            interface['extract'] = json.loads(interface['extract'])
            upgrade_case = {
                'data': interface,
                'name': interface['name'],
                'index': index,
                'caseId': case,
            }
            upgrade_cases.append(upgrade_case)

        service = SuiteService()
        service.update({'id': suite['id'], 'cases': upgrade_cases})

    if db is not None:
        db.close()


if __name__ == '__main__':
    upgrade()
