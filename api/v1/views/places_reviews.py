#!/usr/bin/python3
"""
View for Place Reviewthat handles all RESTful API actions
"""

from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_review_for_place(place_id):
    """Retrieves the list of all Place objects of a City"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Retrieves a Place object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Place object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id):
    """ handles POST method """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'user_id' not in data.keys():
        abort(400, "Missing user_id")
    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data.keys():
        abort(400, "Missing text")
    review = Review(**data)
    review.place_id = place_id
    review.save()
    review = review.to_dict()
    return jsonify(review), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def review_put(review_id):
    """ handles PUT method """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    review = review.to_dict()
    return jsonify(review), 200
