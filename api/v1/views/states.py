#!/usr/bin/python3
"""
View for States that handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def states_all():
    """ returns list of all State objects """
    states_all = storage.all(State).values()
    state_list = [state.to_dict() for state in states_all]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_get(state_id):
    """
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    """
    empty_dict = {}
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """ handles POST method """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    state = state.to_dict()
    return jsonify(state), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_put(state_id):
    """ handles PUT method """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    state = state.to_dict()
    return jsonify(state), 200
