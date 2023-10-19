from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import json

_test_link = 'https://www.flashscore.ua/soccer'

def browser_init(view = True):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    return browser

# def check_wind (browser):
#     window_list = browser.window_handles
#     for window in range(0, len(window_list)-1):
#         browser.switch_to.window(browser.window_handles[len(window_list)-1-window])
#         time.sleep(0.2)
#         browser.close()
#         time.sleep(0.2)
#     window_list = browser.window_handles
#     browser.switch_to.window(browser.window_handles[0])

def get_data_json ():
    with open('leagues_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def set_data_json (data):
    with open('leagues_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

def program ():
    browser = browser_init()
    browser.get(_test_link)
    time.sleep(2) # for load all results
    browser.execute_script("window.open('https://www.google.com', 'new_window')") ## open new window in browser
    window_list = browser.window_handles
    browser.switch_to.window(window_list[0])

    def get_all_country (browser):
        def click_btn_country_more ():
            btn_more = browser.find_element(By.CLASS_NAME, 'lmc__menu').find_element(By.CLASS_NAME,'lmc__itemMore')
            time.sleep(1)
            browser.execute_script("arguments[0].click();", btn_more)
            print('Click btn more')

        click_btn_country_more()
        countrys = browser.find_element(By.CLASS_NAME, 'lmc__menu').find_elements(By.CLASS_NAME, 'lmc__block')
        return countrys
    def get_country_leagues (browser, country):
        leagues = country.find_elements(By.CLASS_NAME, 'lmc__template')
        return leagues
    def get_league_seasons (browser, league_href):
        seasons_array = []
        browser.switch_to.window(window_list[1])
        time.sleep(0.1)
        browser.get(league_link + 'archive/')
        print(f'Get seasons in league')
        time.sleep(0.1)
        season_list = browser.find_elements(By.CLASS_NAME, 'archive__row')
        for season_area in season_list:
            season_obj = {}
            season_arch = season_area.find_element(By.CLASS_NAME, 'archive__text')
            season_name = season_arch.text.strip()
            season_obj['name'] = season_name
            season_obj['href'] = season_arch.get_attribute('href')
            seasons_array.append(season_obj)

        browser.switch_to.window(window_list[0])
        time.sleep(0.1)
        return seasons_array 

    
    leagues_data = {}
    
    for country in get_all_country(browser):
        country_name = country.find_element(By.CLASS_NAME, 'lmc__elementName').text
        print(f'Country : {country_name}')
        country_area = country.find_element(By.TAG_NAME, 'a')
        country_link = country_area.get_attribute('href')
        browser.execute_script("arguments[0].click();", country_area)
        time.sleep(1) # load leagues after click to country btn
        leagues_obj = {}
        for league in get_country_leagues(browser, country):
            league_area = league.find_element(By.CLASS_NAME, 'lmc__templateHref')
            league_name = league_area.text.strip()
            league_link = league_area.get_attribute('href')
            print(f'League name : {league_name} | {league_link}')
            leagues_obj[league_name] = {}
            leagues_obj[league_name]['seasons'] = get_league_seasons(browser, league_link)
            leagues_obj[league_name]['link'] = league_link
        leagues_data[country_name] = leagues_obj
        set_data_json(leagues_data)
    set_data_json(leagues_data)


program()