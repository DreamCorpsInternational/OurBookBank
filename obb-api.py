import sys

# Avoid failure to find flask module: 
sys.path.insert(0, '/Library/Python/2.7/site-packages')

from flask import Flask, Response
app = Flask(__name__)

from pymongo import Connection
mc = Connection('localhost', 27017)
db = mc.obb

from bson import json_util

json_mimetype = 'application/json'

@app.route('/books')
def getBooks():
    booksCollection = db.books
    result = dict()
    books = booksCollection.find()
    result['count'] = books.count()
    result['items'] = [book for book in books]
    result_json = json_util.dumps(result)
    return Response(result_json, mimetype=json_mimetype)

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

