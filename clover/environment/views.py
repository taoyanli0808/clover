
import traceback

from flask import request
from flask import jsonify

from clover.environment.service import Service
from clover.views import CloverView


class TeamView(CloverView):

    def __init__(self):
        super(TeamView, self).__init__()

    def create(self):

        data = request.get_json()

        if 'team' not in data or not data['team']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter team[{0}]".format(data['team']),
                'data': data
            })

        if 'project' not in data or not data['project']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter project[{0}]".format(data['project']),
                'data': data
            })

        if 'owner' not in data or not data['owner']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter owner[{0}]".format(data['owner']),
                'data': data
            })

        try:
            service = Service()
            id = service.Teamcreate(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def delete(self):

        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter id[{0}]".format(data['id']),
                'data': data
            })

        try:
            service = Service()
            id = service.Teamdetele(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def update(self):

        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter id[{0}]".format(data['id']),
                'data': data
            })

        try:
            service = Service()
            id = service.Teamupdate(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def search(self):

        data = request.values.to_dict()

        try:
            service = Service()
            total, result = service.Teamsearch(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': result,
                'total': total,
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def aggregate(self):

        data = request.get_json()

        try:
            service = Service()
            data = service.Teamaggregate(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': data
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def debug(self):
        data = request.get_json()
        if 'mock' not in data or not data['mock']:
            return jsonify({
                'status': 400,
                'message': 'invalid parameter [mock]!',
                'data': data
            })

        if 'snippet' not in data or not data['snippet']:
            return jsonify({
                'status': 400,
                'message': 'invalid parameter [snippet]!',
                'data': data
            })

        try:
            service = Service()
            result = service.Teamdebug(data)
            return jsonify({
                'status': 0,
                'message': "ok",
                'data': result
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': data
            })

    def save(self):
        data = request.get_json()

        if 'mock' not in data or not data['mock']:
            return jsonify({
                'status': 400,
                'message': 'invalid parameter [mock]!',
                'data': data
            })

        if 'snippet' not in data or not data['snippet']:
            return jsonify({
                'status': 400,
                'message': 'invalid parameter [snippet]!',
                'data': data
            })

        try:
            service = Service()
            result = service.Teamsave(data)
            return jsonify({
                'status': 0,
                'message': "ok",
                'data': result
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': data
            })

class VariableView(CloverView):

    def __init__(self):
        super(VariableView, self).__init__()

    def create(self):

        data = request.get_json()
        if 'type' not in data or not data['type']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter type[{0}]".format(data['type']),
                'data': data
            })

        if 'team' not in data or not data['team']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter team[{0}]".format(data['team']),
                'data': data
            })

        if 'project' not in data or not data['project']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter project[{0}]".format(data['project']),
                'data': data
            })

        if 'owner' not in data or not data['owner']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter owner[{0}]".format(data['owner']),
                'data': data
            })

        try:
            service = Service()
            id = service.Variabcreate(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def delete(self):

        data = request.get_json()

        if 'type' not in data or not data['type']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter type[{0}]".format(data['type']),
                'data': data
            })

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter id[{0}]".format(data['id']),
                'data': data
            })

        try:
            service = Service()
            id = service.Variabdetele(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def update(self):

        data = request.get_json()

        if 'type' not in data or not data['type']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter type[{0}]".format(data['type']),
                'data': data
            })

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter id[{0}]".format(data['id']),
                'data': data
            })

        try:
            service = Service()
            id = service.Variabupdate(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def search(self):

        data = request.values.to_dict()

        if 'type' not in data or not data['type']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter type[{0}]".format(data['type']),
                'data': data
            })

        try:
            service = Service()
            total, result = service.Variabsearch(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': result,
                'total': total,
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def aggregate(self):

        data = request.get_json()

        try:
            service = Service()
            data = service.Variabaggregate(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': data
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def debug(self):
        data = request.get_json()
        if 'mock' not in data or not data['mock']:
            return jsonify({
                'status': 400,
                'message': 'invalid parameter [mock]!',
                'data': data
            })

        if 'snippet' not in data or not data['snippet']:
            return jsonify({
                'status': 400,
                'message': 'invalid parameter [snippet]!',
                'data': data
            })

        try:
            service = Service()
            result = service.Variabdebug(data)
            return jsonify({
                'status': 0,
                'message': "ok",
                'data': result
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': data
            })

    def save(self):
        data = request.get_json()

        if 'mock' not in data or not data['mock']:
            return jsonify({
                'status': 400,
                'message': 'invalid parameter [mock]!',
                'data': data
            })

        if 'snippet' not in data or not data['snippet']:
            return jsonify({
                'status': 400,
                'message': 'invalid parameter [snippet]!',
                'data': data
            })

        try:
            service = Service()
            result = service.Variabsave(data)
            return jsonify({
                'status': 0,
                'message': "ok",
                'data': result
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': data
            })

