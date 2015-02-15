"""
Very simple poll application: multiple users can vote
    and see results in real time
"""

import redis

from flask import Flask
from flask.ext import restful
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
api = restful.Api(app)

app.config.from_object('settings')
toolbar = DebugToolbarExtension(app)

# Use redis as data storage background for snappy live polling application
redis_conn = redis.StrictRedis(host='localhost', port=6379)

# TODO: Test each element of the polls class with a redis connection; make sure it works as expected
