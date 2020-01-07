"""
# url mapping for views
# /api/version/module/function
"""
from clover.environment.views import TeamView as team
from clover.environment.views import VariableView as project
from clover.interface.views import InterfaceView as Interface
from clover.suite.views import SuiteView as TestSuite


def map_urls(app):
    # 项目配置管理相关路由与视图
    environment = team.as_view("team")
    app.add_url_rule(
        "/api/v1/team/create",
        view_func=environment,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/team/delete",
        view_func=environment,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/team/update",
        view_func=environment,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/team/search",
        view_func=environment,
        methods=['GET'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/team/aggregate",
        view_func=environment,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/team/debug",
        view_func=environment,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/team/save",
        view_func=environment,
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
    testsuite = TestSuite.as_view("suite")
    app.add_url_rule(
        "/api/v1/suite/create",
        view_func=testsuite,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/suite/delete",
        view_func=testsuite,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/suite/update",
        view_func=testsuite,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/suite/search",
        view_func=testsuite,
        methods=['GET', 'POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/suite/trigger",
        view_func=testsuite,
        methods=['POST'],
        strict_slashes=False,
    )

