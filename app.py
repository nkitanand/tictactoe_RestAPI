from flask import Flask, request
from gameLib import *
import json

app = Flask(__name__)

@app.route("/", methods=['GET'])
def intializeBoard():
    return initialJSON()
    
@app.route("/", methods=['POST'])
def runGame():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        jsonData = request.get_json()
        # Note that in the following function when JSON is passed
        # i.e, "jsonData" is automatically converted into python dictionary
        # before passing it as an argument. Hence, the function can 
        # directly manipulate jsonData as dict. Programmer need not
        # worry about converting data type from JSON to python Object i.e, dict
        newJsonData = updateGameState(jsonData)
        return newJsonData
    else:
        return 'Content-Type not supported!'