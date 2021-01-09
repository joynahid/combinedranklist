import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located


def webDriver(browser_instances):
    chrome_driver_path = os.environ["CHROME_DRIVER_PATH"]
    chrome_bin_path = os.environ["CHROME_BIN"]

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = chrome_bin_path

    web = []

    for i in range(browser_instances):
        web.append(
            webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
        )

    return web
