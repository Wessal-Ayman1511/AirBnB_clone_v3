#!/usr/bin/python3
"""
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Return status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('stats', methods=['GET'])
def stats():
    """Return status of the API"""
    from models.engine.db_storage import classes
    dic = {}
    for key, value in classes.items():
        dic[key] = storage.count(value)
    return jsonify(dic)
