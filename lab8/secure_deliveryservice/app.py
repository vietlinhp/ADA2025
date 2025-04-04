import os

import requests
from flask import Flask, request, make_response, jsonify

from db import Base, engine
from resources.delivery import Delivery
from resources.status import Status

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/deliveries', methods=['POST'])
def create_delivery():
    if check_if_authorize(request) == 200:
        req_data = request.get_json()
        return Delivery.create(req_data)
    else:
        res = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(res)), 401


@app.route('/deliveries/<d_id>', methods=['GET'])
def get_delivery(d_id):
    if check_if_authorize(request) == 200:
        return Delivery.get(d_id)
    else:
        res = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(res)), 401


@app.route('/deliveries/<d_id>/status', methods=['PUT'])
def update_delivery_status(d_id):
    if check_if_authorize(request) == 200:
        status = request.args.get('status')
        return Status.update(d_id, status)
    else:
        res = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(res)), 401


@app.route('/deliveries/<d_id>', methods=['DELETE'])
def delete_delivery(d_id):
    if check_if_authorize(request) == 200:
        return Delivery.delete(d_id)
    else:
        res = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(res)), 401


def check_if_authorize(req):
    auth_header = req.headers['Authorization']
    if 'AUTH_URL' in os.environ:
        auth_url = os.environ['AUTH_URL']
    else:
        auth_url = 'http://userservice_ct:5000/verify'
    result = requests.post(auth_url,
                           headers={'Content-Type': 'application/json',
                                    'Authorization': auth_header})
    status_code = result.status_code
    print(status_code)
    print(result.json())
    return status_code


app.run(host='0.0.0.0', port=5000, debug=True)
