#!/usr/bin/python3
"""sharing blueprints and making code modular"""

from flask import Blueprint
app_views = Blueprint('app_views', __name__)
from api.v1.views.index import *