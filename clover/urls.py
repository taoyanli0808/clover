"""
# url mapping for views
# /api/version/module/function
"""
<<<<<<< HEAD
from clover.environment.views import TeamView as team
from clover.environment.views import VariableView as project
=======
from clover.environment.views import TeamView as Team
from clover.environment.views import KeywordView as Keyword
from clover.environment.views import VariableView as Variable
>>>>>>> remote_origin/master
from clover.interface.views import InterfaceView as Interface
from clover.suite.views import SuiteView as Suite
from clover.report.views import ReportView as Report
from clover.index.views import IndexView as Index


def map_urls(app):
<<<<<<< HEAD
    # 项目配置管理相关路由与视图
    environment = team.as_view("team")
    app.add_url_rule(
        "/api/v1/team/create",
        view_func=environment,
=======
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

    variable = Variable.as_view("variable")
    app.add_url_rule(
        "/api/v1/variable/create",
        view_func=variable,
>>>>>>> remote_origin/master
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
<<<<<<< HEAD
        "/api/v1/team/delete",
        view_func=environment,
=======
        "/api/v1/variable/delete",
        view_func=variable,
>>>>>>> remote_origin/master
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
<<<<<<< HEAD
        "/api/v1/team/update",
        view_func=environment,
=======
        "/api/v1/variable/update",
        view_func=variable,
>>>>>>> remote_origin/master
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
<<<<<<< HEAD
        "/api/v1/team/search",
        view_func=environment,
=======
        "/api/v1/variable/search",
        view_func=variable,
>>>>>>> remote_origin/master
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
<<<<<<< HEAD
        "/api/v1/team/aggregate",
        view_func=environment,
=======
        "/api/v1/keyword/delete",
        view_func=keyword,
>>>>>>> remote_origin/master
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
<<<<<<< HEAD
        "/api/v1/team/debug",
        view_func=environment,
=======
        "/api/v1/keyword/update",
        view_func=keyword,
>>>>>>> remote_origin/master
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
<<<<<<< HEAD
        "/api/v1/team/save",
        view_func=environment,
=======
        "/api/v1/keyword/search",
        view_func=keyword,
        methods=['GET'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/keyword/debug",
        view_func=keyword,
>>>>>>> remote_origin/master
        methods=['POST'],
        strict_slashes=False,
    )

    # 变量配置管理相关路由与视图
    val = project.as_view("project")
    app.add_url_rule(
        "/api/v1/project/create",
        view_func=val,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/project/delete",
        view_func=val,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/project/update",
        view_func=val,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/project/search",
        view_func=val,
        methods=['GET'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/project/aggregate",
        view_func=val,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/project/debug",
        view_func=val,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/project/save",
        view_func=val,
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
        "/api/v1/interface/debug",
        view_func=interface,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/interface/trigger",
        view_func=interface,
        methods=['GET', 'POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/interface/delete",
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
