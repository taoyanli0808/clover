"""
# url mapping for views
# /api/version/module/function
"""
from clover.environment.views import EnvironmentView as Environment
from clover.environment.views import KeywordView as Keyword
from clover.interface.views import InterfaceView as Interface
from clover.suite.views import SuiteView as TestSuite


def map_urls(app):
    # 配置管理相关路由与视图
    environment = Environment.as_view("environment")
    app.add_url_rule(
        "/api/v1/environment/create",
        view_func=environment,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/environment/delete",
        view_func=environment,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/environment/update",
        view_func=environment,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/environment/search",
        view_func=environment,
        methods=['GET'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/environment/aggregate",
        view_func=environment,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/environment/debug",
        view_func=environment,
        methods=['POST'],
        strict_slashes=False,
    )
    app.add_url_rule(
        "/api/v1/environment/save",
        view_func=environment,
        methods=['POST'],
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
        methods=['GET'],
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

