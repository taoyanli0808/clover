#coding=utf-8

from flask import Blueprint

report = Blueprint('report', __name__)

from clover.report import views