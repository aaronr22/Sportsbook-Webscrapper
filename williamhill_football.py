##ticky because we use get_attribute and some string manipulation

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
from time import sleep


chrome_options = Options()  
chrome_options.add_argument("--headless") 
chrome_options.add_argument("window-size=1920,1080")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = ENV['GOOGLE_CHROME_PATH']

#url to the page we want to scrape
base_url = 'https://www.williamhill.com/us/nj/bet/football/events/all'

def run_wh():
    driver = webdriver.Chrome(ENV['CHROMEDRIVER_PATH'], options=chrome_options)
    #driver = webdriver.Chrome('/Users/arotem/Documents/bettingMay/chromedriver', options=chrome_options
    driver.get(base_url)

    driver.implicitly_wait(2) #waits for the json to load
    #eventView eventView-table_tennis

    headers = driver.find_elements_by_xpath(".//div[@class='Expander has--toggle competitionExpander']")
    driver.implicitly_wait(3)
    if(headers[0].text[0:3] != 'NFL'):
        headers[1].click
    driver.implicitly_wait(2)
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(last_height)
        if new_height == last_height:

            break
        last_height = new_height
    driver.implicitly_wait(3)    


    # lists = driver.find_elements_by_xpath(".//div[@class='eventList']")
    # driver.implicitly_wait(3)
    matches = driver.find_elements_by_xpath(".//div[@class='EventCard'] ")
    len(matches)

    #match = matches[0]
    result_dict = {}

    for match in matches:
        date = match.find_element_by_xpath(".//span[@class='date underlined']").text

        game_date = date[:date.index(' |')]
        if(game_date not in result_dict):
            result_dict[game_date] ={}

        teams = match.find_elements_by_xpath(".//a[contains(@class, 'competitor')]")
        team1 = teams[0].text
        team2 = teams[1].text

        odds = match.find_elements_by_xpath(".//div[contains(@class, 'selectionContainer')]")
        len(odds)

        odds_text = list(map(lambda x: x.text.replace('\n', ' ').replace('Over', 'O').replace('Under', 'U'), odds))

        team1_list = [team1]
        team2_list = [team2]
        for i in range(0, len(odds_text),2):
            team1_list.append(odds_text[i])
            team2_list.append(odds_text[i+1])

        result_dict[game_date][team1 + ' - ' + team2] = (team1_list, team2_list)
    driver.close()
    driver.quit()
    return result_dict