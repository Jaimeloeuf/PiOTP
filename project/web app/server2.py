from passlib.hash import pbkdf2_sha256 as sha256
"""
Description:
Server that deals with the data visualization portion.
This web server / web service is designed to be server agnostic, and can run either on
the Pi itself or on an external VPS over the internet.

HTTP based RESTful API  (Only get and post methods are allowed):
GET:
    /	or	/index -> static html file of user home page created using the Jinja templating engine
    /login -> static html returned for user to enter data and submit form data
    /vis

POST:
    /login -> endpoint for posting username and password over to server for verification.

"""
# Dependencies
# Server dependencies
from flask import Flask, render_template, redirect, url_for, request, abort, jsonify
import db

# 'Global' object for Flask server
app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home_page():
    # Check if the user logged in already by looking for a valid JWT.
    # Use put user data into home page and send it back
    return render_template('./index.html', name=name)


# Server Route to test if remote server is online
@app.route('/ping', methods=['GET'])
def ping():
    # Default 200 status code will be sent back
    return

@app.route('/api/<command>/<args>', methods=['GET'])
def api():

    return


if __name__ == "__main__":
    # To get environmental variables avail to the process
    from os import environ
    # Use PORT from the environment if defined, otherwise default to 5000.
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)


    from multiprocessing import Process
    import mqtt_client
    Process(target=mqtt_client.start_sub).start()
    # Add the SIGINT handler to end/terminate the process when caught