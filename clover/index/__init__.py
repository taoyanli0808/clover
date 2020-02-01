#coding=utf-8

from flask import Blueprint

index = Blueprint('index', __name__)

from clover.index import views