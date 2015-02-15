"""Models to store and access data"""
__author__ = 'abought'

import redis # TODO: Is there a way to make the connection pool more efficient?


class Poll(object):
    """Wrapper: access poll information from Redis backend

    Redis will store poll data in two places:
    - "poll_names" : a single redis hash of {uid: poll_title}
    - An individual redis hash (one per poll)
        comprised of {choice_label: vote_count}
    """
    def __init__(self):
        """Connect to redis as background (keeps long-polled demo snappy)"""
        self.redis = redis.StrictRedis(host='localhost', port=6379)

    def get_all_poll_titles(self):
        """Get all known polls as {uid:title}"""
        return self.redis.hgetall("poll_names")

    def get_poll_data(self, uid):
        """Get vote counts for one existing poll from uid, if the poll exists"""
        if not self.redis.hexists("poll_names", uid):
            return None

        #pipe = self.redis.pipeline()
        title = self.redis.hget("poll_names", uid)
        votes = self.redis.hgetall(uid)
        return {"title": title, "votes": votes}

    def make_poll(self, uid, title, choice_list):
        """Add the specified poll information to Redis"""
        pipe = self.redis.pipeline()

        # Add the poll name to the hash of known polls ({uid: title})
        pipe.hset("poll_names", uid, title)

        # Store the choices/ vote counts in a hash whose key is the poll ID
        for c in choice_list:
            pipe.hset(uid, c, 0)

        # TODO: make this return boolean for success..?
        return all(pipe.execute())

    def vote(self, uid, choice):
        """Vote on an existing poll and return the new count"""
        return self.redis.hincrby(uid, choice, 1)

