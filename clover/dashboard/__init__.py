#coding=utf-8

from flask import Blueprint

dashboard = Blueprint('dashboard', __name__)

from clover.dashboard import views
