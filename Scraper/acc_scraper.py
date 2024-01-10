import json
import twint
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import os
import pandas as pd
import time
from sys import platform
# from colored import stylize
# import colored 
from log import *
import re
# from login import *
from get_cookies import *
import csv
from lxml import etree
import configparser
import requests
from bs4 import BeautifulSoup
def acc_info(dom):
    image_link = []
    # dom.xpath('//div[@class="css-1dbjc4n r-1awozwy r-1hwvwag r-18kxxzh r-1b7u577"]')[0].click
    time.sleep(1)
    try:
        fullname = dom.xpath('.//div[@class="css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1awozwy r-6koalj r-1udh08x r-3s2u2q"]/span/span')[0].text
        print(fullname)
    except:
        fullname = ''
    try:
        username = dom.xpath('.//span[contains(text(), "@")]')[0].text
        print(username)
    except:
        username = ''
    time.sleep(0.2)
    try:
        description = dom.xpath('.//div[@class="css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-1h8ys4a r-1jeg54m"]/span')[0].text
        if description == None:
            description = ''
        print(description)
    except:
        description = ''
    profile_image = ''
    try:
        image_links = dom.xpath('.//div[@class="css-175oi2r r-1mlwlqe r-1udh08x r-417010"]/img')
        for i in range(len(image_links)):  
            profile_image = image_links[0].attrib['src'] 
            image = image_links[i].attrib['src'] 
            if i==0 or 'profile_images' in image:
                continue             
            image_link.append(image)
        print(image_link)
    except:
        print(None)
        pass
        # tweets.append(tweet_text)
    account_info = (fullname, username, description, profile_image)
    return account_info
          
