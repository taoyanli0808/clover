
from flask import request
from flask import jsonify
from flask import Blueprint
from flask import render_template

from snippet.service import Service

snippet = Blueprint('snippet', __name__,
                    static_folder='static',
                    template_folder='templates',
                    url_prefix='/snippet')


@snippet.route('/create')
def create():
    return render_template("snippet.html")


@snippet.route('/api/v1/debug', methods=['POST'])
def api_v1_debug():
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
        result = service.debug(data)
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


@snippet.route('/api/v1/save', methods=['POST'])
def api_v1_save():
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
        result = service.save(data)
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
