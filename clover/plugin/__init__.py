
from flask import Blueprint

plugin = Blueprint('plugin', __name__)

from clover.plugin import views
