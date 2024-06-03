import sys
import time
import re
import os
import datetime
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException

client = MongoClient('mongodb://localhost:27017/')
db = client['facebook-data']
collection = db['userscollections']
# Initialize the Firefox driver
# driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=firefox_options)
chromedriver_autoinstaller.install()
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")  # This line disables notifications
driver = webdriver.Chrome(options=chrome_options)
# Login to Facebook
LOGIN_URL = 'https://m.facebook.com/'
driver.get(LOGIN_URL)

email_element = driver.find_element(By.NAME, 'email')
email_element.send_keys('sofiyo2112@gmail.com')

password_element = driver.find_element(By.NAME, 'pass')
password_element.send_keys("Dunizi@#0102")

login_button = driver.find_element(By.NAME, 'login')
login_button.click()
time.sleep(7)
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'list_user.txt')
# file_path = 'list_post.txt'  # Replace with the actual path to your text file
with open(file_path, 'r') as file:
    for line in file:
        try:
            osint_user_id = line.split(" ")[1]
        except:
            osint_user_id = "Anonymous"
        url = "https://m.facebook.com/"+line.split(" ")[0]
        driver.get(url)
        time.sleep(3)
        scroll_count = 0
        while scroll_count < 6:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)
            scroll_count += 1

        # Parse HTML source
        html_source = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        beauty = BeautifulSoup(html_source, 'html.parser')
        results = beauty.find_all("div", class_="x78zum5 x1n2onr6 xh8yej3")

        # Extract post data
        for result in results:
            post_data = {}

            post_channel_element = result.find("div", class_="xu06os2 x1ok221b")
            if post_channel_element:
                post_channel = post_channel_element.text.strip()
                post_data['post_channel'] = post_channel
            results_element = result.find('div', class_='x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a')
            if results_element and results_element.find('image'):
                image_url = results_element.find('image').get("xlink:href")
                post_data['image_url'] = image_url
            title_element = result.find("strong")
            if title_element:
                title = title_element.text.strip()
                post_data['title'] = title
                
            results = result.find_all("a", class_="x1i10hfl")       
            pattern = "https://www.facebook.com/INSA.ETHIOPIA/posts"
            links = [result.get('href') for result in results if result and result.get('href') and result.get('href').startswith(pattern)]
            for p_url in links:
                post_data['p_url'] = p_url
                print(post_data['p_url'])
            result_time = result.find("div", class_="x78zum5 xdt5ytf xz62fqu x16ldp7u")
            if result_time is None:
                print("No time data found")
            else:
                datas = result_time.find_all('div', class_="xu06os2 x1ok221b")
                if datas:  # Check if datas is not empty
                    for i, data in enumerate(datas):
                        text = data.get_text(strip=True)
                        print(text)
                        if i == 0:
                            post_data['header'] = text                   
                        elif i == 1:                   
                            post_data['time_value']=text
                            print(post_data['time_value'])
                        elif i == 2:
                            post_data['message'] = text        
                       
                        else:
                            # Handle any additional cases or simply skip
                            pass
                else:
                    print("No data found in result_time")

            p_data_element = result.find("div", class_="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a")
            if p_data_element:
                p_data = p_data_element.text.strip()
                post_data['p_data'] = p_data

            p_image_element = result.find('img')
            if p_image_element:
                p_image = p_image_element.get("src")
                post_data['p_image'] = p_image

            # Extract reactions
            new_reaction = result.find('div', class_='x168nmei', attrs={'data-visualcompletion': "ignore-dynamic"})
            if new_reaction and new_reaction.find('span', class_="xt0b8zv"):
                reactions = new_reaction.find_all('span', class_="xt0b8zv")
                for i, reaction in enumerate(reactions):
                    post_reaction = reaction.get_text(strip=True)
                    if i == 0:
                        post_data['like'] = post_reaction

            # Extract comments
            comments = result.find('div', class_="x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x1qjc9v5 xozqiw3 x1q0g3np xykv574 xbmpl8g x4cne27 xifccgj")
            if comments:
                comments = comments.find_all('span', class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa")
                for i, comm in enumerate(comments):
                    comment = comm.get_text(strip=True)  
                    if i == 0:
                        post_data['comment_number'] = comment                              
                    elif i == 1:
                        post_data['share_number'] = comment
            post_data['date_of_scraping'] =  datetime.datetime.today()
            post_data['osint_user_id'] = osint_user_id      
            # Insert post data into MongoDB
            if 'post_channel' in post_data and 'title' in post_data:
                post_id = collection.insert_one(post_data).inserted_id
                print("Post inserted to MongoDB with ID:", post_id)
            else:
                print("Skipped inserting post data to MongoDB due to missing post_channel or title")

# Close the browser
driver.quit()