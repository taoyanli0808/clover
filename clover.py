#coding=utf-8

from flask import Flask
from flask import jsonify

from automation import automation

app = Flask(__name__)

app.register_blueprint(automation)


@app.route("/")
@app.route("/index")
def index():
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': {
            'author': "taoyanli0808",
            'introduce': "A Simple and Easy-to-Use Automated Testing Platform",
            'function': {
                'automation': {
                    'version': "0.1.00",
                    'dependence': "3.141.0",
                },
                'interface': {
                    'version': "0.0.00",
                    'requests': "2.18.3",
                }
            }
        }
    })


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=9999,
        debug=True
    )
