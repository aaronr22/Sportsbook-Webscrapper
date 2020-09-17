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
import datetime

chrome_options = Options()  
chrome_options.add_argument("--headless") 
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_PATH')

#url to the page we want to scrape
base_url = 'https://nj.pointsbet.com/sports/american-football/NFL'


def get_lines():
    driver = webdriver.Chrome(os.environ.get('CHROMEDRIVER_PATH'), options=chrome_options)
    #driver = webdriver.Chrome('/Users/arotem/Documents/bettingMay/chromedriver', options=chrome_options
    driver.get(base_url)

    driver.implicitly_wait(2) #waits for the json to load
    #eventView eventView-table_tennis

    result_dict = {}
    matches = driver.find_elements_by_xpath(".//div[@data-test='event']")
    for match in matches:
        days = match.find_element_by_xpath(".//div[@class='fij37bd']").text

        if('d' in days):
            i = days.index('d')
            day = days[:i]
            days = days[i+2:]
        else:
            day = 0
        if('h' in days):
            i = days.index('h')
            hours = days[:i]
        else:
            hours = 0

        today = datetime.datetime.now()
        delta = datetime.timedelta(days=int(day), hours=int(hours))
        future = today + delta
        game_date = future.strftime("%b %d").upper()

        if(game_date not in result_dict.keys()):
            result_dict[game_date] = {}

        #get team names
        team_names = match.find_elements_by_xpath(".//div[@class='f2rhni5']")
        team1 = team_names[0].text
        team2 = team_names[1].text

        odds = match.find_elements_by_xpath(".//button[@data-test='oddsButton']")

        team1_odds = [team1] + list(map(lambda x: x.text.replace('\n', ' ').replace('Ov', 'O').replace('Un', 'U'), odds[:3]))
        team2_odds = [team2] + list(map(lambda x: x.text.replace('\n', ' ').replace('Ov', 'O').replace('Un', 'U'), odds[3:]))

        result_dict[game_date][team1 + ' - ' + team2] = (team1_odds, team2_odds)
    driver.close()
    driver.quit()
    return result_dict