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


#url to the page we want to scrape
base_url = 'https://sportsbook.fanduel.com/sports/navigation/6227.1/13348.3'
#base_url = "https://sportsbook.fanduel.com/sports/navigation/7287.1/9886.3" #did not work for ufc

def get_lines():
    driver = webdriver.Chrome('/Users/arotem/Documents/bettingMay/chromedriver', options=chrome_options)
    driver.get(base_url)

    driver.implicitly_wait(2) #waits for the json to load

    matches = driver.find_elements_by_xpath("//div[@class='event' or @class='event last'] ")
    len(matches)
    return_dict = {}

    #match = matches[1]
    for match in matches:
        time = match.find_element_by_xpath(".//div[@class='time']").text
        try:
            if('Tomorrow' in time):
                final_time = date.today()  + timedelta(days=1)
                final_time = final_time.strftime('%b %d').upper()
            else:
                time_convert = datetime.strptime(time, '%m/%d/%Y %H:%M%p')
                final_time =  time_convert.strftime('%b %d').upper()
        except ValueError as e:
            final_time = date.today().strftime('%b %d').upper()
            print(final_time)
        if(final_time not in return_dict.keys()):
            return_dict[final_time] = {}

        away_team = match.find_element_by_xpath(".//div[@class='eventTitle away']").text
        home_team = match.find_element_by_xpath(".//div[@class='eventTitle home']").text

        lines = match.find_elements_by_xpath(".//div[@class='flex']")
        lines.pop(0)
        away = [away_team]
        home = [home_team]
        for i in range(0, len(lines)-1,2):
            away.append(lines[i].text.replace('\n', ' '))
            home.append(lines[i+1].text.replace('\n', ' '))

        return_dict[final_time][away_team + ' - ' + home_team] = (away, home)
    driver.close()
    driver.quit()
    return return_dict