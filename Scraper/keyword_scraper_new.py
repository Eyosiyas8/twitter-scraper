import json
import twint
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
import os
import pandas as pd
import time
# from login import *
from get_cookies import *
from sys import platform
# from colored import stylize
# import colored
from log import *
import re
import csv
from lxml import etree
import configparser
import requests
from bs4 import BeautifulSoup
           

def keyword_scraper(keyword, dom):
    image_link = []
    try:
        fullname = dom.xpath('.//span[@class="css-901oao css-16my406 css-1hf3ou5 r-poiln3 r-bcqeeo r-qvutc0"]/span')[0].text
        print(fullname)
        username = dom.xpath('.//div[@class="css-901oao css-1hf3ou5 r-14j79pv r-18u37iz r-37j5jr r-1wvb978 r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0"]/span')[0].text
        print(username)
        time.sleep(0.2)
        try:
            tweet_link = dom.xpath('.//div[@class="css-1dbjc4n r-18u37iz r-1q142lx"]/a')[0].attrib['href']
            tweet_link = 'https://www.twitter.com'+tweet_link
            tweet_id = tweet_link.split("/")[-1]
            print(tweet_id)
            print(type(tweet_id))
            print(tweet_link)
        except:
            tweet_link = ''
            tweet_id = ''
            print("Sponsored Content")
        try:
            if driver.current_url=="https://twitter.com/%s" % main_username:
                print('tweet_url '+driver.current_url)
                conversation_id = tweet_id
                print(conversation_id)
                print(type(conversation_id))
            else:
                print('reply_url '+driver.current_url)
                conversation_id = driver.current_url.split("/")[-1]
                print(conversation_id)
                print(type(conversation_id))
        except Exception as e:
            conversation_id = None
        try:
            post_date = dom.xpath('.//time')[0].attrib['datetime']
            print(post_date)
        except:
            NoSuchElementException
            post_date = ''
        # tweets = dom.xpath('.//div[@data-testid="tweetText"]')
        # tweet_text=''
        # for i in tweets:
        #     comment = dom.xpath(tweets+'/span'+'[i]')
        #     tweet_text+=comment
        tweet_text=''
        full_text = dom.xpath('.//div[@data-testid="tweetText"]')
        all_text = dom.xpath('.//div[@data-testid="tweetText"]/span')
        hashtag = dom.xpath('.//div[@data-testid="tweetText"]/span/a')
        external_link = dom.xpath('.//div[@data-testid="tweetText"]/a')
        mention = dom.xpath('.//div[@data-testid="tweetText"]/div/span/a')
        mentions = []
        hashtags = []
        external_links = []

        try:
            for i in range(10):
                time.sleep(0.1)
                print(range(len(full_text)))
                if all_text:
                    text = all_text[i].text            
                    tweet_text += text
                if hashtag:
                    text = hashtag[i].text 
                    hashtags.append(text)          
                    tweet_text += text
                if mention:
                    text = mention[i].text 
                    mentions.append(text)             
                    tweet_text += text
                if external_link:
                    text = external_link[i].text 
                    external_links.append(text)             
                    tweet_text += text
            print(tweet_text)
        except:
            pass
        profile_image = ''
        try:
            image_links = dom.xpath('.//div[@class="css-1dbjc4n r-1adg3ll r-1udh08x"]//img')
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
        try:
            reply_count = dom.xpath('.//span[@class="css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-1e081e0 r-qvutc0"]/span')[0].text
            print(reply_count)
        except:
            reply_count = ''
        try:
            retweet_count = dom.xpath('.//span[@class="css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-1e081e0 r-qvutc0"]/span')[1].text
            print(retweet_count)
        except:
            retweet_count = ''
        try:
            likes_count = dom.xpath('.//span[@class="css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-1e081e0 r-qvutc0"]/span')[2].text
            print(likes_count)
        except:
            likes_count = ''
        try:
            views_count = dom.xpath('.//span[@class="css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-1e081e0 r-qvutc0"]/span')[3].text
            print(views_count)
        except:
            views_count = ''
        # tweets.append(tweet_text)
    except:
        wait = WebDriverWait(driver, 1)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid = "app-bar-close"]'))).click()
    tweet = (fullname, username, tweet_id, str(tweet_link), str(conversation_id), post_date, tweet_text, json.dumps(list(image_link)), json.dumps(list(hashtags)), json.dumps(list(mentions)), json.dumps(list(external_links)), reply_count, retweet_count, likes_count, views_count)
    return tweet

time.sleep(1)
