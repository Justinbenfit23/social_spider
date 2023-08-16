# side note: a digital data vending machine is honestly probably the best business to start. Be the guy selling shovels. 
# first download browsermob proxy
# then use playwright to login to twitter
# then setup browsermob with this: https://www.youtube.com/watch?v=r0ne6zrqVaQ to run a playwright or selenium driver and search hashtags or influencer timelines on twitter then scroll and extract the har files to json. Do first to get training data then keep going to continually have data to make predictions on.
#scrape discord groups as well

from playwright.sync_api import sync_playwright, expect
from scrapy.crawler import CrawlerProcess
import scrapy

import pandas as pd
import re
from datetime import datetime
import random
import os
from dotenv import load_dotenv

load_dotenv()

# Get the absolute path of the directory of the script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Create the absolute path to the 'data' directory
data_path = os.path.join(dir_path, 'data')
followers_scroll_filename = data_path + '/followers_scroll.csv'
hrefs_master = data_path + '/hrefs_master.csv'

import time
from pprint import pprint
# from playwright.sync_api import sync_playwright
import json


CHROMIUM_ARGS = [
    '--no-sandbox'
    ,'--disable-setuid-sandbox'
    ,'--no-first-run'
    ,'--disable-blind-features=AutomationControlled'
]

class TwitterScraper(scrapy.Spider):
    name = 'twitter'
    allowed_domains = ['twitter.com']
    start_urls = ['https://twitter.com/cryptoanalyst27/following']

    def __init__(self, *args, **kwargs):
        super(TwitterScraper, self).__init__(*args, **kwargs)

    def start_requests(self):
        max_tries = 3
        count = 0
        num_count = 1

        print('creating new context...')

        try: 
            with sync_playwright() as playwright:
                self.playwright = playwright
                context = self.playwright.chromium.launch_persistent_context(user_data_dir='./userdata/',channel='chrome',headless=False,slow_mo=50)#,args=CHROMIUM_ARGS, ignore_default_args=['--enable-automation'])
                page = context.new_page()
                page.goto(self.start_urls[0],timeout=0)
                self.process_loop(context, page)
                
                    
        except Exception as e:
            raise e
            # print('Exception in start_requests try starting at line 58: {}'.format(e))
            # count += 1
            # time.sleep(random.randint(3,5))
            # print('Trying driver.get_url again...')
            # if count > max_tries:
            #     loop = False
            #     break

    def process_loop(self, context, page):
        context_first_pass = True
        loop = True
        element_exists = True

        while loop:
            if context_first_pass:
                context_first_pass = False
            else:
                browser_instance = self.playwright.chromium.launch(channel='chrome')
                context = browser_instance.new_context(storage_state="data/state.json")
                page = context.new_page()
                page.goto(self.start_urls[0],timeout=0)

            try:
                page.wait_for_selector('input[name="text"]', timeout = 5000)
            except Exception as e:
                print("Element not found", str(e))
                element_exists = False

            if element_exists:
                email, password, phone, username  = self.get_credentials(num_count)
                # print('CREDENTIALS: ',email,password,phone,username)
                self.login(page, email, password, phone, username)
                href = self.href_loop_grab(context, page)
                if not href:
                    loop = False
                    break
                num_count = self.followers_scroll(page, href, username, num_count,context)
            else:
                element_exists = True
                try:
                    page.wait_for_selector('div[data-testid="UserAvatar-Container-cryptoanalyst27"]', timeout = 5000)

                except Exception as e:
                    print("Element not found", str(e))
                    element_exists = False

                    try:
                        page.wait_for_selector('div[data-testid="UserAvatar-Container-JBenfit"]', timeout = 5000)
                        element_exists = True


                    except Exception as e:
                        print("Counldn't log in. Letting exception {} killing script...".format(e))
                        raise e

                    if element_exists:
                        href = self.href_loop_grab(context, page)
                        if not href:
                            _, _, _, username = self.get_credentials(num_count)
                            loop = False
                            break
                        num_count = self.followers_scroll(page, href, username, num_count, context)

                if element_exists:
                    _, _, _, username  =self.get_credentials(num_count)
                    href = self.href_loop_grab(context, page)
                    if not href:
                        loop = False
                        break
                    num_count = self.followers_scroll(page, href, username, num_count, context)


    def get_credentials(self, num_count):
        accounts = {'email1':'TWITTER_EMAIL'
                    ,'password1':'TWITTER_PASS'
                    ,'username1':'TWITTER_USER'
                    ,'email2':'TWITTER_EMAIL2'
                    ,'password2':'TWITTER_PASS2'
                    ,'username2':'TWITTER_USER2'}
        
            
        email  = os.environ.get(accounts["email{}".format(num_count)])
        password = os.environ.get(accounts["password{}".format(num_count)])
        username  = os.environ.get(accounts["username{}".format(num_count)])
        phone = os.environ.get('TWITTER_PHONE')
        return email, password, phone, username

    def login(self, page, email, password, phone, username):
        print('entering login...')

        try: 
            # Wait for and type into email input
            email_input = page.wait_for_selector('input[name="text"]', state="attached")
            print('email_input in login in line 145')
            time.sleep(random.randint(2, 3))
            email_input.type(email,delay=100)
            print('email input sent in line 148...')
            time.sleep(random.randint(2, 3))

            # Wait for and click next button

            next_button = page.wait_for_selector('xpath=//div[.="Next"]', state="attached")
            print('next_button in line 154')
            time.sleep(random.randint(2, 3))
            next_button.click()
            print('next button clicked at 157...')
            time.sleep(random.randint(2, 3))

            try:
                # Wait for and type into phone input
                phone_input = page.wait_for_selector('input[name="text"]', state="attached", timeout = 5000)
                print('phone_input in like 163...')
                phone_input.type(phone, delay=100)
                print('phone_input at line 163')
                time.sleep(random.randint(2, 9))

                # Wait for and click next button again
                next_button = page.wait_for_selector('xpath=//div[.="Next"]', state="attached")
                print('next button visible at 170...')
                next_button.click()
                print('next button clicked as line 172..')
                time.sleep(random.randint(2, 3))

            except TimeoutError as e:
                print(f'e in try block: {e}')

            print('phone input now inputting password')
            # Wait for and type into password input
            password_input = page.wait_for_selector('input[name="password"]', state="attached")
            password_input.type(password, delay=100)
            time.sleep(random.randint(2, 3))
            print('waiting for login button to be clickable...')
            # Wait for and click login button
            login_button = page.wait_for_selector('xpath=//div[@data-testid="LoginForm_Login_Button"]', state="attached")
            login_button.click()
            print('login clicked...')

            time.sleep(random.randint(2, 3))

        except Exception as e: 
            try:
                element_is_visible = expect(page.get_by_text("Something went wrong. Try reloading.")).to_be_visible()
                if element_is_visible:
                    print('Something went wrong. Likely 429 status.returning at line 189...')
                    self.logout_flow(page, username)
            except Exception as e:
                print(f'Exception: {e} in login...')
                raise e

    def href_loop_grab(self, context, page):

        existing_hrefs = pd.read_csv(hrefs_master)
        first_pass, users_not_to_scrape = self.href_loop_add()

        if first_pass:
            self.cache_session(context, first_pass)
            page.goto(self.start_urls[0],timeout=5000)
            time.sleep(5)
            last_height = page.evaluate("document.body.scrollHeight")
            # Wait for at least one link to be present
            hrefs = set()

            page.wait_for_selector('xpath=//a[.//span[contains(text(), "@")]]')

            # Get all link elements
            link_elements = page.query_selector_all('xpath=//a[.//span[contains(text(), "@")]]')

            for link in link_elements:
                hrefs.add(link.get_attribute('href'))

            len_hrefs = 0
            inner_loop = True
            while inner_loop:
                old_len = len_hrefs
                print('entering inner loop in href_loop_grab line 169...')
                    # Scroll to the bottom of the page
                    # Scroll to the bottom of the page
                page.evaluate("window.scrollBy(0, 1000);")
                
                # Wait for the new tweets to load
                time.sleep(random.randint(2,5)) 
                page.wait_for_selector('xpath=//a[.//span[contains(text(), "@")]]')

                # Get all link elements
                link_elements = page.query_selector_all('xpath=//a[.//span[contains(text(), "@")]]')

                for link in link_elements:
                    hrefs.add(link.get_attribute('href'))

                len_hrefs = len(hrefs)

                print('old_len in href_loop_grab: ', old_len, '\nnew_len in href_loop_grab: ', len_hrefs)
                if old_len == len_hrefs:
                    inner_loop = False
                    break

            print('HREF1: ', hrefs)

            if not (len([href for href in hrefs if href not in existing_hrefs['0']]) == 0):
                hrefs = list(hrefs)
                href_series = pd.Series(hrefs)
                href_series.to_csv(hrefs_master, index = False)
        else: hrefs = existing_hrefs['0'].values

        hrefs = [href for href in hrefs if '@' + href.split('/')[-1] not in users_not_to_scrape]
        hrefs = ['https://twitter.com{}'.format(href) for href in hrefs]
        return hrefs[0].strip()
    
    def href_loop_add(self):
        df = pd.read_csv(followers_scroll_filename)
        today = datetime.today().strftime('%Y-%m-%d')
        if len(df.loc[pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d') == today]) > 0:
            return False, df['handle'].unique()
        else: return True, df['handle'].unique()

    def cache_session(self, first_pass, browswer):
        if first_pass:
            # Save storage state into the file.
            browswer.storage_state(path="data/state.json")
        else: return

    def followers_scroll(self, page, href, username, num_count, context):
        tweets_string = []
        try:
            # if page.get_by_text("Details").click()
            print('CURRENT HREF: ', href)
            page.goto(href)
            # Get the current scroll height
            last_height = page.evaluate("document.body.scrollHeight")
            print('Original Last Height: ', last_height)
            # Navigate to the specific href and wait for the articles to load
            # Wait for at least one tweet to be present

            page.wait_for_selector("xpath=//*[@role='article']")

            # Get all tweet elements
            tweet_elements = page.query_selector_all("xpath=//*[@role='article']")
 
   
            time.sleep(random.randint(2,5))
            print('slept 3 seconds...')
            # Extract the text content from each tweet element
            tweets = [tweet.text_content() for tweet in tweet_elements]
            tweets_string.extend(tweets)

            inner_loop = True
            while inner_loop:
                print('entering inner loop...')
                    # Scroll to the bottom of the page
                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait for the new tweets to load
                time.sleep(random.randint(2,3)) # consider adding randomness. attempting to avoid 429 status
                
                # Get the tweets
                tweet_elements = page.query_selector_all("xpath=//*[@role='article']")
                tweets_string.extend([tw.text_content() for tw in tweet_elements])

                
                # Process the tweets
                for r in range(len(tweets_string)):
                    print('len tweets_string: ',len(tweets_string))
                    print('tweets_string_contents: ', tweets_string)
                    print("entering df creation at index {}".format(r))
                    if tweets_string:
                        try:
                            data = tweets_string[r]

                            print('un-parsed data in tweet_string: ', data)

                            result = self.parse_tweet_info(data)
                            result = self.tweet_format(result, data)
                            result = self.format_date(result)
                            if result:
                                df = pd.DataFrame()
                                df.at[r,'username'] = result['username']
                                df.at[r,'handle'] = result['handle']
                                df.at[r,'date'] = result['date']
                                df.at[r,'tweet'] = result['tweet']
                                df.at[r,'timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                print(df)


                                df.drop_duplicates(subset = ['handle','tweet'], inplace = True)
                        
                                df_write_filename = data_path + '/followers_scroll.csv'

                                if os.path.isfile(df_write_filename):
                                        df.to_csv(df_write_filename, mode='a', header=False, index=False)
                                        df = pd.DataFrame()
                                        tweets_string
                                else:
                                    df.to_csv(df_write_filename, header=True, index=False)

                        except Exception as e:
                            raise e
                            # pass
                            # print('Exception while creating df lists... {}... moving to next tweet_string'.format(e))

                        # ### in testing 
                        # if tweet in stopping_section:
                        #     loop = False
                        #     break
                        # ###

                # Break the loop if no more tweets are loaded
                new_height = page.evaluate("document.body.scrollHeight")
                print('prelim len tweets_string: ', len(tweets_string))

                tweets_string = [] #wipe list clean to go back through

                # print('TWEETS_STRING',tweets_string)
                print('new_height: ', new_height, '\nOld Height: ', last_height)
                if new_height == last_height:
                    print('moving to next user...')
                    inner_loop = self.logout_flow(page, username)
                    if not inner_loop:
                        break
                 
                last_height = new_height
                # print(usernames)
                time.sleep(random.randint(1,2)) 

            if num_count == 2:
                num_count = 1
            else: num_count += 1
            return num_count

        except Exception as e:
            # raise e
            print('Exception in follower_scroll: {}... moving to next user...'.format(e))

            self.logout_flow(page, username)
          
            if num_count == 2:
                num_count = 1
            else: num_count += 1
            return num_count

        
            #ADD BACK eventually and get to work -- filename = data_path + '/most_recents.csv'
            # today_most_recent.to_csv(filename, index = False)

    def parse_tweet_info(self, tweet_string):
        if ('Promoted') in tweet_string:
            return None
        # Regular expression pattern to match username, handle, date and tweet
        patterns = [
        re.compile(r'(.*?)\s@(\w+)\s·\s(\w+\s\d+,\s\d+)(.*?)(\d+.*|$)'),
        re.compile(r'.*?([^\s@]+(?:\s[^\s@]+)*)@(\S+)·(\S+\s\d+)(.*?)(\d+.*|$)'),
        re.compile(r'(.*?)@(\w+)·(\w+\s\d+),\s(\d+)(.*?)(\d+.*|$)'),
        re.compile(r'(.*?)@(\w+)·(\w+)(.*)'),
        # Add more patterns here as needed
        ]

        for pattern in patterns:
            # Search for matches
            match = pattern.match(tweet_string)
         # If matches are found, build and return a dictionary
            if match:
                return {
                    'username': match.group(1),
                    'handle': '@' + match.group(2),
                    'date': match.group(3),
                    'tweet': match.group(4).strip()
                }
                
        # If no matches are found with any patterns, return None
        return None

    def tweet_format(self, dct, tweet_string):
        if dct:
            print('tweet_string: ',tweet_string)
            print('dct: ',dct)
            if '·' in tweet_string:
                dct['tweet'] = tweet_string.split('·')[1]
                dct['tweet'] = dct['tweet'] = re.sub("^, \d+", "", dct['tweet'])
                return dct

    def format_date(self, dct):
        if dct:
            pattern = re.compile(r'^\S+\s\d+|\d+\.\d+[KkMmGgTt]?$')
            dct['tweet'] = re.sub(pattern, '', dct['tweet'])

            splits = re.split('Retweeted|Pinned Tweet', dct['username'])
            if len(splits) > 1:
                dct['username'] = splits[-1]

            if len(dct['date'].split(' ')) <= 2:
                dct['date'] = dct['date'] + ', 2023'
            else: pass

            return dct
    
    def logout_flow(self, page, username):
        try:
            # profile_pic = page.wait_for_selector('div[data-testid="SideNav_AccountSwitcher_Button"]')
            # profile_pic = page.wait_for_selector('div[aria-label="Account menu"]')
            profile_pic = page.wait_for_selector('div[data-testid="UserAvatar-Container-{}"]'.format(username))
            profile_pic.click()
        except Exception as e:
            username = 'JBenfit'
            profile_pic = page.wait_for_selector('div[data-testid="UserAvatar-Container-{}"]'.format(username))
            profile_pic.click()

        # Logout_btn = page.wait_for_selector('[data-testid="AccountSwitcher_Logout_Button"]')
        # logout_btn = page.wait_for_selector('[data-testid="AccountSwitcher_Logout_Button"]')
        # logout_btn.click()
        page.get_by_test_id("AccountSwitcher_Logout_Button").click()
        time.sleep(2)
        page.get_by_test_id("confirmationSheetConfirm").click()
        time.sleep(5)
        page.get_by_test_id("loginButton").click()

        time.sleep(10)

        return False
            
if "__main__" == __name__:
    process = CrawlerProcess()
    process.crawl(TwitterScraper)
    process.start()

   


                                
