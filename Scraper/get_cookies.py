import os
import pickle
import urllib.error
import random
import time
import chromedriver_autoinstaller
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from log import error_log

def login(driver, cookies):
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(e)
    driver.get("https://www.twitter.com/")  # Login URL
    time.sleep(2)
    try:
        wait = WebDriverWait(driver, 3)
        element = wait.until(EC.presence_of_element_located((By.XPATH, './/span[contains(text(), "You have reached the limit for seeing posts today. Subscribe to see more posts every day.")]')))
        return True  # Daily limit reached
    except:
        return False  # Login successful

chromedriver_autoinstaller.install()
options = Options()
driver = webdriver.Chrome(options=options)

my_list = ['cookies.pkl', 'cookies1.pkl']
num_selections = 1
cookie_selected = None

while not cookie_selected:
    new_list = random.sample(my_list, num_selections)
    joint_cookies = ', '.join(new_list)
    new_cookie = os.path.join(os.path.dirname(os.path.abspath(__file__)), joint_cookies)
    cookies = pickle.load(open(new_cookie, "rb"))
    driver.get("https://www.twitter.com/login")
    if login(driver, cookies):
        error_log('The session has reached the daily limit')
        my_list.remove(os.path.basename(new_cookie))  # Remove the selected cookie from the list
        if not my_list:
            break  # No more cookies to try
    else:
        cookie_selected = new_cookie  # Successful login, exit the loop

if cookie_selected:
    print("Successfully logged in with cookie:", cookie_selected)
else:
    print("Failed to log in with all cookies")

# login(driver, cookies)  # Close the WebDriver once done
