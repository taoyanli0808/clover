
from flask import Blueprint

from clover.automation.service import Service

automation = Blueprint('automation', __name__, template_folder='templates')

from clover.automation import views
