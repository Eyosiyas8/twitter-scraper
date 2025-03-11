import os
import pickle
import random
import time
import requests
import chromedriver_autoinstaller
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from log import error_log

def check_session(driver, cookies):
    # Check session by visiting a page that requires login and verifying elements
    driver.get("https://twitter.com/settings/account")
    time.sleep(2)  # Wait for the page to load

    # Verify the presence of a known element that indicates a logged-in state
    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-testid="AppTabBar_Home_Link"]')))  # Change XPath to a reliable element in the logged-in state
        return True
    except:
        return False

def load_cookies(file_path):
    try:
        with open(file_path, 'rb') as file:
            cookies = pickle.load(file)
            if not isinstance(cookies, list):
                raise ValueError("Cookies file should contain a list of cookie dictionaries.")
            return cookies
    except (OSError, pickle.UnpicklingError, ValueError) as e:
        print(f"Failed to load cookie file: {e}")
        return None

def login(driver, cookies):
    driver.get("https://twitter.com/login")  # Replace with actual login URL
    time.sleep(2)  # Wait for the login page to load

    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(2)  # Wait for the cookies to be applied and the page to reload

    return check_session(driver, cookies)

# def main():
chromedriver_autoinstaller.install()
options = Options()
options.add_argument('--headless')  # Uncomment to run headless
driver = webdriver.Chrome(options=options)

my_list = ['cookies.pkl', 'cookies1.pkl']
num_selections = 1
cookie_selected = None
max_retries = 3

while not cookie_selected and my_list:
    new_list = random.sample(my_list, num_selections)
    new_cookie_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), new_list[0])
    cookies = load_cookies(new_cookie_path)

    if not cookies:
        my_list.remove(new_list[0])  # Remove invalid cookie file from list
        continue

    for attempt in range(max_retries):
        if login(driver, cookies):
            cookie_selected = new_list[0]  # Successful login, exit the loop
            print(cookies)
            break
        else:
            print(cookies)
            print(f"Login attempt {attempt + 1} failed. Retrying...")
            time.sleep(2)

    if not cookie_selected:
        my_list.remove(new_list[0])  # Remove the selected cookie from the list
        if not my_list:
            break  # No more cookies to try

if cookie_selected:
    print("Successfully logged in with cookie:", cookie_selected)
else:
    print("Failed to log in with all cookies")


# if __name__ == "__main__":
#     main()
