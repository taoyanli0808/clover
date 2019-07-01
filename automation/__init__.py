
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

    commands = data.get('commands', None)
    if not commands:
        return jsonify({
            'status': 400,
            'message': "invalid parameter [commands].",
            'data': data,
        })
    service = Service()
    service.debug(commands)
    return jsonify({
        'status': 0,
        'message': "ok.",
        'data': {},
    })
    # try:
    #     service = Service()
    #     service.debug(commands)
    #     return jsonify({
    #         'status': 0,
    #         'message': "ok.",
    #         'data': {},
    #     })
    # except Exception as error:
    #     return jsonify({
    #         'status': 500,
    #         'message': "server internal error.",
    #         'data': str(error),
    #     })
