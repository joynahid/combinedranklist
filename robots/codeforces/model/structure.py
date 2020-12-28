from collections import namedtuple

Contest = namedtuple('Contest', 'id name type phase frozen durationSeconds startTimeSeconds relativeTimeSeconds')
Problems = namedtuple('Problems', 'contestId index name type points tags')
Rows = namedtuple('Rows', 'party rank points penalty problemResults')
Party = namedtuple('Party', 'contestId members participantType teamId teamName ghost room startTimeSeconds')
Member = namedtuple('Member', 'handle')
ProblemResults = namedtuple('ProblemResults', 'points penalty rejectedAttemptCount type bestSubmissionTimeSeconds', defaults=(0, 0, 0, None, 0))