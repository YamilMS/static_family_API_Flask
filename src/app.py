"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#                                       GET METHOD
@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        jackson_family
    except NameError:
        return jsonify({'message': "NameError"}), 500
    else:
        members= jackson_family.get_all_members()
        return jsonify(members), 200

#                                       GET MEMBER THROUGH ID METHOD
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        jackson_family
    except NameError:
        return jsonify({'message': "NameError"}), 500

    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"message":"Member doesnt exist"}), 400


#                                       POST METHOD
@app.route('/members', methods=['POST'])
def add_member():
    try:
        jackson_family
    except NameError:
        return jsonify({'message': "NameError"}), 500
    
    member = request.get_json(force=True)
    jackson_family.add_member(member)
    return jsonify(member), 200
  


#                                       DELETE METHOD
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        jackson_family
    except NameError:
        return jsonify({'message': "NameError"}), 500

    if jackson_family.delete_member(id):
        return jsonify({"done": True}), 200
    else:
        return jsonify({"message":"Member doesn't exist"}),404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
