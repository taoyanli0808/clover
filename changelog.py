"""
# added － 这里记录新增加了哪些功能／接口
# changed － 功能／接口变更
# deprecated － 不建议使用的功能／接口，将来会删掉
# removed － 之前不建议使用的功能／接口，这次真的删掉了
# fixed － 这里记录解决了哪些问题
"""

changelog = [
    {
        'version': '0.7.5',
        'date': '2020-03-25',
        'added': [
            '创建套件页面被添加的接口可以删除。',
        ]
    },
    {
        'version': '0.7.4',
        'date': '2020-03-25',
        'changed': [
            '日志采用logging记录到文件，采用pre标签直接展示。',
        ]
    },
    {
        'version': '0.7.3',
        'date': '2020-03-23',
        'fixed': [
            '修复接口编辑页面提交后body部分变为[Object Object]问题',
            '修复接口运行时"expected string or bytes-like object报错"',
            '修复接口运行时"list" object has no attribute "encode"报错',
            '修复接口运行时requests请求报错导致运行失败的问题',
            '暂时关闭日志功能以解决运行出错的严重问题',
        ]
    },
    {
        'version': '0.7.2',
        'date': '2020-03-21',
        'fixed': [
            '修复请求体为空时postman报错的问题',
        ]
    },
    {
        'version': '0.7.1',
        'date': '2020-03-20',
        'changed': [
            '修改新的创建套件交互方式',
        ]
    },
    {
        'version': '0.6.1',
        'date': '2020-03-15',
        'fixed': [
            '修复环境变量中添加与修改时，没有判断变量名重复问题',
        ],
        'changed': [
            '新增create与updata中根据status来返回前端状态判断是否重复',
            '新增用project与name参数查询数据库步骤',
            '修复部分前端页面警告',
            '修改创建接口页面body部分，使其同步更新后端',
            '修改更新接口页面body部分，使其同步更新后端',
        ]
    },
    {
        'version': '0.6.0',
        'date': '2020-03-15',
        'fixed': [
            '修复postman插件创建接口时formdata和urlencoded类型数据处理不正确的问题',
        ],
        'changed': [
            '修改postman插件替换变量的方式，改为更严谨的变量替换',
            '修改接口请求体类型由列表改为字典{mode:"raw", data:"abc"}',
        ]
    },
    {
        'version': '0.5.7',
        'date': '2020-03-14',
        'fixed': [
            '修复postman插件创建变量失败的问题',
            '修复postman插件创建接口丢失端口号的问题',
            '修复postman插件当请求不存在path时创建失败的问题'
        ]
    },
    {
        'version': '0.5.7',
        'date': '2020-03-14',
        'fixed': [
            '修复postman插件创建变量失败的问题',
            '修复postman插件创建接口丢失端口号的问题',
            '修复postman插件当请求不存在path时创建失败的问题'
        ]
    },
    {
        'version': '0.5.6',
        'date': '2020-03-11',
        'fixed': [
            '修复特定情形下接口编辑页面断言和提取参数不可编辑问题',
            '修复header里ua包含英文分号导致解析不正确的问题'
        ]
    },
    {
        'version': '0.5.5',
        'date': '2020-02-27',
        'added': [
            '增加消息通知机制'
        ]
    },
    {
        'version': '0.5.4',
        'date': '2020-02-27',
        'added': [
            '增加邮箱通知模块，QQ邮箱验证通过'
        ]
    },
    {
        'version': '0.5.3',
        'date': '2020-02-27',
        'added': [
            '增加企业微信机器人通知模块'
        ]
    },
    {
        'version': '0.5.2',
        'date': '2020-02-26',
        'added': [
            '引入postman插件，支持倒入collection创建接口.'
        ]
    },
    {
        'version': '0.5.1',
        'date': '2020-02-23',
        'added': [
            '引入插件机制支持通过插件创建接口与套件.'
        ]
    },
    {
        'version': '0.4.1',
        'date': '2020-02-13',
        'added': [
            '引入celery_once确保任务只被执行一次.'
        ]
    },
    {
        'version': '0.4.0',
        'date': '2020-02-13',
        'added': [
            '增加定时任务页面，实现增删改查.'
        ]
    },
    {
        'version': '0.3.7',
        'date': '2020-02-11',
        'added': [
            '增加配置项控制功能是否生效.'
        ]
    },
    {
        'version': '0.3.6',
        'date': '2020-02-07',
        'added': [
            '增加接口编辑页面，打开接口列表页编辑接口的入口.'
        ]
    },
    {
        'version': '0.3.5',
        'date': '2020-02-07',
        'changed': [
            '修改创建接口页面添加断言与提取响应展示.'
            '修改添加断言与提取响应删除项行为，由依据表达式删除改为依据索引删除.'
        ]
    },
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
