
import traceback

from flask import request
from flask import jsonify
from flask import Blueprint
from flask import render_template

from environment.service import Service

environment = Blueprint('environment', __name__,
                     static_folder='static',
                     template_folder='templates',
                     url_prefix='/environment')


@environment.route("/")
def index():
    return render_template("environment.html")


@environment.route("/api/v1/create", methods=['POST'])
def api_v1_create():

    data = request.get_json()

    if 'name' not in data or not data['name']:
        return jsonify({
            'status': 400,
            'message': "invalid parameter name[{0}]".format(data['name']),
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
    print(data)

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


@environment.route("/api/v1/search/")
def api_v1_search():

    data = request.values.to_dict()

    try:
        service = Service()
        data = service.search(data)
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
