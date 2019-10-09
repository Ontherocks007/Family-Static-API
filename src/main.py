"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
from models import Family

myFamily = Family('Doe')

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET', 'POST'])
def handle_person():

    if request.method == 'GET':
       response_body = {
           "members": myFamily.get_all_members(),
           "family_name": myFamily.last_name,
           "lucky_numbers": [],
           "sum_of_lucky": 1
       }
       return jsonify(response_body), 200

    if request.method == 'POST':
       body = request.get_json()
       if 'name' not in body:
           return 'You need to specify the first_name',400
       if 'age' not in body:
           return 'You need to specify the last_name', 400
       if 'gender' not in body:
           return 'You need to specify the last_name', 400
       if 'lucky_number' not in body:
           return 'You need to specify the last_name', 400
       response = myFamily.add_member (body)

       return jsonify(response), 200

@app.route('/members/<int:member_id>', methods=['GET', 'DELETE'])
def getlete_member(member_id):
    member=family.get_member(member_id)
    if request.method == 'GET':
        return jsonify(response_body), 400
    family.delete_member(member_id)
    if request.method == 'DELETE':
        return jsonify(response_body), 200

@app.route('/members/<int:member_id>', methods=['POST'])
def new_member(member_id):
    member=family.get_member(member_id)
    if request == 'POST':
        return jsonify(response_body), 400

# this only runs if `$ python src/main.py` is exercuted
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
