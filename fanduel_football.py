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
from datetime import datetime, timedelta
from datetime import date


chrome_options = Options()  
chrome_options.add_argument("--headless") 
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = os.environ['GOOGLE_CHROME_PATH']

#url to the page we want to scrape
base_url = 'https://sportsbook.fanduel.com/sports/navigation/6227.1/13348.3'
#base_url = "https://sportsbook.fanduel.com/sports/navigation/7287.1/9886.3" #did not work for ufc

def get_lines():
    driver = webdriver.Chrome(os.environ['CHROMEDRIVER_PATH'], options=chrome_options)
    driver.get(base_url)

    driver.implicitly_wait(2)

    html_source = driver.page_source
    driver.close()
    driver.quit()
    soup = BeautifulSoup(html_source, 'html.parser')

    matches = soup.findAll("div", {"class": ["event", "event last"]})

    match = matches[0]
    return_dict = {}

    for match in matches:
        _time = match.find("div", {"class": "time"}).find("span", {"class": ""}).text
        try:
            if('Tomorrow' in _time):
                final_time = date.today()  + timedelta(days=1)
                final_time = final_time.strftime('%b %d').upper()
            else:
                time_convert = datetime.strptime(_time, '%m/%d/%Y %H:%M%p')
                final_time =  time_convert.strftime('%b %d').upper()
        except ValueError as e:
            final_time = date.today().strftime('%b %d').upper()

        if(final_time not in return_dict.keys()):
            return_dict[final_time] = {}

        away_team = match.find("div", {"class": "eventTitle away"}).text.strip()
        home_team = match.find("div", {"class": "eventTitle home"}).text.strip()

        away_team

        away = [away_team]
        home = [home_team]

        points = match.find("div", {"class":'market points'})
        money = match.find("div", {"class":'market money'})
        total = match.find("div", {"class":'market total'})

        p_val = points.findAll("div", {"class":'flex'})
        m_val = money.findAll("div", {"class":'flex'})
        t_val = total.findAll("div", {"class":'flex'})

        if len(p_val) == 2:
            home.append(p_val[1].text.strip())
            away.append(p_val[0].text.strip())
        else:
            home.append(0)
            away.append(0)
        if len(m_val) == 2:
            home.append(m_val[1].text.strip())
            away.append(m_val[0].text.strip())
        else:
            home.append(0)
            away.append(0)
        if len(t_val) == 2:
            home.append(t_val[1].text.strip())
            away.append(t_val[0].text.strip())
        else:
            home.append(0)
            away.append(0)
        return_dict[final_time][away_team + ' - ' + home_team] = (away, home)
    return return_dict