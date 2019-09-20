#!/usr/bin/env python


import json
import os
import requests
import datetime
from datetime import date
from datetime import timedelta
import request


import os
import time


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

from flask import Flask
from flask import request
from flask import make_response


# firebase
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://wesender2019.firebaseio.com',
    'storageBucket': 'https://wesender2019.appspot.com'
})

database = db.reference()
bucket = storage.bucket("wesender2019.appspot.com")
multiID=[]
multiAPI=[]

def divProcess(reportId):
    #check jika report id ada di dalam list
    if reportId in multiID:
        #menjalankan API
        index = multiID.index(reportId)
        service = multiAPI[index]
        return str(service)
    else:
        #menambah proses ke multi
        if len(multiID)<5:
            multiID.append(reportId)
            multiAPI.append(len(multiID))

            service=str(len(multiID))
            return str(service)
        else:
            #mengganti prioritas
            multiID.pop(0)
            multiAPI.append(multiAPI[0])
            multiAPI.pop(0)
            multiID.append(reportId)
            return str(multiAPI[len(multiAPI)-1])

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/get_barcode', methods=['POST'])
def get_barcode():
    try:
        userKey = str(request.headers["apikey"])+""
    except Exception as error:
        return "Error 404 Key Not Found"

    try:
        reportId = str(request.json["reportId"])+""
    except Exception as error:
        return "Error 404 reportId Not Found"

    #check firebase api key
    fireKey = database.child("userAPI").get()
    if userKey in fireKey:
        service = divProcess(reportId)
        URL = "https://api-gomamedia-wasender-s"+service+".herokuapp.com/"
        key = {
            "reportId":reportId
        }
        apikey = {
            "apikey" : userKey
        }
        return requests.post(headers=apikey ,url=URL+"get_barcode", data=key).text
    else:
        return "Error 401 Wrong Key"

@app.route('/send_message', methods=['POST'])
def send_message():  
    try:
        userKey = str(request.headers["apikey"])+""
    except Exception as error:
        return "Error 404 Key Not Found"

    try:
        reportId = str(request.json["reportId"])+""
    except Exception as error:
        return "Error 404 reportId Not Found"

    try:
        number = str(request.json["number"])+""
    except Exception as error:
        return "Error 404 number Not Found"

    try:
        message = str(request.json["message"])+""
    except Exception as error:
        return "Error 404 message Not Found"

    #check firebase api key
    fireKey = database.child("userAPI").get()
    if userKey in fireKey:
        service = divProcess(reportId)
        URL = "https://api-gomamedia-wasender-s"+service+".herokuapp.com/"
        keySend = {
                "reportId":reportId,
                "number":number,
                "message":message,
        }
        apikey = {
            "apikey" : userKey
        }
        
        #mengurangi limit
        limit = database.child("userAPI/"+userKey+"/limit").get() - 1
        database.child("userAPI/"+userKey).update({
            "limit":limit
        })
        return requests.post(headers=apikey ,url = URL+"send_message", data=keySend).text
    else:
        return "Error 401 Wrong Key"

@app.route('/send_report', methods=['POST'])
def send_report():
    try:
        userKey = str(request.headers["apikey"])+""
    except Exception as error:
        return "Error 404 Key Not Found"

    try:
        reportId = str(request.json["reportId"])+""
    except Exception as error:
        return "Error 404 reportId Not Found"

    try:
        email = str(request.json["email"])+""
    except Exception as error:
        return "Error 404 email Not Found"

    #check firebase api key
    fireKey = database.child("userAPI").get()
    if userKey in fireKey:
        service = divProcess(reportId)
        URL = "https://api-gomamedia-wasender-s"+service+".herokuapp.com/"
        keyReport = {
                "reportId":reportId,
                "email":email
        }
        apikey = {
            "apikey" : userKey
        }
        return requests.post(headers=apikey ,url = URL+"send_report", data  = keyReport).text
    else:
        return "Error 401 Wrong Key"

@app.route('/close', methods=['POST'])
def close():
    try:
        userKey = str(request.headers["apikey"])+""
    except Exception as error:
        return "Error 404 Key Not Found"

    try:
        reportId = str(request.json["reportId"])+""
    except Exception as error:
        return "Error 404 reportId Not Found"

    #check firebase api key
    fireKey = database.child("userAPI").get()
    if userKey in fireKey:
        service = divProcess(reportId)
        URL = "https://api-gomamedia-wasender-s"+service+".herokuapp.com/"
        keyClose = {
            "reportId":reportId
        }
        apikey = {
            "apikey" : userKey
        }
        return requests.post(headers=apikey ,url = URL+"close", data  = keyClose).text
    else:
        return "Error 401 Wrong Key"

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))

    print ("Starting app on port %d" %(port))

    app.run(debug=False, port=port, host='0.0.0.0')
