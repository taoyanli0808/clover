
from flask import request
from flask import jsonify
from flask import Blueprint
from flask import render_template

from automation.service import Service

automation = Blueprint('automation', __name__,
                       url_prefix='/automation',
                       static_folder='static',
                       template_folder='templates')


@automation.route("/create")
def create():
    return render_template("create.html")


@automation.route("/api/v1/debug", methods=['POST'])
def api_v1_debug():

    data = request.get_json()

    name = data.get('name', None)
    if not name:
        return jsonify({
            'status': 400,
            'message': "invalid parameter [name].",
            'data': data,
        })

    commands = data.get('commands', None)
    if not commands:
        return jsonify({
            'status': 400,
            'message': "invalid parameter [commands].",
            'data': data,
        })

    try:
        service = Service()
        id = service.debug(data)
        return jsonify({
            'status': 0,
            'message': "ok.",
            'data': {
                'id': id,
            },
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': "server internal error.",
            'data': str(error),
        })


@automation.route("/api/v1/create", methods=['POST'])
def api_v1_create():

    data = request.get_json()

    name = data.get('name', None)
    if not name:
        return jsonify({
            'status': 400,
            'message': "invalid parameter [name].",
            'data': data,
        })

    commands = data.get('commands', None)
    if not commands:
        return jsonify({
            'status': 400,
            'message': "invalid parameter [commands].",
            'data': data,
        })

    try:
        service = Service()
        service.create(data)
        return jsonify({
            'status': 0,
            'message': "ok.",
            'data': {},
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': "server internal error.",
            'data': str(error),
        })


@automation.route("/api/v1/delete", methods=['DELETE'])
def api_v1_delete():

    data = request.get_json()

    id = data.get('id', None)
    if not id:
        return jsonify({
            'status': 400,
            'message': "invalid parameter [id].",
            'data': data,
        })

    try:
        service = Service()
        service.delete(data)
        return jsonify({
            'status': 0,
            'message': "ok.",
            'data': {},
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': "server internal error.",
            'data': str(error),
        })
