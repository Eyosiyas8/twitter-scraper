import csv
from timeline_scraper_new import *
def scrape_replies(username, tweet_links):
    # file = open('../csv_files/twets_'+username+'.csv')
    tweet_data = []
    for tweet_link in tweet_links:
        reply_data = []
        print('the data is ',tweet_link)
        # print('tweet text is ',tweet_texts)
        # print('askdjf;lkasjdf;lakjsdf;ljasd;lkjfalkdsjflaksdjfaslkjdf;as',record)
        # print('askdjf;lkasjdf;lakjsdf;ljasd;lkjfalkdsjflaksdjfaslkjdf;as',record[1])
        # if username in twee
        driver.get(tweet_link)
        # Define the URL for the user's timeline
        # Find all the tweet elements on the page
        tweet_ids = set()
        # last_position = driver.execute_script('return window.pageYOffset;')
        scrolling = True
        x=0
        y=1800
        last_position = driver.execute_script('return window.pageYOffset;')
        print("NOT entered scrolling loop")
        while scrolling:
            print("entered scrolling loop")
            # wait = WebDriverWait(driver, 1)
            # element = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid = "tweet"]')))
            # print(len(element))
            
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            tweet_elements = soup.find_all('article', attrs={'data-testid': 'tweet'})
            print(len(tweet_elements))
            time.sleep(5)
            for tweet_element in tweet_elements:
                # print('tweet element ',tweet_element)
                dom = etree.HTML(str(tweet_element))
                tweet = scrape_user_timeline(username, dom)
                print('the tweet is ',tweet[6])
                if tweet and tweet[2] != None or tweet[4] != None:
                    tweet_id = ''.join(tweet)
                    if tweet_id not in tweet_ids:
                        tweet_ids.add(tweet_id)
                        if tweet[5] == 'None':
                            continue
                        else:
                            reply_data.append({
                    'username': tweet[0],
                    'name': tweet[1], 'tweet_id': tweet[2], 'tweet_link': tweet[3], 'conversation_id': tweet[4], 'date':tweet[5], 'tweet': tweet[6], 'image_link': tweet[7], 'hashtags': tweet[8], 'mentions': tweet[9], 'link': tweet[10],
                    'replies_count': tweet[11],
                    'retweets_count': tweet[12], 'likes_count': tweet[13], 'views_count': tweet[14],
                    'replies': [], 'reporting': {'is_reported': False, 'reporting_date': None, 'reported_by': None}})
            try:
                if len(reply_data) >= 0 and len(reply_data) < 10:
                    pass
                else:
                    break
            except:
                pass
            # while True:
                # check scroll position
            reply_scroll_attempt = 0
            print('Last position reply ',last_position)
            while True:
                try:
                    wait = WebDriverWait(driver, 3)
                    element = wait.until(EC.presence_of_element_located((By.XPATH, 'div[@class="css-18t94o4 css-1dbjc4n r-1777fci r-1pl7oy7 r-1ny4l3l r-o7ynqc r-6416eg r-13qz1uu"]')))
                    more_tweets = element.click()
                except:
                    pass    
                time.sleep(1)
                driver.execute_script('window.scrollTo({0}, {1});'.format(x, y))
                x+=1000
                y+=1000
                curr_position = driver.execute_script('return window.pageYOffset;')
                print('current position reply ', curr_position)
                if last_position == curr_position:
                    print('try scroll again')
                    reply_scroll_attempt+=1
                    print('scroll atempt is ',reply_scroll_attempt)

                    # end of scroll region
                    if reply_scroll_attempt >= 3:
                        print('scroll attempt reached 3 times')
                        scrolling = False
                        break
                    else:
                        time.sleep(2) # attempt to scroll again
                else:
                    last_position = curr_position
                    print('scrolling again ')
                    break
        # print('reply data ', type(reply_data), ' tweet data ', tweet_data)
        tweet_data.extend(reply_data)
    # print('this is all the tweet data',tweet_data)
    return tweet_data