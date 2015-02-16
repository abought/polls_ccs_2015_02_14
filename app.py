"""
Very simple poll application: multiple users can vote
    and see results in real time
"""

from flask import Flask
from flask.ext import restful
from flask_debugtoolbar import DebugToolbarExtension

from flask.ext.socketio import SocketIO


app = Flask(__name__)
api = restful.Api(app)

app.config.from_object('settings')
toolbar = DebugToolbarExtension(app)
socketio = SocketIO(app)