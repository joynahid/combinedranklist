import asyncio
import os, json
from robots.browser.browser import webDriver
from bs4 import BeautifulSoup
from robots.vjudge.utils.db_query import vj_stands_saveto_db

def get_sec(str):
    ret=int(str[0:2])*60*60
    ret+=int(str[3:5])*60
    ret+=int(str[6:8])
    return ret

def vjudge_standings(contests, contest_passwords):
    browser = webDriver(1)[0]

    browser.get('https://vjudge.net/')

    browser.implicitly_wait(1)

    browser.find_element_by_css_selector('#navbarResponsive > ul > li:nth-child(8) > a').click()
    browser.find_element_by_id("login-username").send_keys(os.environ.get('VJUDGE_USERNAME'))
    browser.find_element_by_id("login-password").send_keys(os.environ.get('VJUDGE_PASSWORD'))
    browser.find_element_by_id("btn-login").click()

    datas = []

    for k in range(0, len(contests)):
        browser.get(f'https://vjudge.net/contest/{contests[k]}#rank')
        
        if len(contest_passwords[k]):
            try:
                chk = browser.find_element_by_id("contest-login-password")
                chk.send_keys(str(contest_passwords[k]))
                browser.find_element_by_id("btn-contest-login").click()
            except Exception as e:
                pass
        
        source = browser.page_source
        
        soup = BeautifulSoup(source, 'html.parser')

        title = soup.select('title')[0].text
        author = soup.select('#contest-manager > a')[0].text
        query = '#contest-rank-table > thead:nth-child(2) > tr:nth-child(1) > th'
        numOfProblems = len(soup.select(query))-4

        fetchRank = soup.find_all("td", {'class': ["meta", "prob"]})

        ranks = []


        for i in range(0,len(fetchRank), numOfProblems+4):
            p = []
            
            for j in range(numOfProblems+4):
                p.append(fetchRank[i].text)
                i+=1

            data = {
                'serial' : int(p[0]),
                'handle' : p[1].split(' ')[0],
                'solved' : int(p[2]),
                'penalty' : int(p[3].split(' ')[1].strip())
            }
            problem_result=[]

            for j in range(4, numOfProblems+4):
                if p[j]=='\xa0':
                    continue
                x=0
                if p[j][-1]==')':
                    x=int(p[j][-2:-1])

                if p[j][2] == ':':
                    problem_result.append({
                        'problemId': chr(ord('A')+(j-4)),
                        'score' : 1,
                        'bestSubmissionTime' : int(get_sec(p[j])),
                        'rejectedCount': x
                    })

            data['problemResults']=problem_result

            ranks.append(data)
        
        ret = {
            'contestid' : contests[k],
            'title' : title,
            'author' : author,
            'numOfProblems': numOfProblems,
            'rows' : ranks
        }
        
        datas.append(ret)        
        asyncio.create_task(vj_stands_saveto_db(contests[k], ret))

    browser.close()
    return datas