#!/usr/bin/python3
"""
View for States that handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def state_cities(state_id):
    # states_list = [state.to_dict()
    # for state in storage.all(State).values() if state.id == state_id]
    # if states_list == []:
    if not storage.get(State, state_id):
        abort(404)
    cities_list = [
        city.to_dict() for city in storage.all(City).values()
        if city.state_id == state_id
        ]
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", methods=['GET'])
def city_get(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def city_delete(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def city_create(state_id):
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")
    if not data.get('name'):
        abort(400, description="Missing name")
    data['state_id'] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201



@app_views.route("/cities/<city_id>", methods=['PUT'])
def city_update(city_id):
    if not request.is_json:
        abort(400, description="Not a JSON")
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
