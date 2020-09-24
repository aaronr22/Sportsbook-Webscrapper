#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
from datetime import datetime
from time import sleep
from selenium.webdriver.chrome.options import Options


# In[2]:


#mobile_emulation = { "deviceName": "iPad" }

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--example-flag")
chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
#chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = os.environ['GOOGLE_CHROME_PATH']

def hasNumbers(inputString):
    if("49ers" in inputString):
        return False
    else:
        return any(char.isdigit() for char in inputString)
    
teams_dict = {'HOU Texans': 'Houston Texans',
 'KC Chiefs': 'Kansas City Chiefs',
 'MIA Dolphins': 'Miami Dolphins',
 'NE Patriots': 'New England Patriots',
 'CLE Browns': 'Cleveland Browns',
 'BAL Ravens': 'Baltimore Ravens',
 'NY Jets': 'New York Jets',
 'BUF Bills': 'Buffalo Bills',
 'LV Raiders': 'Las Vegas Raiders',
 'CAR Panthers': 'Carolina Panthers',
 'SEA Seahawks': 'Seattle Seahawks',
 'ATL Falcons': 'Atlanta Falcons',
 'PHI Eagles': 'Philadelphia Eagles',
 'WAS Football Team': 'Washington Football Team',
 'CHI Bears': 'Chicago Bears',
 'DET Lions': 'Detroit Lions',
 'IND Colts': 'Indianapolis Colts',
 'JAX Jaguars': 'Jacksonville Jaguars',
 'GB Packers': 'Green Bay Packers',
 'MIN Vikings': 'Minnesota Vikings',
 'LA Chargers': 'Los Angeles Chargers',
 'CIN Bengals': 'Cincinnati Bengals',
 'ARZ Cardinals': 'Arizona Cardinals',
 'TB Buccaneers': 'Tampa Bay Buccaneers',
 'NO Saints': 'New Orleans Saints',
 'DAL Cowboys': 'Dallas Cowboys',
 'LA Rams': 'Los Angeles Rams',
 'PIT Steelers': 'Pittsburgh Steelers',
 'NY Giants': 'New York Giants',
 'TEN Titans': 'Tennessee Titans',
 'DEN Broncos': 'Denver Broncos',
  'SF 49ers':'San Francisco 49ers'}


base_url = 'https://mobile.nj.bet365.com'

def get_lines():
    driver = webdriver.Chrome(os.environ['CHROMEDRIVER_PATH'], options=chrome_options)
    try:
        #driver = webdriver.Chrome('/Users/arotem/Documents/bettingMay/chromedriver', options=chrome_options)
        driver.get(base_url)

        driver.implicitly_wait(2) #waits for the json to load


        football_element = driver.find_element_by_xpath(".//div[@class='crm-MarketSplash_Image crm-MarketSplash_Image-12 ']")



        football_element.click()
        sleep(2)

        driver.find_element_by_xpath(".//div[contains(text(),'Lines')]").click()
        sleep(2)

        driver.find_element_by_xpath(".//span[contains(text(),'Game Lines')]").click()
        #driver.implicitly_wait(3) 
        sleep(2)

        left_col = driver.find_element_by_xpath(".//div[contains(@class, 'cm-MarketCouponFixtureLabelAdvancedRowHeight sl-MarketCouponFixtureLabelBase gl-Market_General gl-Market_HasLabels gl-Market_PWidth-50 ')]")
        line_cols = driver.find_elements_by_xpath(".//div[contains(@class, 'sl-MarketCouponAdvancedBase gl-Market_General gl-Market_PWidth-18 cm-MarketCouponAdvancedOddsDonBest2Col ')]")
        mid_col = line_cols[0]
        right_col = line_cols[1]

        l_rows = left_col.find_elements_by_xpath(".//div[contains(@class, 'cm-ParticipantWithBookClosesDonBest_TeamName ') or contains(@class, 'gl-MarketColumnHeader sl-MarketHeaderLabel sl-MarketHeaderLabel_Date ')]")
        m_rows = mid_col.find_elements_by_xpath(".//div[contains(@class, 'cm-ParticipantCenteredAndStackedDonBest gl-Participant_General ') or contains(@class, 'gl-MarketColumnHeader ')]")
        r_rows = right_col.find_elements_by_xpath(".//div[contains(@class, 'cm-ParticipantOddsWithHandicapDonBest gl-Participant_General ') or contains(@class, 'gl-MarketColumnHeader ')]")

        l_text = [x.text for x in l_rows]
        m_text = [x.text for x in m_rows]
        r_text = [x.text for x in r_rows]

        zipped = list(zip(l_text, m_text, r_text))

        t = 0
        tmp_dict = {}
        current_date = ''
        for i in range(0,len(zipped)):
            if(hasNumbers(zipped[t][0])):
                current_date = zipped[t][0][4:].upper()
                tmp_dict[current_date] = {}
                t = t+1
            else:
                game_title = teams_dict[zipped[t][0]] + ' - ' + teams_dict[zipped[t+1][0]]
                tmp_dict[current_date][game_title] = ((teams_dict[zipped[t][0]], zipped[t][1].replace('\n', ' '), 0 , zipped[t][2].replace('\n', ' ')),(teams_dict[zipped[t+1][0]], zipped[t+1][1].replace('\n', ' '), 0 , zipped[t+1][2].replace('\n', ' ')))
                t = t+2
            if(t == len(zipped)):
                break


        driver.close()
        driver.quit()
        return tmp_dict
    except Exception as e:
        driver.close()
        driver.quit()
        return {"Error": e}
