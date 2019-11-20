
import traceback

from flask import request
from flask import jsonify
from flask import Blueprint
from flask import render_template

from clover.environment.service import Service

environment = Blueprint('environment', __name__,
                     static_folder='static',
                     template_folder='templates',
                     url_prefix='/environment')


@environment.route("/team")
def team():
    return render_template("team.html")


@environment.route("/variable")
def variable():
    return render_template("variable.html")


@environment.route("/api/v1/create", methods=['POST'])
def api_v1_create():

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

    try:
        service = Service()
        id = service.create(data)
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


@environment.route("/api/v1/delete", methods=['POST'])
def api_v1_delete():

    data = request.get_json()

    if 'type' not in data or not data['type']:
        return jsonify({
            'status': 400,
            'message': "invalid parameter type[{0}]".format(data['type']),
            'data': data
        })

    if 'id_list' not in data or not data['id_list']:
        return jsonify({
            'status': 400,
            'message': "invalid parameter id_list[{0}]".format(data['id_list']),
            'data': data
        })

    try:
        service = Service()
        id = service.detele(data)
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


@environment.route("/api/v1/update", methods=['POST'])
def api_v1_update():

    data = request.get_json()

    if 'type' not in data or not data['type']:
        return jsonify({
            'status': 400,
            'message': "invalid parameter type[{0}]".format(data['type']),
            'data': data
        })

    if '_id' not in data or not data['_id']:
        return jsonify({
            'status': 400,
            'message': "invalid parameter _id[{0}]".format(data['_id']),
            'data': data
        })

    try:
        service = Service()
        id = service.update(data)
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


@environment.route("/api/v1/search")
def api_v1_search():

    data = request.values.to_dict()

    if 'type' not in data or not data['type']:
        return jsonify({
            'status': 400,
            'message': "invalid parameter type[{0}]".format(data['type']),
            'data': data
        })
    service = Service()
    data = service.search(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data
    })
    # try:
    #     service = Service()
    #     data = service.search(data)
    #     return jsonify({
    #         'status': 0,
    #         'message': 'ok',
    #         'data': data
    #     })
    # except Exception as error:
    #     return jsonify({
    #         'status': 500,
    #         'message': str(error),
    #         'traceback': traceback.format_stack(),
    #         'data': data
    #     })


@environment.route("/api/v1/aggregate", methods=['POST'])
def api_v1_aggregate():

    data = request.get_json()

    if 'type' not in data or not data['type']:
        return jsonify({
            'status': 400,
            'message': "invalid parameter type[{0}]".format(data['type']),
            'data': data
        })

    if 'key' not in data or not data['key']:
        return jsonify({
            'status': 400,
            'message': "invalid parameter key[{0}]".format(data['key']),
            'data': data
        })

    try:
        service = Service()
        data = service.aggregate(data)
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
