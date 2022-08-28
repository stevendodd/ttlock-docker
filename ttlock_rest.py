from flask import Flask
from flask import request
import json
import requests
import time
import os
 
tokenExpiryTime = 0

def current_milli_time():
    return round(time.time() * 1000)

def get_token():
    global tokenExpiryTime
    if current_milli_time() > tokenExpiryTime:
        global clientId
        global accessToken
        global lockId

        clientId = os.environ['CLIENTID']
        lockId = os.environ['LOCKID']
        clientSecret = os.environ['CLIENTSECRET']
        user = os.environ['USER']
        password = os.environ['PASSWORD']
      
        data = {"client_id": clientId,
                "client_secret": clientSecret,
                "username": user,
                "password": password
                }
        response = requests.post("https://euapi.ttlock.com/oauth2/token", data)
            
        if response.status_code == 200:
            accessToken = response.json()["access_token"]
            tokenExpiryTime = int(response.json()["expires_in"])*1000 + current_milli_time() - 25000
        
def handle_users():
    get_token()
    response = requests.get("https://euapi.ttlock.com/v3/lockRecord/list?clientId=" + clientId + "&accessToken=" + accessToken + "&lockId=" + lockId + "&pageNo=1&pageSize=1&date=" + str(current_milli_time()))
    if response.status_code == 200:
        return(response.json())
    
def handle_unlock():  
    get_token()
    data = {"clientId": clientId,
            "accessToken": accessToken,
            "lockId": lockId,
            "date": current_milli_time()
        }
    
    response = requests.post("https://euapi.ttlock.com/v3/lock/unlock", data)
            
    if response.status_code == 200:
        return(response.json())


def request_lock():
    get_token()    
    response = requests.get("https://euapi.ttlock.com/v3/lock/detail?clientId=" + clientId + "&accessToken=" + accessToken + "&lockId=" + lockId + "&date=" + str(current_milli_time()))
         
    if response.status_code == 200:
        return(response.json())


app = Flask(__name__)

@app.route("/",methods = ['GET'])
def hello():
    return('stevendodd/TTLock')

@app.route("/<lock>/unlock",methods = ['POST', 'GET'])
def unlock(lock):
    return handle_unlock()

@app.route("/<lock>/users",methods = ['GET'])
def users(lock):
    return handle_users()

@app.route("/<lock>",methods = ['GET'])
def get_lock(lock):
    return request_lock()
