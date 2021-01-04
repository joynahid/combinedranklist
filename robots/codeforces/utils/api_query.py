import asyncio
import aiohttp
from robots.codeforces.utils.db_query import cf_stands_saveto_db

BASE_URL = 'https://codeforces.com/api/'

session = None

async def fetch(url, params, s):
    async with s.get(url, params= params) as response:
        res = await response.json()

        print(res)

        if res['status'] == 'FAILED':
            raise CodeforcesAPIError(res['comment'])

        return res

async def query(api_method, params = None):
    endpoint = BASE_URL + api_method

    responses = None

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in params['contestId']:
            new_params = {
                'contestId': i,
                'handles' : params['handles']
            }

            tasks.append(asyncio.create_task(fetch(endpoint, new_params, session)))
        try:
            responses = await asyncio.gather(*tasks)
        except CodeforcesAPIError:
            for task in tasks:
                task.cancel()
            pass

    return responses

async def single_query(api_method, params = None):
    endpoint = BASE_URL + api_method

    res = None

    async with aiohttp.ClientSession() as session:
        res = await fetch(endpoint, params, session)

    return res



class CodeforcesAPIError(Exception):
    def __init__(self, message):
        super().__init__('Codeforces API Error ' + message)