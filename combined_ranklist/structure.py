from collections import namedtuple
from essentials.essen_func import toNamedTuple

SameProblemResults = namedtuple(
    "ProblemResults",
    "index name problemDivision points pointsGained rejectedCount bestSubmissionTimeSeconds by",
    defaults=("", "", "", 0, 0, 0, 0),
)
UserInfo = namedtuple("UserInfo", "unique codeforces atcoder vjudge")
