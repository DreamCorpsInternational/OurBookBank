import sys
import json

# Avoid failure to find flask module: 
sys.path.insert(0, "/Library/Python/2.7/site-packages")

from flask import Flask
app = Flask(__name__)

@app.route("/books")
def hello():
	result = dict()
	result["count"] = 100
	result["books"] = dict()
	result["books"][1] = "A book"
	result["books"][2] = "Another book"

	return json.dumps(result)

if __name__ == "__main__":
	app.run()
