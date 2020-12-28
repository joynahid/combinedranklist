from robots.atcoder.utils.api_query import atc_standings
from essentials.essen_func import toNamedTuple
from robots.atcoder.utils.db_query import atc_stands_from_db

TO_SEC = 1000000000 # From atcoder inspection :p

class AtcoderContest:
    @staticmethod
    def standings(contests, handles):
        fast_query = {}

        for x in handles: fast_query[x] = 1

        batch_res = atc_stands_from_db(contests)

        not_found_cs = batch_res[1]
        not_found_res = []
        if len(not_found_cs):
            not_found_res = atc_standings(not_found_cs)

        batch_res = batch_res[0]

        if len(not_found_res):
            batch_res += not_found_res

        print(not_found_cs)

        relevant_res = []

        for contest in batch_res:
            for each in contest['StandingsData']:
                if each['UserScreenName'].lower() in fast_query:
                    relevant_res.append(each)

        return relevant_res