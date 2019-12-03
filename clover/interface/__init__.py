#coding=utf-8

from flask import Blueprint

interface = Blueprint('interface', __name__, url_prefix='/interface')

from clover.interface import views
