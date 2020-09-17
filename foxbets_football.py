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
    #driver = webdriver.Chrome('/Users/arotem/Documents/bettingMay/chromedriver', options=chrome_options
    driver.get(base_url)

    driver.implicitly_wait(2) #waits for the json to load

    #eventView eventView-table_tennis

    matches = driver.find_elements_by_xpath("//section[@class='afEvt eventView compHeader eventView--embeddedHeaders' or @class='afEvt eventView'] ")
    #match = matches[0]
    return_dict = {}

    for match in matches:
        time = match.find_element_by_xpath(".//em[@class='match-time']").text

        date = match.find_element_by_xpath(".//span[@class='match-time__date']").get_attribute('innerHTML')[:-2].upper()
        if(date not in return_dict.keys()):
            return_dict[date] = {}

        markets = match.find_elements_by_xpath(".//div[@class='afEvt__teamMarkets']")
        len(markets)

        m1_children = markets[0].find_elements_by_xpath("*")
        m2_children = markets[1].find_elements_by_xpath("*")

        m1_lines = map(lambda x: x.text.replace('\n', ' '), m1_children)
        m2_lines = map(lambda x: x.text.replace('\n', ' '), m2_children)

        match_name = match.find_element_by_xpath(".//a[@class='afEvt__link']").get_attribute("innerHTML")
        match_name = match_name.replace('@', '-')
        home = match_name[:match_name.index('-')-1]
        away = match_name[match_name.index('-')+2:]

        away_out = [away] + list(m1_lines)
        home_out = [home] + list(m2_lines)

        return_dict[date][match_name] = (home_out, away_out)
    driver.close()
    driver.quit()
    return return_dict