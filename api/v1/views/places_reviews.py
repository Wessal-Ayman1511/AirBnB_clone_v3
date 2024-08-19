#!/usr/bin/python3
"""
View for States that handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route("places/<place_id>/reviews", methods=['GET'])
def place_reviews(place_id):
    if not storage.get(Place, place_id):
        abort(404)
    review_list = [
        review.to_dict() for review in storage.all(Review).values()
        if review.place_id == place_id
        ]
    return jsonify(review_list)


@app_views.route("reviews/<review_id>", methods=['GET'])
def review_get(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("reviews/<review_id>", methods=['DELETE'])
def review_delete(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/reviews', methods=['POST'])
@app_views.route('places/<place_id>/reviews/', methods=['POST'])
def create_review(place_id):
    '''Creates a City'''
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    user_obj = storage.get("User", data['user_id'])
    if user_obj is None:
        abort(404)
    new_review = Review(place_id=place_id, user_id=data['user_id'], text=data['text'])
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def updates_review(review_id):
    '''Updates a Review object'''
    all_reviews = storage.all("Review").values()
    review_obj = [obj.to_dict() for obj in all_reviews if obj.id == review_id]
    if review_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'text' in request.get_json():
        review_obj[0]['text'] = request.json['text']
        for obj in all_reviews:
            if obj.id == review_id:
                obj.text = request.json['text']
        storage.save()
    return jsonify(review_obj[0]), 200
