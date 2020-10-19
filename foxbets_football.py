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
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta, date
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()  
chrome_options.add_argument("--headless") 
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = os.environ['GOOGLE_CHROME_PATH']

#url to the page we want to scrape
nfl_base_url = 'https://nj.foxbet.com/#/american_football/competitions/8169879'
cfb_base_url = 'https://nj.foxbet.com/#/american_football/competitions/8211237'

def get_lines(sport):
    driver = webdriver.Chrome(os.environ['CHROMEDRIVER_PATH'], options=chrome_options)
    try:
    #driver = webdriver.Chrome('/Users/arotem/Documents/bettingMay/chromedriver', options=chrome_options
        if sport == 'NFL':
            driver.get(nfl_base_url)
        elif sport == 'CFB':
            driver.get(cfb_base_url)

        driver.implicitly_wait(2) #waits for the json to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".teamName")))
        driver.implicitly_wait(3)
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        driver.close()
        driver.quit()
        regex = re.compile('.*afEvt eventView.*')
        matches = soup.findAll("section", {"class": regex})
        print(len(matches))

        return_dict = {}

        for match in matches:
            try:
                d = match.find("span", {"class": "match-time__date"}).text[:-2].upper()
            except:
                d = date.today().strftime('%b %d').upper()
            if len(d) == 5:
                d = d[0:4] + '0' + d[4]
            if(d not in return_dict.keys()):
                return_dict[d] = {}

            markets = match.findAll("div", {"class":"afEvt__teamMarkets"})

            m1_children = markets[0].findChildren("em", {"class":['button__bet__title button__bet__title--abbreviated','selectionOdds-event']})
            m2_children = markets[1].findChildren("em", {"class":['button__bet__title button__bet__title--abbreviated','selectionOdds-event']})

            m1_lines = list(map(lambda x: x.text.strip().replace('\n', ' '), m1_children))
            m2_lines = list(map(lambda x: x.text.strip().replace('\n', ' '), m2_children))

            names = match.findAll("span", {"class":'teamName'})

            home = names[1].text
            away = names[0].text

            if 'Washington' in home:
                home = 'Washington Football Team'
            if 'Washington' in away:
                away = 'Washington Football Team'

            match_name = home + ' - ' + away
            if(len(m1_lines) == 5):
                away_out = [away] + [m1_lines[0] + ' '+m1_lines[1]] + [m1_lines[2]] + [m1_lines[3] + ' '+m1_lines[4]]
            elif(len(m1_lines) == 3):
                away_out = [away] + [m1_lines[0] + ' '+m1_lines[1]] + [m1_lines[2]] + [0]
            elif(len(m1_lines) == 4):
                away_out = [away] + [m1_lines[0] + ' '+m1_lines[1]] + [0] + [m1_lines[2] + ' ' + m1_lines[3]] 
            else:
                print(m1_lines)
                away_out = [away] + ['|'.join(m1_lines)]
            if(len(m2_lines) == 5):
                home_out = [home] + [m2_lines[0] + ' '+m2_lines[1]] + [m2_lines[2]] + [m2_lines[3] + ' '+m2_lines[4]]
            elif(len(m2_lines) == 3):
                home_out = [home] + [m2_lines[0] + ' '+m2_lines[1]] + [m2_lines[2]] + [0]
            elif(len(m2_lines) == 4):
                home_out = [home] + [m2_lines[0] + ' '+m2_lines[1]] +[0] + [m2_lines[2]+ m2_lines[3]] 
            else:
                home_out = [home] + ['|'.join(m2_lines)]
            return_dict[d][match_name] = (home_out, away_out)
        return return_dict
    except Exception as e:
        driver.close()
        driver.quit()
        print(e)
        return {"Error": e}