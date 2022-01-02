import hashlib
from typing import List
from codeforces import CodeforcesAPI
import requests

data = {}
good_cache = {}
flat_cache = {}


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
    hash = hashlib.sha256("".join(handles).encode('utf-8')).digest()

    if hash in good_cache and hash in flat_cache:
        return good_cache[hash], flat_cache[hash]

    users = get_cf_users()

    lookup = {}
    for i, u in enumerate(users):
        lookup[u.handle.lower()] = 1

    good = []
    flat = []
    for h in handles:
        if h.lower() in lookup:
            good.append(h.lower())
            flat.append(h.lower())
        else:
            e = h.lower()

            resp = requests.head(
                "https://codeforces.com/profile/"+e, allow_redirects=False)
            url = resp.headers.get('Location')

            if url is None:
                good.append(None)
                flat.append(None)
                continue

            if "profile" in url:
                new_handle = url.split("/").pop()
                good.append((e.lower(), new_handle.lower()),)
                flat.append(new_handle.lower())

                print("resolved", e, "to", new_handle)
            else:
                good.append(None)
                flat.append(None)
                continue

    good_cache[hash] = good
    flat_cache[hash] = flat

    return good, flat
