from collections import namedtuple

TaskInfo = namedtuple("TaskInfo", "Assignment TaskName TaskScreenName")
SolvedProblem = namedtuple(
    "SolvedProblem",
    "Count Failure Penalty Score Elapsed Status Pending Frozen Additional",
)
StandingsData = namedtuple(
    "StandingsData",
    "Rank Additional UserName UserScreenName UserIsDeleted Affiliation Country Rating OldRating IsRated IsTeam Competitions AtCoderRank TaskResults TotalResult",
)
TotalResult = namedtuple(
    "TotalResult", "Count Accepted Penalty Score Elapsed Frozen Additional"
)
