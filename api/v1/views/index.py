#!/usr/bin/python3
"""
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', methods=['GET'])
def status():
    """Return status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('stats', methods=['GET'])
def stats():
    """Return status of the API"""
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return jsonify(count_dict)
