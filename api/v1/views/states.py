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


@app_views.route('/states/', methods=['POST'])
def create_state():
    '''Creates a State'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    states.append(new_state.to_dict())
    return jsonify(states[0]), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_update(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
