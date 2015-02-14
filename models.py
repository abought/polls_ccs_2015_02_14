"""Models to store and access data"""
__author__ = 'abought'

#redis_conn = redis.StrictRedis(host='localhost', port=6379)


# Quick hack for test application. Really, global variables are insane

KNOWN_POLLS = {}  # {uid: title}
VOTE_COUNTS = {}  # {uid: {choice:count}}

# dummy data to aid testing after reload
KNOWN_POLLS["dummy"] = "Sample poll"
VOTE_COUNTS["dummy"] = {"Parsley": 0,
                        "Sage": 0,
                        "Rosemary": 2,
                        "Thyme": 3}