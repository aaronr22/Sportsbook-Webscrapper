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


chrome_options = Options()  
chrome_options.add_argument("--headless") 
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = os.environ['GOOGLE_CHROME_PATH']

#url to the page we want to scrape
base_url = 'https://nj.foxbet.com/#/american_football/competitions/8169879'

def get_lines():
    driver = webdriver.Chrome(os.environ['CHROMEDRIVER_PATH'], options=chrome_options)
    try:
    #driver = webdriver.Chrome('/Users/arotem/Documents/bettingMay/chromedriver', options=chrome_options
        driver.get(base_url)

        driver.implicitly_wait(2) #waits for the json to load

        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        driver.close()
        driver.quit()
        regex = re.compile('.*afEvt eventView.*')
        matches = soup.findAll("section", {"class": regex})


        return_dict = {}

        for match in matches:
            try:
                d = match.find("span", {"class": "match-time__date"}).text[:-2].upper()
            except:
                d = date.today().strftime('%b %d').upper()
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

            match_name = home + ' - ' + away
            away_out = [away] + [m1_lines[0] + ' '+m1_lines[1]] + [m1_lines[2]] + [m1_lines[3] + ' '+m1_lines[4]]
            home_out = [home] + [m2_lines[0] + ' '+m2_lines[1]] + [m2_lines[2]] + [m2_lines[3] + ' '+m2_lines[4]]

            return_dict[d][match_name] = (home_out, away_out)
        return return_dict
    except Exception as e:
        driver.close()
        driver.quit()
        return {"Error": e}