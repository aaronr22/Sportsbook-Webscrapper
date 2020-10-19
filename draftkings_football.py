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
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = os.environ['GOOGLE_CHROME_PATH']

nfl_base_url = 'https://sportsbook.draftkings.com/leagues/football/3?category=game-lines&subcategory=game'
cfb_base_url = 'https://sportsbook.draftkings.com/leagues/football/2?category=game-lines&subcategory=game'
def parse_tuple(list_map):
    #parse first element
    try:
        index = list_map[0].index('AM')
    except:
        index = list_map[0].index('PM')
    v1 = list_map[0][index + 2:]
    #parse 2nd
    try:
        index = list_map[1].index('+', 1)
    except:
        index = list_map[1].index('-', 1)
    v2= list_map[1][:index] + ' ' + list_map[1][index:]
    #parse 3rd
    v3 = list_map[2].replace("\xa0", " ")
    return (v1,v2,v3,list_map[3])


def get_game(tuple1, tuple2):
    #g1 = (tuple1[0][tuple1[0].index('\n')+1:], tuple1[1], tuple1[2], tuple1[3])
    game_title = tuple1[0] +' - ' + tuple2[0]
    return_duct = (game_title, [tuple1, tuple2])
    return return_duct

#base_url = "https://sportsbook.draftkings.com/leagues/mma/2162?category=fight-lines&subcategory=moneyline" #ufc works
def get_lines(sport):
    driver = webdriver.Chrome(os.environ['CHROMEDRIVER_PATH'], options=chrome_options)
    #driver = webdriver.Chrome('/Users/arotem/Documents/bettingMay/chromedriver', options=chrome_options
    
    if sport == 'NFL':
        driver.get(nfl_base_url)
    elif sport == 'CFB':
        driver.get(cfb_base_url)

    driver.implicitly_wait(2)

    html_source = driver.page_source

    soup = BeautifulSoup(html_source, 'html.parser')
    driver.close()
    driver.quit()
    game_days = soup.findAll("section", {"class": "sportsbook-table"})
    final_dict = {}
    for game_day in game_days:
        date_field = game_day.find("div", {"class":"sportsbook-table-header__title"}).text.strip()
        try:
            if('Tomorrow' in date_field):
                final_time = date.today()  + timedelta(days=1)
                final_time = final_time.strftime('%b %d').upper()
            else:
                time_convert = datetime.strptime(date_field[:-2], '%a %b %d')

                final_time =  time_convert.strftime('%b %d').upper()
        except ValueError:
            final_time = date.today().strftime('%b %d').upper()
        final_dict[final_time] = {}

        body = game_day.find("div", {"class":"sportsbook-table__body"})
        body_children = body.findChildren("div", recursive=False)

        tmp_list = []
        line1 = body_children[0].findAll("div", {"class":["sportsbook-table__column-row", "sportsbook-table__column-row break-line"]})
        line2 = body_children[1].findAll("div", {"class":["sportsbook-table__column-row", "sportsbook-table__column-row break-line"]})
        line3 = body_children[2].findAll("div", {"class":["sportsbook-table__column-row", "sportsbook-table__column-row break-line"]})
        line4 = body_children[3].findAll("div", {"class":["sportsbook-table__column-row", "sportsbook-table__column-row break-line"]})



        tmp_map = map(lambda x: (x[0].text, x[1].text.replace('\n', ' '), x[2].text.replace('\n', ' '), x[3].text.replace('\n', ' ')), zip(line1, line2, line3, line4))

        tmp_list = list(tmp_map)
        list_map = []
        for item in tmp_list:
            list_map.append(parse_tuple(item))
        i = 0
        for i in range(len(list_map))[0::2]:
            if(i < len(list_map)-1):
                tmp = get_game(list_map[i], list_map[i+1])
                title = tmp[0]
                final_dict[final_time][title] = tmp[1]
            #i = i+2
    return final_dict