"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import math
import random
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

users = [
    { "username": "user1", "password": "password", "id": "1"},
    { "username": "user2", "password": "passcode", "id": "2"}
]

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_user():
    json_text = jsonify(users)
    return json_text

    # return jsonify(response_body), 200

@app.route('/users', methods=['POST'])
def add_new_user():
    request_body = request.json 
    new_id = random.randint(3,999)
    request_body["id"] = new_id
    users.append(request_body)
    return jsonify(users)

@app.route('/users/<int:position>', methods=['PUT'])
def change_user(position):
    request_body = request.json
    users[position] = request_body
    return jsonify(users)

@app.route('/users/<int:position>', methods=['DELETE'])
def delete_user(position):
    print("This is the position to delete:", position)
    deleted = users.pop(position)
    return jsonify(deleted)


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
