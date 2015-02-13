import logging
import sys
from configparser import ConfigParser

# Get configurable auth info.
config = ConfigParser()
config.readfp(open("obb.cfg"))

# Avoid failure to find flask module: 
sys.path.insert(0, '/Library/Python/2.7/site-packages')

from flask import Flask, Response, request
app = Flask(__name__)
app.debug = True

from pymongo import Connection
mc = Connection('localhost', 27017)
db = mc.obb
users = db.users
key = { "username" : "bob" }
data = { "phoneNumber" : "6473093872", "email" : "chris.brelski" }
users.update(key, data, True)

from bson import json_util

json_mimetype = 'application/json'

# Routes. 

@app.route('/auth', methods=['POST'])
def login():
#    log = logging.getLogger('werkzeug')
    requestDict = request.json
    # JSON is None if content type is not application/json.

    logging.debug('The dict is: ' + str(requestDict))

    if requestDict is None:
        return Response("{\"message\":\"Incorrect content type header!\"}", mimetype=json_mimetype)

    user = requestDict["username"]
    authCode = requestDict["authcode"]

    pendingLogins = db.pending_logins
    pendingLogins.insert(requestDict)

    if user is None or authCode is None:
        return Response("{\"message\":\"Incorrect content!\"}", mimetype=json_mimetype)

    import os

    # Twillio call.
    targetURI = config.get("twillioCredentials", "targetURI")
    fromNumber = config.get("twillioCredentials", "fromNumber")
    baCredentials = config.get("twillioCredentials", "basicAuthCredentials")
  
    body = "bla bla"
    toNumber = "+6473093872"

    curlCommand = "curl -X POST '" + targetURI + "' -d 'From=" + fromNumber + "' -d 'To=" + toNumber + "' -d 'Body=" + body + "' -u " + baCredentials

    logging.debug("Calling system command: " + curlCommand)
    os.system(curlCommand)

    usersCollection = db.users
    found = usersCollection.find({ 'username' : user})
    foundStuff = [f for f in found]
    found_json = json_util.dumps(foundStuff)

    #return Response("{\"message:\":\"Received user name and auth code succesfully: user is " + foundUsername + "\"}", mimetype=json_mimetype)
    return Response(found_json, mimetype=json_mimetype)

@app.route('/books')
def getBooks():
    booksCollection = db.books
    result = dict()
    books = booksCollection.find()
    result['count'] = books.count()
    result['items'] = [book for book in books]
    result_json = json_util.dumps(result)
    return Response(result_json, mimetype=json_mimetype)


@app.route('/books', methods=['POST'])
def addBook():
    log = logging.getLogger('werkzeug')
    requestDict = request.json
    # JSON is None if content type is not application/json.

    logging.debug('The dict is: ' + str(requestDict))

    if requestDict is None:
        return Response("{\"message\":\"Incorrect content type header!\"}", mimetype=json_mimetype)

    books = db.books
    books.insert(requestDict)

    # Required format: title, image, isbn, author

    return Response("{\"message:\":\"Created succesfully\"}", mimetype=json_mimetype)

@app.route('/picks')
def getPicks():
    picksCollection = db.picks
    result = dict()
    picks = picksCollection.find()
    result['count'] = picks.count()
    result['items'] = [pick for pick in picks]
    result_json = json_util.dumps(result)
    return Response(result_json, mimetype=json_mimetype)

if __name__ == "__main__":
    logging.basicConfig(filename='obb.log', level=logging.DEBUG)
    app.run(host='0.0.0.0') # Allow connections from outside the VM. 
