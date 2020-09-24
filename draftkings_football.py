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
from datetime import datetime, timedelta, date
from selenium.webdriver.chrome.options import Options


chrome_options = Options()  
chrome_options.add_argument("--headless") 
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = os.environ['GOOGLE_CHROME_PATH']

base_url = 'https://sportsbook.draftkings.com/leagues/football/3?category=game-lines&subcategory=game'

def get_game(tuple1, tuple2):
    g1 = (tuple1[0][tuple1[0].index('\n')+1:], tuple1[1], tuple1[2], tuple1[3])
    game_title = g1[0] +' - ' + tuple2[0]
    return_duct = (game_title, [g1, tuple2])
    return return_duct

#base_url = "https://sportsbook.draftkings.com/leagues/mma/2162?category=fight-lines&subcategory=moneyline" #ufc works
def get_lines():
    driver = webdriver.Chrome(os.environ['CHROMEDRIVER_PATH'], options=chrome_options)
    #driver = webdriver.Chrome('/Users/arotem/Documents/bettingMay/chromedriver', options=chrome_options
    driver.get(base_url)

    driver.implicitly_wait(2) #waits for the json to load

    game_days = driver.find_elements_by_xpath(".//section[@class='sportsbook-table'] ")
    final_dict = {}

    game_days = driver.find_elements_by_xpath(".//section[@class='sportsbook-table'] ")

    final_dict = {}

    for game_day in game_days:
        #print(game_day.get_attribute('innerHTML'))
        date_field = game_day.find_element_by_xpath(".//div[@class='sportsbook-table-header__title']").text
        #print(date_field)
        body = game_day.find_element_by_xpath(".//div[@class='sportsbook-table__body']")
        body_children = body.find_elements_by_xpath("*")
        
        try:
            if('Tomorrow' in date_field):
                final_time = date.today()  + timedelta(days=1)
                final_time = final_time.strftime('%b %d').upper()
            else:

                time_convert = datetime.strptime(date_field[:-2], '%a %b %d')

                final_time =  time_convert.strftime('%b %d').upper()
        except ValueError:
            final_time = date.today().strftime('%b %d').upper()
        #final_time = date_field
        final_dict[final_time] = {}

        tmp_list = []
        line1 = body_children[0].find_elements_by_xpath(".//div[@class='sportsbook-table__column-row' or @class='sportsbook-table__column-row break-line']")
        line2 = body_children[1].find_elements_by_xpath(".//div[@class='sportsbook-table__column-row' or @class='sportsbook-table__column-row break-line']")
        line3 = body_children[2].find_elements_by_xpath(".//div[@class='sportsbook-table__column-row' or @class='sportsbook-table__column-row break-line']")
        line4 = body_children[3].find_elements_by_xpath(".//div[@class='sportsbook-table__column-row' or @class='sportsbook-table__column-row break-line']")
        #zip these into a list

        tmp_map = map(lambda x: (x[0].text, x[1].text.replace('\n', ' '), x[2].text.replace('\n', ' '), x[3].text.replace('\n', ' ')), zip(line1, line2, line3, line4))

        list_map = list(tmp_map)
        

        i = 0
        for i in range(len(list_map))[0::2]:
            if(i < len(list_map)-1):
                tmp = get_game(list_map[i], list_map[i+1])
                title = tmp[0]
                final_dict[final_time][title] = tmp[1]
            #i = i+2
    driver.close()
    driver.quit()
    return final_dict