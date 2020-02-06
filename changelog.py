"""
# added － 这里记录新增加了哪些功能／接口
# changed － 功能／接口变更
# deprecated － 不建议使用的功能／接口，将来会删掉
# removed － 之前不建议使用的功能／接口，这次真的删掉了
# fixed － 这里记录解决了哪些问题
"""

changelog = [
    {
        'version': '0.3.4',
        'date': '2020-02-06',
        'added': [
            '表格加载数据增加加载状态动画.',
        ],
        'changed': [
            '运行日志替换弹出框为单独页面.'
            '报告列表页查询结果不返回detail与log字段.'
        ]
    },
    {
        'version': '0.3.3',
        'date': '2020-02-05',
        'fixed': [
            '修复requirements.txt缺少的redis依赖.',
            '修复MySQL数据库report表插入初始值时间为0的问题.',
        ]
    },
    {
        'version': '0.3.2',
        'date': '2020-02-05',
        'changed': [
            'Celery异步运行任务.'
        ]
    }
]
