
from flask import Blueprint

environment = Blueprint('environment', __name__, url_prefix='/environment')

from clover.environment import views
