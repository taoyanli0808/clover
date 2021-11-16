#coding=utf-8

from flask import Blueprint

log = Blueprint('log', __name__)

from clover.log import views