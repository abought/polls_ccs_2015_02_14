"""Models to store and access data"""
__author__ = 'abought'

from app import redis_conn
# TODO: Is there a way to make the connection pool more efficient?


class Poll(object):
    """Wrapper: access poll information from Redis backend

    Redis will store poll data in two places:
    - "poll_names" : a single redis hash of {uid: poll_title}
    - An individual redis hash (one per poll)
        comprised of {choice_label: vote_count}
    """
    def get_all_poll_titles(self):
        """Get all known polls as {uid:title}"""
        return redis_conn.hgetall("poll_names")

    def get_poll_data(self, uid):
        """Get vote counts for one existing poll from uid, if the poll exists"""
        if not redis_conn.hexists("poll_names", uid):
            return None

        #pipe = redis_conn.pipeline()
        title = redis_conn.hget("poll_names", uid)
        votes = redis_conn.hgetall(uid)
        return {"title": title, "votes": votes}

    def make_poll(self, uid, title, choice_list):
        """Add the specified poll information to Redis"""
        pipe = redis_conn.pipeline()

        # Add the poll name to the hash of known polls ({uid: title})
        pipe.hset("poll_names", uid, title)

        # Store the choices/ vote counts in a hash whose key is the poll ID
        for c in choice_list:
            pipe.hset(uid, c, 0)

        # TODO: make this return boolean for success..?
        return all(pipe.execute())

    def vote(self, uid, choice):
        """Vote on an existing poll and return the new count"""
        return redis_conn.hincrby(uid, choice, 1)


poll_data = Poll()
print "pd in models mod", poll_data.get_all_poll_titles()

#
# KNOWN_POLLS = {}  # {uid: title}
# VOTE_COUNTS = {}  # {uid: {choice:count}}



# # dummy data to aid testing after reload
# KNOWN_POLLS["dummy"] = "Sample poll"
# VOTE_COUNTS["dummy"] = {"Parsley": 0,
#                         "Sage": 0,
#                         "Rosemary": 2,
#                         "Thyme": 3}