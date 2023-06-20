from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import pickle


from selenium.webdriver.common.keys import Keys

import time
#from bs4 import BeautifulSoup
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
# Assigning a link to a webdriver

chromedriver_autoinstaller.install()
options = Options()
options.add_argument('--headless')
# chro_path = os.environ.get('CHROME_PATH')
driver = webdriver.Chrome(options=options)

driver.get("https://www.twitter.com/login")
print(driver.current_url)

print("Opening twitter account...")

basedir = os.path.dirname(os.path.abspath(__file__))
# account_info = os.path.join(basedir, '../Authentication/Account.txt')
#log in into an account

time.sleep(2)
new_cookie = os.path.join(basedir, 'cookies.pkl')
cookies = pickle.load(open(new_cookie, "rb"))
def login():
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(e)
    # pickle.dump(cookies, open('cookies.pkl', "wb"))
    driver.get("https://www.twitter.com/")
    time.sleep(2)
