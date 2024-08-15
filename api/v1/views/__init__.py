#!/usr/bin/python3
"""
"""

from flask import Blueprint

# Create the Blueprint instance
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import all view modules
from api.v1.views import index
