import logging
import sys

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
    log = logging.getLogger('werkzeug')
    requestDict = request.json
    # JSON is None if content type is not application/json.

    log.debug('The dict is: ' + str(requestDict))

    if requestDict is None:
        return Response("{\"message\":\"Incorrect content type header!\"}", mimetype=json_mimetype)

    user = requestDict["username"]
    authCode = requestDict["authcode"]

    pendingLogins = db.pending_logins
    pendingLogins.insert(requestDict)

    if user is None or authCode is None:
        return Response("{\"message\":\"Incorrect content!\"}", mimetype=json_mimetype)

    import os
    os.system("curl -s --user 'api:key-85ca8274209617fbef11d4a2a18f8e4d' https://api.mailgun.net/v2/sandboxa94ddc8c9b464a23bc258ea56fb53f7b.mailgun.org/messages -F from='Mailgun Sandbox <postmaster@sandboxa94ddc8c9b464a23bc258ea56fb53f7b.mailgun.org>' -F to='Jun <j.jun.luo@gmail.com>' -F subject='Mailgun TEST!!!!!' -F text='This is an email for da API'")

    os.system("curl -X POST 'https://api.twilio.com/2010-04-01/Accounts/AC8335feed73e8f0667b162bc638d14d22/Messages.json' -d 'From=+16475609905' -d 'To=+6473093872' -d 'Body=withoutquotes' -u AC8335feed73e8f0667b162bc638d14d22:f71a5272be1e942c449459f661b77b88")

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

    log.debug('The dict is: ' + str(requestDict))

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
    app.run(host='0.0.0.0') # Allow connections from outside the VM. 
