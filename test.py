
from robots.vjudge.utils.vjudge import *

# print(get_sec("01:10:56"))
id=['408262', '413583']
p=[None, '213']
handles = ['tahsin_1710006', 'joynahiid']

print(VjudgeContest.standings(id, p, handles))