''' Database Connection File '''

from datetime import datetime
import os
from random import choice
from string import ascii_letters

from pymongo.collection import Collection

from flask import Flask, request, Response
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError
from bson import json_util

from .model import Band


app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['JSON_SORT_KEYS'] = False
pymongo = PyMongo(app)

bands: Collection = pymongo.db.bands

@app.errorhandler(404)
def resource_not_found(error):
    """
    An error-handler to ensure that 404 errors are returned as JSON.
    """
    return json_util.dumps({'message': 'resource not found'}), 404


@app.errorhandler(DuplicateKeyError)
def duplicate_key_error(error):
    """
    An error-handler to ensure that MongoDB duplicate key errors are returned as JSON.
    """
    return json_util.dumps({'message': 'duplicate key error'}), 400


@app.route('/api/', methods=['POST'])
def create_band():
    """
    POST a new band into the database
    """
    while True:
        _id = ''.join(choice(ascii_letters) for _ in range(10))
        if not bands.find_one({'_id': _id}): break

    raw_data: dict = request.get_json()
    raw_data['data_registro'] = datetime.now()
    raw_data['_id'] = _id

    band = Band(raw_data)
    insertion = bands.insert_one(band.json())
    if insertion: response = json_util.dumps({'message': f'band created successfully with ID: {_id}'})

    return Response(response, mimetype='application/json')

@app.route('/api/', methods=['GET'])
def all_bands():
    """
    GET all bands from the database
    """
    response = json_util.dumps(bands.find())

    return Response(response, mimetype='application/json')

@app.route('/api/<string:_id>', methods=['GET'])
def get_band(_id):
    """
    GET a band from the database
    """
    response = json_util.dumps(bands.find_one({'_id': _id}))
    print(bands.find_one({'_id': _id})['nome'])

    return Response(response, mimetype='application/json')

@app.route('/api/<string:_id>', methods=['PUT'])
def update_band(_id):
    """
    PUT new information to update a existing band
    """
    raw_data: dict = request.get_json()
    raw_data['_id'] = _id
    raw_data['data_registro'] = bands.find_one({'_id': _id})['data_registro']

    band = Band(raw_data)

    update = bands.update_one({'_id': _id}, {'$set': band.json()})
    if update: response = json_util.dumps({'message': 'band updated successfully'})

    return Response(response, mimetype='application/json')


@app.route('/api/<string:_id>', methods=['DELETE'])
def delete_band(_id):
    """
    DELETE a existent band
    """
    deleted = bands.delete_one({'_id': _id})
    if deleted: response = json_util.dumps({'message': 'band deleted successfully'})

    return Response(response, mimetype='application/json')


if __name__ == '__main__':
    app.run()