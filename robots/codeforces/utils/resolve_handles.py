from typing import List
from codeforces import CodeforcesAPI

data = {}

class cache:
    @staticmethod
    def get(key):
        if key in data:
            return data[key]

    @staticmethod
    def set(key, d):
        data[key] = d

def get_cf_users():
    api = CodeforcesAPI()
    _cache_key = "user_rated_list"
    users = cache.get(_cache_key)

    if not users:
        users = api.user_rated_list()
        cache.set(_cache_key, users)

    return users

def filter_bad_handles(handles: List[str]):
    users = get_cf_users()

    lookup = {}
    for i, u in enumerate(users):
        lookup[u.handle.lower()] = u.handle.lower()

    for h in handles:
        if h.lower() in lookup:
            yield lookup[h]