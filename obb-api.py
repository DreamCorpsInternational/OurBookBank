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

from bson import json_util

json_mimetype = 'application/json'

# Routes. 

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
    app.run()
