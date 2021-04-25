#coding=utf-8

from flask import Blueprint

mock = Blueprint('mock', __name__)

from clover.mock import views