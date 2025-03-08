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
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from log import error_log

# Set Chrome binary path for Docker
CHROME_BINARY_PATH = "/usr/bin/google-chrome-stable"  # Ensure Selenium finds Chrome in Docker
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"  # Ensure correct ChromeDriver path

def check_session(driver, cookies):
    """Check if session is valid by verifying the presence of a logged-in element."""
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
    """Load cookies from a pickle file."""
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
    """Log in to Twitter using stored cookies."""
    driver.get("https://twitter.com/login")  # Replace with actual login URL
    time.sleep(2)  # Wait for the login page to load

    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(2)  # Wait for the cookies to be applied and the page to reload

    return check_session(driver, cookies)

# Auto-install ChromeDriver
chromedriver_autoinstaller.install()

# Set up Chrome options
options = Options()
options.binary_location = CHROME_BINARY_PATH  # Explicitly set the Chrome binary path
options.add_argument('--headless')  # Uncomment to run headless
options.add_argument('--no-sandbox')  # Required for Docker
options.add_argument('--disable-dev-shm-usage')  # Prevent crashes due to limited /dev/shm space

# Initialize WebDriver with explicit ChromeDriver path
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# List of cookie files to try
my_list = ['cookies.pkl', 'cookies1.pkl']
num_selections = 1  # Number of cookies to randomly select
cookie_selected = None
max_retries = 3  # Number of retries per cookie file

# Attempt to log in with available cookies
while not cookie_selected and my_list:
    new_list = random.sample(my_list, num_selections)  # Randomly select a cookie file
    new_cookie_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), new_list[0])
    cookies = load_cookies(new_cookie_path)

    if not cookies:
        my_list.remove(new_list[0])  # Remove invalid cookie file from list
        continue

    # Try logging in with the selected cookie
    for attempt in range(max_retries):
        if login(driver, cookies):
            cookie_selected = new_list[0]  # Successful login, exit the loop
            print(f"Successfully logged in using cookies from: {cookie_selected}")
            break
        else:
            print(f"Login attempt {attempt + 1} failed. Retrying...")
            time.sleep(2)

    if not cookie_selected:
        my_list.remove(new_list[0])  # Remove the selected cookie from the list
        if not my_list:
            break  # No more cookies to try

# Print login status
if cookie_selected:
    print("Successfully logged in with cookie:", cookie_selected)
else:
    print("Failed to log in with all cookies")

# Close WebDriver to free resources
driver.quit()