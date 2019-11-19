
# from flask import request
# from flask import jsonify
from flask import Blueprint
from flask import render_template

snippet = Blueprint('snippet', __name__,
                    static_folder='static',
                    template_folder='templates',
                    url_prefix='/snippet')


@snippet.route('/create')
def create():
    return render_template("snippet.html")
