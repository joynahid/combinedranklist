import asyncio
import os, json
from robots.browser.browser import webDriver
from robots.atcoder.utils.db_query import atc_stands_saveto_db

def atc_standings(contests):
    browser = webDriver(1)[0]

    browser.get('https://atcoder.jp/login')

    browser.find_element_by_id("username").send_keys(os.environ.get('ATC_USERNAME'))
    browser.find_element_by_id("password").send_keys(os.environ.get('ATC_PASSWORD'))
    browser.find_element_by_id("submit").click()

    datas = []

    for contest_id in contests:
        browser.get(f'https://atcoder.jp/contests/{contest_id}/standings/json')

        print(browser.current_url)

        data = browser.find_elements_by_tag_name('pre')

        json_ranklist = {}
        for i in data:
            json_ranklist = json.loads(i.text)

        datas.append(json_ranklist)
        asyncio.create_task(atc_stands_saveto_db(contest_id, json_ranklist))
    
    browser.close()
    return datas