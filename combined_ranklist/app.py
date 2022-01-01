import asyncio
import logging
from typing import Any

from dataclasses import dataclass
from robots.codeforces.model.structure import ProblemResults
from robots.codeforces.utils.cf import Codeforces
from robots.atcoder.utils.atc import AtcoderContest
from robots.codeforces.utils.resolve_handles import filter_bad_handles
from robots.vjudge.utils.vjudge import VjudgeContest
from combined_ranklist.structure import SameProblemResults
from combined_ranklist.sheet_formatting import format_sheet
from collections import defaultdict, deque
from robots.gsheet.gservice_conf import drive_service, sheet_service
from robots.gsheet.google_sheet import retrieve, update
from essentials.essen_func import toNamedTuple
from quart import websocket

CF_DIVISIONS = ["div. 1", "div. 2", "div. 3", "div. 4"]

@dataclass
class UserInfo:
    unique: Any
    codeforces: Any
    vjudge: Any
    atcoder: Any


logging.basicConfig(
    filename="build_log.txt",
    level=logging.ERROR,
    format="%(levelname)s - %(asctime)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S",
)

logging.getLogger(__name__)


class CombRanklist:
    def __init__(self, **kwargs):
        self.contest_ids_cf = kwargs.get("contest_ids_cf", None)
        self.contest_ids_vj = kwargs.get("contest_ids_vj", None)
        self.contest_passwds_vj = kwargs.get("contest_ids_vj_passwords", None)
        self.contest_ids_atc = kwargs.get("contest_ids_atc", None)
        self.time_penalty = int(kwargs.get("time_penalty", 20 * 60))
        self.sheet_link = kwargs.get("sheet_link")
        self.sheet_range = kwargs.get("sheet_range", "A1:Z1000")
        self.up_sheet_link = kwargs.get("up_sheet_link", None)
        self.up_sheet_range = kwargs.get("up_sheet_range", "A1")
        self.unique_user_index = int(kwargs.get("unique_user_index", 1))
        self.cf_user_index = int(kwargs.get("cf_user_index", 0))
        self.atc_user_index = int(kwargs.get("atc_user_index", -5))
        self.vj_user_index = int(kwargs.get("vj_user_index", -5))
        self.handles = {}
        self.unique = dict(codeforces={}, atcoder={}, vjudge={})

        self.fetch_from_sheet()

        self.standings = {}
        for i in self.handles.unique:
            self.standings[i] = {}

        self.json_standings = {}

    def fetch_from_sheet(self):
        rows = []
        if self.sheet_link is not None:
            rows = retrieve(self.sheet_link, self.sheet_range, "COLUMNS")

        self.handles["codeforces"] = [x for x in filter_bad_handles([
            x.lower().strip() for x in rows[self.cf_user_index]
        ])]

        self.handles["unique"] = rows[self.unique_user_index]

        if self.atc_user_index >= 0:
            self.handles["atcoder"] = [
                x.lower().strip() for x in rows[self.atc_user_index]
            ]

        if self.vj_user_index >= 0:
            self.handles["vjudge"] = [
                x.lower().strip() for x in rows[self.vj_user_index]
            ]

        for i in range(len(self.handles["codeforces"])):
            key = self.handles["codeforces"][i]
            self.unique["codeforces"].update(
                {key: rows[self.unique_user_index][i]})

        for i in range(len(self.handles["atcoder"])):
            key = self.handles["atcoder"][i]
            self.unique["atcoder"].update(
                {key: rows[self.unique_user_index][i]})

        for i in range(len(self.handles["vjudge"])):
            key = self.handles["vjudge"][i]
            self.unique["vjudge"].update(
                {key: rows[self.unique_user_index][i]})

        self.handles = UserInfo(**self.handles)

    async def get_cf_standings(self):
        if len(self.contest_ids_cf):
            logging.info(
                f"Codeforces: Retrieving ranklist for {len(self.contest_ids_cf)} contests"
            )

            standings = await Codeforces.standings(
                self.contest_ids_cf, self.handles.codeforces
            )

            # print(standings)

            for each in standings:
                for row in each[2]:  # index of all_rows = 2
                    handle = row.party.members[0].handle.lower()
                    contestId = row.party.contestId
                    problemRes = []
                    contestTitle = each[0].name

                    for j in range(len(each[1])):
                        problemDivision = CF_DIVISIONS[1]

                        for d in CF_DIVISIONS:
                            if d in contestTitle.lower():
                                problemDivision = d.replace(" ", "").replace(
                                    ".", ""
                                )
                                break

                        problemRes.append(
                            SameProblemResults(
                                str(contestId) + " " + each[1][j].index,
                                each[1][j].name,
                                problemDivision,
                                each[1][j].points,
                                row.problemResults[j].points,
                                row.problemResults[j].rejectedAttemptCount,
                                row.problemResults[j].bestSubmissionTimeSeconds,
                                handle,
                            )
                        )

                    # mp[handle] = 1
                    self.standings[self.unique["codeforces"][handle]].update(
                        {contestId: {"problems": problemRes, "rank": row.rank}}
                    )

            # await self.filterCfHandles(mp)

    async def get_cf_maxrating(self):
        self.max_rating = {}
        data = await Codeforces.user_info(self.handles.codeforces)

        if "result" in data:
            for i in data["result"]:
                if "maxRating" in i:
                    self.max_rating[
                        self.unique["codeforces"][i["handle"].lower()]
                    ] = i["maxRating"]
                else:
                    self.max_rating[
                        self.unique["codeforces"][i["handle"].lower()]
                    ] = "Not Available"

    def get_atc_standings(self):
        standings = AtcoderContest.standings(
            self.contest_ids_atc, self.handles.atcoder
        )

        for e in standings:
            handle = e["UserScreenName"].lower()
            problemRes = []
            contestId = ""

            for task in e["TaskResults"]:
                contestId = task[3:-2]
                contestType = task[0:3]
                index = contestId + " " + task[-1:].upper()

                problemRes.append(
                    SameProblemResults(
                        index,
                        "Atcoder Problem " + task.capitalize(),
                        contestType,
                        None,
                        e["TaskResults"][task]["Score"] // 100,
                        e["TaskResults"][task]["Penalty"],
                        e["TaskResults"][task]["Elapsed"] // 1000000000,
                        handle,
                    )
                )

            self.standings[self.unique["atcoder"][handle]].update(
                {
                    "atc"
                    + str(contestId): {"problems": problemRes, "rank": e["Rank"]}
                }
            )

    def get_vj_standings(self):
        standings = VjudgeContest.standings(
            self.contest_ids_vj, self.contest_passwds_vj, self.handles.vjudge
        )

        for each in standings:
            for e in each["rows"]:
                handle = e["handle"].lower().strip()
                problemRes = []
                contestId = each["contestid"]
                rank = e["serial"]

                for task in e["problemResults"]:
                    contestType = "Vjudge"
                    index = "Vjudge X"

                    problemRes.append(
                        SameProblemResults(
                            index,
                            "Vjudge Problem",
                            contestType,
                            None,
                            task["score"],
                            task["rejectedCount"],
                            task["bestSubmissionTime"],
                            handle,
                        )
                    )

                if handle in self.unique["vjudge"]:
                    self.standings[self.unique["vjudge"][handle]].update(
                        {
                            "vj"
                            + str(contestId): {"problems": problemRes, "rank": rank}
                        }
                    )

    async def make_standings(self):
        if len(self.contest_ids_cf):
            await websocket.send(f"Retrieving codeforces ranklist ({len(self.contest_ids_cf)} contests)")
            await self.get_cf_standings()

        if len(self.contest_ids_atc):
            await websocket.send(f"Retrieving atcoder ranklist ({len(self.contest_ids_atc)} contests)")
            self.get_atc_standings()

        if len(self.contest_ids_vj):
            await websocket.send(f"Retrieving vjudge ranklist ({len(self.contest_ids_vj)} contests)")
            self.get_vj_standings()

        await websocket.send("Combining gathered standings")

        good_standings = self.standings

        for user in good_standings:
            solved, penalty, points = 0, 0, 0

            data_i = dict(problemStats={})
            data_i["ranks"] = []

            for contest in good_standings[user]:
                c_data = good_standings[user][contest]

                rnk = str(c_data["rank"]) + "th in " + str(contest)

                data_i["ranks"].append(rnk)

                # Iterate through each problems
                for i in c_data["problems"]:
                    if i.bestSubmissionTimeSeconds:  # If accepted
                        if i.pointsGained > 1:  # If points available
                            points += i.pointsGained
                        # add 1 to solved count
                        solved += int(bool(i.pointsGained))
                        key = i.problemDivision + "_" + i.index.split()[1]

                        if key not in data_i["problemStats"]:
                            data_i["problemStats"][key] = []
                        data_i["problemStats"][key].append(i._asdict())
                        penalty += (
                            i.bestSubmissionTimeSeconds
                            + i.rejectedCount * self.time_penalty
                        )  # Calculate Penalty for each problem independently

            data_i["totalSolved"] = solved
            data_i["totalPoints"] = points
            data_i["totalPenalty"] = penalty

            self.json_standings.update({str(user): data_i})

        return self.json_standings

    async def get_sheet_friendly_standings(self):
        await websocket.send("Getting codeforces max rating of contestants")

        without = ""

        try:
            await self.get_cf_maxrating()
        except Exception as e:
            await websocket.send("Failed to get max rating. " + str(e))
            without = " without codeforces max rating "

        all_divisions = {}

        await websocket.send("Generating sheet friendly standings" + without)

        for uniq in self.json_standings:
            for key in self.json_standings[uniq]["problemStats"]:
                all_divisions[key] = 1

        rows = deque(
            [
                deque(
                    ["", "", "", "", "", "", "Solve Counts on Different Categories"]
                    + ["" for i in all_divisions]
                ),
                deque(
                    [
                        "Rank",
                        "Contestants",
                        "Total Solved",
                        "Total Score",
                        "Total Penalty (s)",
                    ]
                    + [x.replace("_", " ").title() for x in all_divisions]
                    + ["Codeforces Max Rating", "Ranks in participated contests"]
                ),
            ]
        )

        row_data = deque([])
        for uniq in self.handles.unique:
            data = deque([uniq])
            data += [
                self.json_standings[uniq]["totalSolved"],
                self.json_standings[uniq]["totalPoints"],
                self.json_standings[uniq]["totalPenalty"],
            ]
            for i in all_divisions:
                if i in self.json_standings[uniq]["problemStats"]:
                    data.append(
                        len(self.json_standings[uniq]["problemStats"][i]))
                else:
                    data.append(0)

            data.append("")

            data += deque(self.json_standings[uniq]["ranks"])
            row_data.append(data)

        row_data = sorted(row_data, key=lambda x: x[3])
        row_data = sorted(row_data, key=lambda x: x[1], reverse=True)

        for i in range(len(row_data)):
            row_data[i].appendleft(i + 1)
        rows += row_data

        row_list = []

        for e in rows:
            l = list(e)
            row_list.append(l)

        return row_list

    async def dump_standings_to_sheet(self):
        sheet_standings = await self.get_sheet_friendly_standings()

        await websocket.send("Dumping standings to google sheet")

        _format = format_sheet(self.up_sheet_link)

        update(self.up_sheet_range, sheet_standings,
               self.up_sheet_link, _format)
