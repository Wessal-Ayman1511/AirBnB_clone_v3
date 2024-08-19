#!/usr/bin/python3
"""
View for Amenities that handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrieve the list of all users objects"""
    amenities = [
        user.to_dict()
        for user in storage.all(User).values()
        ]
    return jsonify(amenities)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_byID(user_id):
    """Retrieve a specific User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a specific user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    '''Creates an User'''
    if not request.get_json(silent=True):
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json(silent=True):
        abort(400, 'Missing email')
    if 'password' not in request.get_json(silent=True):
        abort(400, 'Missing password')
    users = []
    new_user = User(
        email=request.json['email'],
        password=request.json['password'])
    storage.new(new_user)
    storage.save()
    users.append(new_user.to_dict())
    return jsonify(users[0]), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a specific User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
