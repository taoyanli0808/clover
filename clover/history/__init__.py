#coding=utf-8

from flask import Blueprint

statistics = Blueprint('history', __name__)

from clover.history import views
