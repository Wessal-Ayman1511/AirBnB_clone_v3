#!/usr/bin/python3
"""
"""
from flask import Flask
from models import storage  # Import storage from models
from api.v1.views import app_views  # Import the Blueprint instance
import os
from flask import jsonify

app = Flask(__name__)

# Register the Blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Close storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ handles 404 errors """
    status = {"error": "Not found"}
    return jsonify(status), 404


if __name__ == "__main__":
    app.run(
        host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
        port=int(os.getenv('HBNB_API_PORT', 5000)),
        threaded=True
    )
