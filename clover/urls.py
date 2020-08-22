"""
# url mapping for views
# /api/version/module/function
"""
from clover.environment.views import TeamView as Team
from clover.keyword.views import KeywordView as Keyword
from clover.environment.views import VariableView as Variable
from clover.interface.views import InterfaceView as Interface
from clover.suite.views import SuiteView as Suite
from clover.report.views import ReportView as Report
from clover.index.views import IndexView as Index
from clover.task.views import TaskView as Task
from clover.plugin.views import PluginView as Plugin
from clover.dashboard.views import DashboardView as Dashboard


def map_urls(app):
    # 版本相关路由与视图带增加
    # 配置管理相关路由与视图
    index = Index.as_view("index")
    app.add_url_rule(
        "/api/v1/index/info",
        view_func=index,
        methods=['GET'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/index/count",
        view_func=index,
        methods=['GET'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/index/config",
        view_func=index,
        methods=['GET'],
        strict_slashes=False,
    )

    # 配置管理相关路由与视图
    team = Team.as_view("team")
    app.add_url_rule(
        "/api/v1/team/create",
        view_func=team,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/team/delete",
        view_func=team,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/team/update",
        view_func=team,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/team/search",
        view_func=team,
        methods=['GET'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/team/aggregate",
        view_func=team,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/team/navigation",
        view_func=team,
        methods=['POST'],
        strict_slashes=False,
    )

    variable = Variable.as_view("variable")
    app.add_url_rule(
        "/api/v1/variable/create",
        view_func=variable,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/variable/delete",
        view_func=variable,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/variable/update",
        view_func=variable,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/variable/search",
        view_func=variable,
        methods=['GET'],
        strict_slashes=False,
    )

    # 关键字相关路由与视图
    keyword = Keyword.as_view("keyword")
    app.add_url_rule(
        "/api/v1/keyword/create",
        view_func=keyword,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/keyword/delete",
        view_func=keyword,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/keyword/update",
        view_func=keyword,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/keyword/search",
        view_func=keyword,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/keyword/debug",
        view_func=keyword,
        methods=['POST'],
        strict_slashes=False,
    )

    # 接口测试相关路由与视图
    interface = Interface.as_view("interface")
    app.add_url_rule(
        "/api/v1/interface/create",
        view_func=interface,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/interface/delete",
        view_func=interface,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/interface/update",
        view_func=interface,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/interface/search",
        view_func=interface,
        methods=['GET', 'POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/interface/trigger",
        view_func=interface,
        methods=['GET', 'POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/interface/switch",
        view_func=interface,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/interface/tree",
        view_func=interface,
        methods=['POST'],
        strict_slashes=False,
    )

    # 测试套件相关路由与视图
    suite = Suite.as_view("suite")
    app.add_url_rule(
        "/api/v1/suite/create",
        view_func=suite,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/suite/delete",
        view_func=suite,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/suite/update",
        view_func=suite,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/suite/search",
        view_func=suite,
        methods=['GET', 'POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/suite/trigger",
        view_func=suite,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/suite/switch",
        view_func=suite,
        methods=['POST'],
        strict_slashes=False,
    )

    # 定时任务相关路由与视图
    task = Task.as_view("task")
    app.add_url_rule(
        "/api/v1/task/create",
        view_func=task,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/task/delete",
        view_func=task,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/task/update",
        view_func=task,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/task/search",
        view_func=task,
        methods=['get', 'POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/report/trigger",
        view_func=task,
        methods=['POST'],
        strict_slashes=False,
    )

    # 测试报告相关路由与视图
    report = Report.as_view("report")
    app.add_url_rule(
        "/api/v1/report/delete",
        view_func=report,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/report/search",
        view_func=report,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/report/log",
        view_func=report,
        methods=['POST'],
        strict_slashes=False,
    )

    # 插件相关路由与视图
    plugin = Plugin.as_view("plugin")
    app.add_url_rule(
        "/api/v1/plugin/create",
        view_func=plugin,
        methods=['POST'],
        strict_slashes=False,
    )

    # 看板相关路由与视图
    dashboard = Dashboard.as_view("dashboard")
    app.add_url_rule(
        "/api/v1/dashboard/info",
        view_func=dashboard,
        methods=['GET', 'POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/dashboard/suite",
        view_func=dashboard,
        methods=['GET', 'POST'],
        strict_slashes=False,
    )
