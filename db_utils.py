#!/usr/bin/python
#coding:utf-8
import pymongo
from tables import *
import datetime, json
from datetime import timedelta,tzinfo
import numpy as np
from bson import ObjectId
import base64
import os
import shutil
import sys
import io
from werkzeug.security import generate_password_hash, check_password_hash
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATABASE_NAME = "urine"

table_name_user = "user"
table_name_urine_items = "urine_items"
table_name_record = "urine_record"


datapath = os.path.abspath(os.path.dirname(__file__))
ZERO_TIME_DELTA = timedelta(0)
LOCAL_TIME_DELTA = timedelta(hours=8)
class LocalTimezone(tzinfo):
    def utcoffset(self, dt):
        return LOCAL_TIME_DELTA

    def dst(self, dt):
        return ZERO_TIME_DELTA

    def tzname(self, dt):
        return '+08:00'
    pass
class JSONEncoder(json.JSONEncoder):
    """deal with ObjectId and datatime"""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return datetime.datetime.strftime(o, '%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, o)
    
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def get_db():
    client = pymongo.MongoClient(host="localhost", port=27017)
    # create database mancare if it dosent exist
    db = client[DATABASE_NAME]
    return db


'''
/insert_urine_record
json:
{
user_data:
{name:"xxx",
gender:"xxx",
age:"xxx"},
urine_data:
    [
        {
        date:xxx,
        urines:[
        {time:xxx, volume:xxx},
        {time:xxx, volume:xxx},
        {time:xxx, volume:xxx}]
        },
        {
        date:xxx,
        urines:[
        {time:xxx, volume:xxx},
        {time:xxx, volume:xxx},
        {time:xxx, volume:xxx}]
        },
        ...
    ]
}
'''
def insert_urine_record(db, data):
    # add a user
    user_id = db[table_name_user].insert_one(data['user_data']).inserted_id
    print("user_id:", user_id)
    # add many urine data records
    urine_data_id_list = []
    for data_item in data['urine_data']:
        urine_record_id = db[table_name_urine_items].insert_one(data_item).inserted_id
        urine_data_id_list.append(urine_record_id)
        print("urine_record_id:", urine_record_id)
    
    urine_record = {}
    urine_record['user_id'] = user_id
    urine_record['data_items'] = urine_data_id_list
    urine_record['diagnosis'] = ''
    urine_record['datetime'] = datetime.datetime.now()
    
    urine_diagnosis_id = db[table_name_record].insert_one(urine_record).inserted_id
    print("urine_diagnosis_id:", urine_diagnosis_id)
    return 'y'


'''
/set_diagnosis
json:
{
_id:"xxx",
diagnosis:"xxx",
}
'''
def set_diagnosis(db, data):
    query = {"_id":ObjectId(data["_id"])}
    new_values = {"$set":{"diagnosis":data["diagnosis"]}}
    records = db[table_name_record].update_one(query, new_values)

    return 'y'


'''
/get_urine_record
json (return):
[
    {'_id':xxx},
    {'user_id':xxx},
    {'data_items':[
                {"date":xxx, "volume":xxx}
             ]},
    {'diagnosis':xxx}
]
'''
def get_urine_record(db, data):
    # import pdb; pdb.set_trace()
    records = db[table_name_record].find().sort([("diagnosis",1), ("datetime",-1)])
    all_urine_record = []
    for record in records:
        data_item = {}
        user_data = db[table_name_user].find_one({"_id":record['user_id']},{"_id":0})
        
        urine_data = []
        for urine_id in record['data_items']:
            urine_item = db[table_name_urine_items].find_one({"_id":urine_id}, {"_id":0})
            urine_data.append(urine_item)  
            
        data_item['user_data'] = user_data
        data_item['urine_data'] = urine_data
        data_item['_id'] = str(record['_id'])
        data_item['diagnosis'] = record['diagnosis']
        data_item['datetime'] = record['datetime']
        all_urine_record.append(data_item)

    return all_urine_record
