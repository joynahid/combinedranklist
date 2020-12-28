import asyncio
import requests
import json
import sys
from robots.codeforces.utils.api_query import query, single_query
from robots.codeforces.model.structure import Contest, ProblemResults, Problems, Rows, Party, Member
from essentials.essen_func import toNamedTuple

class Codeforces:
    @staticmethod
    async def standings(contest_ids, handles=None):
        params = {
            'contestId': contest_ids
        }

        if handles is not None:
            params['handles'] = ';'.join(handles)

        responses = await query('contest.standings', params)

        # TODO Handle Exceptions for response

        batch_res = []

        for response in responses:
            response = response['result']

            contest = toNamedTuple(Contest, response['contest'])
            problems = [toNamedTuple(Problems, problem_dict) for problem_dict in response['problems']]

            for row in response['rows']:
                row['party']['members'] = [toNamedTuple(Member, member) for member in row['party']['members']]
                row['party'] = toNamedTuple(Party, row['party'])
                row['problemResults'] = [toNamedTuple(ProblemResults, problem_result) for problem_result in row['problemResults']]
            
            ranklist = [toNamedTuple(Rows, row_dict) for row_dict in response['rows']]

            batch_res.append((contest, problems, ranklist))

        return batch_res

    @staticmethod
    async def user_info(handles):
        params = {}
        if handles is not None: params['handles'] = ';'.join(handles)
        responses = await single_query('user.info', params)

        return responses