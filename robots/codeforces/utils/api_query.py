import asyncio
import aiohttp
import logging
from robots.codeforces.utils.db_query import cf_stands_saveto_db

BASE_URL = "https://codeforces.com/api/"

session = None


async def fetch(url, params, s):
    async with s.get(url, params=params) as response:
        res = await response.json()
        return res


async def query(api_method, params=None):
    endpoint = BASE_URL + api_method

    responses = None

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in params["contestId"]:
            new_params = {"contestId": i, "handles": params["handles"]}
            tasks.append(asyncio.create_task(fetch(endpoint, new_params, session)))

        responses = await asyncio.gather(*tasks, return_exceptions=True)

    for each in responses:
        if "status" in each:
            if each["status"] == "FAILED":
                if "not found" in each["comment"]:
                    raise CFHandleNotFound(each["comment"])
        else:
            raise CodeforcesAPIError("Codeforces API Error")

    return responses


async def single_query(api_method, params=None):
    endpoint = BASE_URL + api_method

    res = None

    async with aiohttp.ClientSession() as session:
        res = await fetch(endpoint, params, session)

    if "status" in res:
        if res["status"] == "FAILED":
            if "not found" in res["comment"]:
                raise CFHandleNotFound(res["comment"])
    else:
        raise CodeforcesAPIError("Invalid Response from Codeforces")

    return res


class CodeforcesAPIError(Exception):
    def __init__(self, message):
        super().__init__("Codeforces API Error: " + message)


class CFHandleNotFound(Exception):
    def __init__(self, msg):
        super().__init__("Codeforces Handle Error: " + msg)