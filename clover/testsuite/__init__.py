#coding=utf-8

from flask import Blueprint

testsuite = Blueprint('testsuite', __name__)

from clover.testsuite import views