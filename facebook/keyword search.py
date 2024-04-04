import sys
import time
import re 
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import StaleElementReferenceException
firefox_options = Options()
firefox_options.set_preference("dom.webnotifications.enabled", False)
client = MongoClient('mongodb://localhost:27017/')
db = client['facebook-data']
collection = db['keyword']
# Initialize the Firefox driver
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=firefox_options)

# chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.default_content_setting_values.notifications": 2}
# chrome_options.add_experimental_option("prefs", prefs)
LOGIN_URL = 'https://m.facebook.com/'
driver.get(LOGIN_URL)
# Enter email and password
email_element = driver.find_element('name', 'email')
email_element.send_keys('ethioact844@gmail.com')
password_element = driver.find_element('name', 'pass')
password_element.send_keys("Maru@#0184")
# Click the login button
login_button = driver.find_element(By.NAME, 'login')
login_button.click()
time.sleep(7)
# Wait for 2 seconds for the page to show up
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

keyword =''.join(sys.argv[1:])
link = "https://m.facebook.com/search/posts/?q="
link=link+keyword
driver.get(link)
time.sleep(3)
scroll_count = 0
while scroll_count < 2:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)  # Adjust this delay as needed
    scroll_count += 1
html_source= driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
beauty = BeautifulSoup(html_source, 'html.parser')
results = beauty.find("div", class_="x193iq5w x1xwk8fm")
urls = beauty.find_all("a", class_="x1i10hfl")
extracted_urls=[]
for url in urls:
    post_url=url.get("href")
    extracted_urls.append(post_url)
    
pfbid_pattern = re.compile(r"/posts/pfbid(?P<pfbid>\d+)")
fbid_pattern = re.compile(r"/photo/\?fbid=(?P<fbid>\d+)")
normal_page_post= set()
normal_poto_post= set()

for url_post in extracted_urls:
    pfbid_match = pfbid_pattern.search(url_post)
    fbid_match = fbid_pattern.search(url_post)
    if pfbid_match:
        normal_page_post.add(url_post)
    if fbid_match:
        normal_poto_post.add(url_post)
 
for url_post in normal_page_post:
    url_post=url_post.split('https://www.facebook.com')
    url_post=url_post[1]
    modified_url_post = "https://m.facebook.com"+url_post
    driver.get(modified_url_post)
    time.sleep(6)
    scroll_count = 0
    while scroll_count < 2:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)  # Adjust this delay as needed
        scroll_count += 1
    html_source= driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    single_url = BeautifulSoup(html_source, 'html.parser')
    extracted_header = ""
    extracted_time_value = ""
    extracted_message = ""
    results = single_url.find("div", class_="x1n2onr6 x1ja2u2z")
    if results is None:
        print("none")
    else:
        datas =results.find_all('div', class_="xu06os2 x1ok221b")
        
        time.sleep(3)
        if datas is None:
            print("none")
        else:
            for i, data in enumerate(datas):
                text = data.get_text(strip=True)
                if i == 0:
                    header = text
                    extracted_header+=header
                elif i == 1:
                    time_value = text
                    extracted_time_value+=time_value
                elif i == 2:
                    message = text
                    print(message)
                    extracted_message+=message
                else:
                    # Handle any additional cases or simply skip
                    pass
    profilei_image=""
    results = single_url.find('div', class_='x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a')
    if results and results.find('image'):
        image_url = results.find('image')
        image_url=image_url.get("xlink:href")
        print(image_url)
        profilei_image+=image_url
        
    else:
        # Handle case where no images are found
        print("No images found")
    
    extracted_image_urls = []
    results = single_url.find('div', class_='x1n2onr6', style="padding-top:calc(600% / 6)")
    time.sleep(3)
    # Check if results are not None and if there are any images found
    if results and results.find('img'):
        image_urls = results.find_all('img')
        time.sleep(3)
        for image_url in image_urls:
            post_image_url = image_url.get("src")
            extracted_image_urls.append(post_image_url)
    else:
        # Handle case where no images are found
        print("No images found")
        
    extracted_like_reactions = ""
    results = single_url.find('div', class_='x168nmei', attrs={'data-visualcompletion': "ignore-dynamic"})
    if results and results.find('span', class_="xt0b8zv"): # Corrected line
        reactions = results.find_all('span', class_="xt0b8zv") # Corrected line
        for i, reaction in enumerate(reactions):
            post_reaction = reaction.get_text(strip=True)
            if i==0:
                like= post_reaction
                print(like)
                extracted_like_reactions+=like
            else:
                # Handle any additional cases or simply skip
                pass
    else:
        # Handle case where no images are found
        print("No reactions found")
    
    comment_numbers=""
    shares=""
    results = single_url.find('div', class_='x168nmei', attrs={'data-visualcompletion': "ignore-dynamic"})
    if results and results.find('div', class_="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xg83lxy x1h0ha7o x10b6aqq x1yrsyyn"): # Corrected line
        Comments = results.find_all('div', class_="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xg83lxy x1h0ha7o x10b6aqq x1yrsyyn") # Corrected line
        for i,  comm in enumerate(Comments):
            Comment = comm.get_text(strip=True)
            if i == 0:
                comment_number = Comment
                comment_numbers+=comment_number
            elif i == 1:
                value=0
            elif i == 2:
                share_number = Comment
                print(share_number)
                shares+=share_number
            else:
                # Handle any additional cases or simply skip
                pass
            
    else:
        # Handle case where no images are found
        print("No reactions found")
     
    
    extracted_comment_reactions = []
    results = single_url.find('div', class_='x1gslohp')
    if results and results.find('span', class_="x193iq5w"): # Corrected line
        comments = results.find_all('span', class_="x193iq5w") # Corrected line
        for reaction in comments:
            comment = reaction.get_text(strip=True)
            extracted_comment_reactions.append(comment)
    else:
        # Handle case where no images are found
        print("No reactions found")
        
    post_data = {
        'keyword':keyword,
        'profile_image':profilei_image,
        'post_url':modified_url_post,
        'header': extracted_header,
        'time_value': extracted_time_value,
        'message': extracted_message,
        'image_urls': extracted_image_urls,
        'number_of_likes': extracted_like_reactions,
        'number_of_comments':comment_numbers,
        'number_of_shares':shares,
        'comment_reactions': extracted_comment_reactions
        # Add more fields as needed
    }
    post_id = collection.insert_one(post_data).inserted_id
    print("Post inserted with ID:", post_id)

driver.close()