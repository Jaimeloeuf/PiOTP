"""
Description:
Code for IOTP Project

API  (Only get and post methods are allowed):
GET:
	/	or	/index -> static html file of user home page created using the Jinja templating engine
	/login -> static html returned for user to enter data and submit form data

POST:
	/login -> endpoint for posting username and password over to server for verification.

"""
# Dependencies
# Server dependencies
from flask import Flask, render_template, request, abort, jsonify

# 'Global' object for Flask server
app = Flask(__name__)

# Flask server routes
@app.route('/', methods=['GET'])
def home_page():
    # Use templating engine to put user data into the home page and send it back
    return render_template('./index.html')

# Flask Route to mimic pressing the button
@app.route('/login', methods=['POST'])
def login():
	checkPasswd()

# Server Route to test if remote server is online
@app.route('/ping', methods=['GET'])
def ping():
	# Set status code to 200 and end response.
	return 200
	
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)