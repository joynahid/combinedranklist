from robots.vjudge.utils.api_query import vjudge_standings
from essentials.essen_func import toNamedTuple
from robots.vjudge.utils.db_query import vj_stands_from_db

TO_SEC = 1000000000 # From atcoder inspection :p

class VjudgeContest:
    @staticmethod
    def standings(contests, contest_passwords, handles):
        try:
            fast_query = {}

            for x in handles: fast_query[x] = 1

            batch_res = vj_stands_from_db(contests)

            not_found_cs = batch_res[1]
            not_found_contests = []
            not_found_res = []
            not_found_cs_pass = []

            for i in not_found_cs:
                not_found_cs_pass.append(contest_passwords[i])
                not_found_contests.append(contests[i])

            print(not_found_contests, not_found_cs_pass)

            if len(not_found_cs):
                not_found_res = vjudge_standings(not_found_contests, not_found_cs_pass)

            batch_res = batch_res[0]

            if len(not_found_res):
                batch_res+=not_found_res

            print(batch_res)
            
            relevant_res = []

            for contest in batch_res:
                rows = []
                for c in contest['rows']:
                    if c['handle'].lower().strip() in fast_query:
                        rows.append(c)

                data = {
                    'contestid': contest['contestid'],
                    'title': contest['title'],
                    'author': contest['author'],
                    'numOfProblems': contest['numOfProblems'],
                    'rows': rows
                }

                relevant_res.append(data)

            return relevant_res
        except Exception as e:
            print('VJUDGE API ERROR', e)