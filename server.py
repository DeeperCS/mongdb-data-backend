#!/usr/bin/python
#coding:utf-8

from flask import Flask, url_for, request,make_response,jsonify, render_template
import os
import logging
import json
from werkzeug.security import generate_password_hash, check_password_hash

import db_utils

db = db_utils.get_db()

app = Flask(__name__)

def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response
app.after_request(after_request)

@app.route('/')
def index():
    # return "Hello, index"
    return render_template('index.html')

'''
/insert_user
{name:"xxx",
gender:"xxx",
age:"xxx"}
'''
@app.route('/insert_user', methods=['OPTIONS', 'POST', 'get'])
def insert_user():
    print("request.get_data():", request.get_data())
    # import pdb; pdb.set_trace()
    if request.method == 'OPTIONS':
        response = make_response()
    if request.method == 'POST':
        data =json.loads(request.get_data().decode('utf-8'))
        code = db_utils.insert_user(db, data)
        response = make_response(jsonify({'result': code}))
    return response


'''
/insert_urine_record
json:
{name:"xxx",
gender:"xxx",
age:"xxx",
urine_data:[
    {date:xxx,
    volulme:xxx},
    {date:xxx,
    volulme:xxx},
    ...
    ]
}
'''
@app.route('/insert_urine_record', methods=['OPTIONS', 'POST', 'get'])
def insert_urine_record():
    print("request.get_data():", request.get_data())
    # import pdb; pdb.set_trace()
    if request.method == 'OPTIONS':
        response = make_response()
    if request.method == 'POST':
        data =json.loads(request.get_data().decode('utf-8'))
        code = db_utils.insert_urine_record(db, data)
        response = make_response(jsonify({'result': code}))
    return response


'''
/get_record
json:
{data:[
    {name:"xxx",
    gender:"xxx",
    age:"xxx",
    diagnose:"xxx",
    urine_data:[
        {date:xxx,
        volulme:xxx},
        {date:xxx,
        volulme:xxx},
        ...
        ]
    },
    {name:"xxx",
    gender:"xxx",
    age:"xxx",
    diagnose:"xxx",
    urine_data:[
        {date:xxx,
        volulme:xxx},
        {date:xxx,
        volulme:xxx},
        ...
        ]
    },
    ...
]}

'''
@app.route('/get_record', methods=['OPTIONS', 'POST', 'get'])
def get_record():
    # import pdb; pdb.set_trace()
    if request.method == 'OPTIONS':
        response = make_response()
    if request.method == 'POST' or request.method == 'GET':
        data =json.loads(request.get_data().decode('utf-8'))
        code = db_utils.get_urine_record(db, data)
        response = make_response(jsonify({'result': code}))
    return response


'''
/set_diagnosis
json:
{
_id:"xxx",
diagnosis:"xxx",
}
'''
@app.route('/set_diagnosis', methods=['OPTIONS', 'POST', 'get'])
def set_diagnosis():
    # import pdb; pdb.set_trace()
    if request.method == 'OPTIONS':
        response = make_response()
    if request.method == 'POST':
        data =json.loads(request.get_data().decode('utf-8'))
        code = db_utils.set_diagnosis(db, data)
        response = make_response(jsonify({'result': code}))
    return response


if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    app.run(debug=True, host='0.0.0.0', port=6006, threaded=True)