
from flask import Blueprint

keyword = Blueprint('keyword', __name__)

from clover.keyword import views
