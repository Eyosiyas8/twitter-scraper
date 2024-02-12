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
    repost = False
    image_link = []
    tweet_text = ''
    hashtags = []
    mentions = []
    external_links = []

    try:
        fullname = dom.xpath('.//div[@class="css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1awozwy r-6koalj r-1udh08x r-3s2u2q"]/span/span')[0].text
        print(fullname)
        username = dom.xpath('.//span[contains(text(), "@")]')[0].text
        print(username)
        time.sleep(0.2)
        try:
            repost = dom.xpath('.//span[contains(text(), " reposted")]')[0].text
            print(repost)
            repost = True
        except:
            repost = False

        try:
            tweet_link = dom.xpath('.//div[@class="css-175oi2r r-18u37iz r-1q142lx"]/a')[0].attrib['href']
            tweet_link = 'https://www.twitter.com' + tweet_link
            tweet_id = tweet_link.split("/")[-1]
            print(tweet_id)
            print(type(tweet_id))
            print(tweet_link)
        except:
            tweet_link = ''
            tweet_id = ''
            print("Sponsored Content")

        try:
            if driver.current_url == "https://twitter.com/%s" % username:
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
            post_date = 'None'
            print('Sponsored Content')

        # Extracting tweet content, hashtags, mentions, and external links
        full_text = dom.xpath('.//div[@data-testid="tweetText"]//span//text()')
        hashtag = dom.xpath('.//div[@data-testid="tweetText"]/span/a/text()')
        mention = dom.xpath('.//div[@data-testid="tweetText"]/div/span/a/text()')
        external_link = dom.xpath('.//div[@data-testid="tweetText"]/a/text()')

        # Constructing tweet text and collecting hashtags, mentions, and external links
        for text in full_text:
            tweet_text += text
        for tag in hashtag:
            hashtags.append(tag)
        for mention in mention:
            mentions.append(mention)
        for link in external_link:
            external_links.append(link)

        print(tweet_text)
        print(hashtags)
        print(mentions)
        print(external_links)

        # Extracting profile image links
        image_links = dom.xpath('.//div[@class="css-175oi2r r-1pi2tsx r-13qz1uu r-eqz5dr"]//img/@src')
        for i, link in enumerate(image_links):
            if i == 0 or 'profile_images' in link:
                continue
            image_link.append(link)

        print(image_link)

        # Extracting tweet engagement counts
        try:
            reply_count = dom.xpath('.//span[@data-testid="app-text-transition-container"]/span/span')[0].text
            print(reply_count)
        except:
            reply_count = ''

        try:
            retweet_count = dom.xpath('.//span[@data-testid="app-text-transition-container"]/span/span')[1].text
            print(retweet_count)
        except:
            retweet_count = ''

        try:
            likes_count = dom.xpath('.//span[@data-testid="app-text-transition-container"]/span/span')[2].text
            print(likes_count)
        except:
            likes_count = ''

        try:
            views_count = dom.xpath('.//span[@data-testid="app-text-transition-container"]/span/span')[3].text
            print(views_count)
        except:
            views_count = ''

        # Joining lists into comma-separated strings
        image_link_str = ', '.join(image_link)
        external_links_str = ', '.join(external_links)
        hashtags_str = ', '.join(hashtags)
        mentions_str = ', '.join(mentions)

        # Constructing the tweet tuple
        tweet = (
            fullname, username, tweet_id, tweet_link, conversation_id, post_date, 
            tweet_text, str(repost), image_link_str, hashtags_str, mentions_str, 
            external_links_str, reply_count, retweet_count, likes_count, views_count
        )

        return tweet

    except Exception as e:
        print("An error occurred:", e)
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid = "app-bar-close"]'))).click()

time.sleep(1)
