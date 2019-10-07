#coding=utf-8

from flask import jsonify
from flask import request
from flask import Blueprint
from flask import render_template

from interface.service import Service

interface = Blueprint('interface', __name__,
                      static_folder='static',
                      template_folder='templates',
                      url_prefix='/interface')


@interface.route('/')
@interface.route('/index')
def index():
    return render_template("interface.html")


@interface.route('/report/<run_id>')
def report(run_id):
    return render_template('interface/report.html')


@interface.route('/list')
def list():
    return render_template('list.html')


@interface.route('/api/v1/debug', methods=['POST'])
def api_v1_debug():
    # get请求使用request.values.to_dict接收
    # post、put、delete使用request.get_json接收
    data = request.get_json()

    method = data.get('method', None)
    if not method:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [method]',
            'data': data,
        })

    host = data.get('host', None)
    if not host:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [host]',
            'data': data,
        })

    try:
        status, message, data = Service().execute(data)
        return jsonify({
            'status': status,
            'message': message,
            'data': data,
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'data': data
        })


@interface.route('/api/v1/save', methods=['POST'])
def api_v1_save():
    # get请求使用request.values.to_dict接收
    # post、put、delete使用request.get_json接收
    data = request.get_json()

    method = data.get('method', None)
    if not method:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [method]',
            'data': data,
        })

    host = data.get('host', None)
    if not host:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [host]',
            'data': data,
        })

    try:
        case_id = Service().save(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': case_id,
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'data': data
        })


@interface.route('/api/v1/trigger', methods=['GET', 'POST'])
def api_v1_trigger():
    # 这里支持GET与POST请求，获取参数方法不同。
    if request.method == 'GET':
        data = request.values.to_dict()
    else:
        data = request.get_json()

    cases = data.get('cases', None)
    if not cases:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [cases]',
            'data': data,
        })

    try:
        result = Service().trigger(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result,
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'data': data
        })


@interface.route('/api/v1/report', methods=['GET', 'POST'])
def api_v1_report():
    # 这里支持GET与POST请求，获取参数方法不同。
    if request.method == 'GET':
        data = request.values.to_dict()
    else:
        data = request.get_json()

    run_id = data.get('run_id', None)
    if not run_id:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [run_id]',
            'data': data,
        })

    try:
        result = Service().report(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result,
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'data': data
        })


@interface.route('/api/v1/list', methods=['GET', 'POST'])
def api_v1_list():
    # 这里支持GET与POST请求，获取参数方法不同。
    if request.method == 'GET':
        data = request.values.to_dict()
    else:
        data = request.get_json()

    try:
        result = Service().list(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result,
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'data': data
        })
