import sys
import json

# Avoid failure to find flask module: 
sys.path.insert(0, "/Library/Python/2.7/site-packages")

from flask import Flask
app = Flask(__name__)

@app.route("/books")
def getBooks():
	result = dict()
	result["count"] = 3
	result["items"] = []
	result["items"].append(dict())
	result["items"][0]["title"] = "War and Peace"
	result["items"][0]["isbn"] = "91231221313121"
	result["items"][0]["author"] = "Leo Tolstoy"
	result["items"][0]["image"] = "http://fakeimages.com/war.png"

	result["items"].append(dict())
	result["items"][1]["title"] = "Crime and Punishment"
	result["items"][1]["isbn"] = "4353452342"
	result["items"][1]["author"] = "Fyodor Dostoevsky"
	result["items"][1]["image"] = "http://fakeimages.com/crime.png"

	result["items"].append(dict())
	result["items"][2]["title"] = "Pride and Prejudice"
	result["items"][2]["isbn"] = "9999999999"
	result["items"][2]["author"] = "Jane Austen"
	result["items"][2]["image"] = "http://fakeimages.com/pride.png"

	return json.dumps(result)

@app.route("/picks")
def getPicks():
	result = dict()
	result["count"] = 4
	result["items"] = []
	result["items"].append(dict())
	result["items"][0]["timestamp"] = 1417058455
	result["items"][0]["isbn"] = "91231221313121"
	result["items"][0]["context"] = "Donation" # one of possible values (enum type) 
	result["items"].append(dict())
	result["items"][1]["timestamp"] = 1417058457
	result["items"][1]["isbn"] = "91231221313121"
	result["items"][1]["context"] = "Donation" # one of possible values (enum type) 
	result["items"].append(dict())
	result["items"][2]["timestamp"] = 1417058461
	result["items"][2]["isbn"] = "91231545"
	result["items"][2]["context"] = "Donation" # one of possible values (enum type) 
	result["items"].append(dict())
	result["items"][3]["timestamp"] = 1417058461
	result["items"][3]["isbn"] = "4353452342"
	result["items"][3]["context"] = "Donation" # one of possible values (enum type) 

	return json.dumps(result)

if __name__ == "__main__":
	app.run()
