#coding=utf-8

from flask import Blueprint

interface = Blueprint('interface', __name__)

from clover.interface import views
