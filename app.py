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


from flask import Flask
from flask import request
from flask import make_response

import base64

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/start', methods=['POST'])
def start():
    try:
        link = str(request.json["link"])+""
    except Exception as error:
        return "Error 404 link Not Found"
    return link
    
    

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))

    print ("Starting app on port %d" %(port))

    app.run(debug=False, port=port, host='0.0.0.0')
