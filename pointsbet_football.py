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
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()  
chrome_options.add_argument("--headless") 
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_PATH')

#url to the page we want to scrape
nfl_base_url = 'https://nj.pointsbet.com/sports/american-football/NFL'
cfb_base_url = 'https://nj.pointsbet.com/sports/american-football/NCAAF'

def get_lines(sport):
    try:
        driver = webdriver.Chrome(os.environ.get('CHROMEDRIVER_PATH'), options=chrome_options)
        if sport == 'NFL':
            driver.get(nfl_base_url)
        elif sport == 'CFB':
            driver.get(cfb_base_url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".f1tiy9f2")))
        #driver.implicitly_wait(4) #waits for the json to load
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        driver.close()
        driver.quit()
        result_dict = {}
        matches = soup.findAll("div", {"data-test": "event"})
        if(len(matches) == 0):
            print('No matches found')
        for match in matches:
            days = match.find("div", {"class": "f1tiy9f2"}).text

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
            team_names = match.findAll("div", {"class":'f2rhni5'})
            team1 = team_names[0].text
            team2 = team_names[1].text

            odds = match.findAll("button", {"data-test":'oddsButton'})

            team1_odds = [team1] + list(map(lambda x: x.text.replace('\n', ' ').replace('Ov', 'O').replace('Un', 'U'), odds[:3]))
            team2_odds = [team2] + list(map(lambda x: x.text.replace('\n', ' ').replace('Ov', 'O').replace('Un', 'U'), odds[3:]))
            result_dict[game_date][team1 + ' - ' + team2] = (team1_odds, team2_odds)
        return result_dict
    except Exception as e:
        driver.close()
        driver.quit()
        print(e)
        return {"Error": e}