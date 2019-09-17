#!/usr/bin/env python


import json
import os
import requests
import datetime
from datetime import date
from datetime import timedelta
import request

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
import time

from io import BytesIO
from PIL import Image

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

apiKey = "6bef18936ac12a9096e9fe7a8fe1f878"

database = db.reference()
bucket = storage.bucket("wesender2019.appspot.com")

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/get_barcode', methods=['POST'])

#user request
#{
#	"key":"6bef18936ac12a9096e9fe7a8fe1f878",
#	"reportId":"test",
#	"email":"snorlak1999@gmail.com"
#}

def get_barcode():
    try:
        codeData = str(request.json["reportId"])+""
    except Exception as error:
        return "Error 404 reportId Not Found"

    try:
        email = str(request.json["email"])+""
    except Exception as error:
        return "Error 404 Email Not Found"

    try:
        userKey = str(request.json["key"])+""
    except Exception as error:
        return "Error 404 reportId Not Found"
    #validasi key
    if (userKey==apiKey):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3641.0 Safari/537.36')
            chrome_options.binary_location = GOOGLE_CHROME_PATH
            
            # Driver to open a browser
            driver = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

            #link to open a site
            driver.get("https://web.whatsapp.com/")
            time.sleep(1)
            png = driver.save_screenshot(codeData+".png")
            
            
            im = Image.open(codeData+".png")
            im = im.crop((430, 130, 720, 430))
            im.save(codeData+".png")

            today = date.today()
            today = str(today.strftime("%d/%m/%Y"))
            #push to firebase
            database.child("API/"+userKey+"/"+codeData).update({
                "date" : today,
                "email" : email
            })
            # push image to firebase
            blob = bucket.blob("API/"+userKey+"/"+codeData+".png")
            blob.upload_from_filename(codeData+".png")
            urlImg = "https://firebasestorage.googleapis.com/v0/b/wesender2019.appspot.com/o/API%2F"+userKey+"%2F"+codeData+".png?alt=media"
            os.remove(codeData+".png")
            return urlImg
        except Exception as error:
            return str(error)
    else:
        return "Error 401 Key Error"
    


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))

    print ("Starting app on port %d" %(port))

    app.run(debug=False, port=port, host='0.0.0.0')
