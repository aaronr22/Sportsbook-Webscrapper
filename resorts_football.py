#selenium is for loading the javascript and interacting with buttons on the page.  
from selenium import webdriver
#for filling out a form.  not used in this script
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
#bs4 is for crawling through the source of the page to pull data
from bs4 import BeautifulSoup
import re
import os
import json
from datetime import datetime
from time import sleep
from selenium.webdriver.chrome.options import Options

base_url = 'https://sport.resortscasino.com/sports/football/nfl/'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("window-size=1920,1080")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = os.environ['GOOGLE_CHROME_PATH']

def get_lines():

    driver = webdriver.Chrome(os.environ['CHROMEDRIVER_PATH'], options=chrome_options)
    try:
        #driver = webdriver.Chrome('/Users/arotem/Documents/bettingMay/chromedriver', options=chrome_options
        driver.get(base_url)

        driver.implicitly_wait(2) #waits for the json to load

        matches = driver.find_elements_by_xpath(".//div[@class='rj-ev-list__ev-card__inner']")
        html = list(map(lambda x: x.get_attribute('innerHTML'), matches))

        last_height = driver.execute_script("return document.body.scrollHeight")

        for i in range(3):

            # Scroll down to the bottom.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            driver.implicitly_wait(2)
            # Wait to load the page.
            sleep(2)
            
            tmp = driver.find_elements_by_xpath(".//div[@class='rj-ev-list__ev-card__inner']") 
            tmp_html = list(map(lambda x: x.get_attribute('innerHTML'), tmp))
            print(len(tmp))
            html = html + tmp_html

            # Calculate new scroll height and compare with last scroll height.
            new_height = driver.execute_script("return document.body.scrollHeight")
            print(last_height)
            if new_height == last_height:

                break
        last_height = new_height
        tmp = driver.find_elements_by_xpath(".//div[@class='rj-ev-list__ev-card__inner']") 
        print(len(tmp))
        matches = matches + tmp
        driver.implicitly_wait(3)    

        master_list = {}
        for match in html:
            soup = BeautifulSoup(match, features="html.parser")
            tmp_str = (soup.get_text(separator="|")).split('|')[:-1]
            date = tmp_str[2].upper()
            if (date not in master_list.keys()):
                master_list[date] = {}
            t1 = tmp_str[0] 
            t2 = tmp_str[1]
            if('Washington' in t1):
                t1 = 'Washington Football Team'
            if('Washington' in t2):
                t2 = 'Washington Football Team'
            game_title = t1 + ' - ' + t2
            team1 = [t1, tmp_str[4] + ' ' + tmp_str[5]]
            team2 = [t2, tmp_str[6] + ' ' + tmp_str[7]]
            if(tmp_str[8] != 'O' and tmp_str[8] != 'U'):
                team1.append(tmp_str[8])
                team2.append(tmp_str[9])
                team1.append(tmp_str[10]+ ' ' + tmp_str[11] + ' ' + tmp_str[12])
                team2.append(tmp_str[13]+ ' ' + tmp_str[14] + ' ' + tmp_str[15])
            else:
                team1.append(0)
                team2.append(0)
                team1.append(tmp_str[8]+ ' ' + tmp_str[9] + ' ' + tmp_str[10])
                team2.append(tmp_str[11]+ ' ' + tmp_str[12] + ' ' + tmp_str[13])
            master_list[date][game_title] = (team1, team2)
        driver.close()
        driver.quit()
        return master_list
    except Exception as e:
        driver.quit()
        driver.close()
        return {'Error': e}