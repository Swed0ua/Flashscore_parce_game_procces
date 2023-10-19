from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import traceback
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import datetime
_test_link = 'https://www.flashscore.ua/soccer/england/premier-league/fixtures/'
import multiprocessing
import json

def browser_init(view = True):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    return browser

def program (ligue_datas_all, newM = False):
    count_procces = int(multiprocessing.current_process().name.replace('Process-','').strip())-1
    print(f'Count procces {count_procces}')
    ligue_datas = ligue_datas_all[count_procces]
    browser = browser_init()
    browser.execute_script("window.open('https://www.google.com', 'new_window')") ## open new window in browser
    window_list = browser.window_handles
    browser.switch_to.window(window_list[0])
    result_data = []

    def click_btn_country_more (browser):
            try:
                btn_more = browser.find_element(By.CLASS_NAME, 'event__more')
                time.sleep(1)
                browser.execute_script("arguments[0].click();", btn_more)
                print('Click btn more')
                return True
            except Exception as e:
                print('No btn more')
                return False
    
    def get_match_data (browser):
        def get_static_item (text, repl = False) :
            try:
                statistic_wrap =  browser.find_element(By.CLASS_NAME,'section')
                statistics = statistic_wrap.find_elements(By.CLASS_NAME, "stat__row")
                atach_wrapp = statistic_wrap.find_element(By.XPATH, f'.//div[text()="{text}"]/..')
                vl1 = atach_wrapp.find_element(By.CLASS_NAME, 'stat__homeValue').text
                vl2 = atach_wrapp.find_element(By.CLASS_NAME, 'stat__awayValue').text
                try:
                    if repl != False:
                        vl1 = vl1.replace(repl, '')
                        vl2 = vl2.replace(repl, '')
                except Exception as e :
                    print(f'Err in repl {e}')
                vl1 = int(vl1)
                vl2 = int(vl2)
                
                return [vl1, vl2]
            except:
                if repr != False:
                    time.sleep(1)
                try:
                    statistic_wrap =  browser.find_element(By.CLASS_NAME,'section')
                    statistics = statistic_wrap.find_elements(By.CLASS_NAME, "stat__row")
                    atach_wrapp = statistic_wrap.find_element(By.XPATH, f'.//div[text()="{text}"]/..')
                    vl1 = atach_wrapp.find_element(By.CLASS_NAME, 'stat__homeValue').text
                    vl2 = atach_wrapp.find_element(By.CLASS_NAME, 'stat__awayValue').text
                    try:
                        if repl != False:
                            vl1 = vl1.replace(repl, '')
                            vl2 = vl2.replace(repl, '')
                    except Exception as e :
                        print(f'Err in repl {e}')
                    vl1 = int(vl1)
                    vl2 = int(vl2)
                    
                    return [vl1, vl2]
                except:
                    return ['', '']
        obj = {}
        # Tour
        try:
            tour = browser.find_element(By.CLASS_NAME,'tournamentHeader__country').text
            obj['tour'] = tour.split(' - ')[-1]
        except Exception as e :
            print(e)
            obj['tour'] = ''

        # Name
        try:
            names = browser.find_elements(By.CLASS_NAME,"participant__participantName")
            obj['name_1'] = names[1].text.strip()
            obj['name_2'] = names[3].text.strip()
        except Exception as e :
            print(e)
            obj['name_1'] = ''
            obj['name_2'] = ''
       
        # Score
        try:
            score_wrapp = browser.find_element(By.CLASS_NAME,'detailScore__wrapper')
            obj['score_1'] = int(score_wrapp.find_elements(By.TAG_NAME, 'span')[0].text)
            obj['score_2'] = int(score_wrapp.find_elements(By.TAG_NAME, 'span')[-1].text)
        except Exception as e :
            obj['score_1'] = ''
            obj['score_2'] = ''
        
        # Date
        try:
            date = browser.find_element(By.CLASS_NAME,'duelParticipant__startTime')
            item = date.text.strip().split(' ')[0].split('.')
            obj['date'] = item
        except Exception as e :
            obj['date'] = ''

        

        # Кофіцієнт
        try:
            cof_wrap = browser.find_element(By.CLASS_NAME, 'oddsRow')
            obj['cof1'] = float(cof_wrap.find_elements(By.CLASS_NAME, 'oddsValueInner')[0].text)
            obj['cofx'] = float(cof_wrap.find_elements(By.CLASS_NAME, 'oddsValueInner')[1].text)
            obj['cof2'] = float(cof_wrap.find_elements(By.CLASS_NAME, 'oddsValueInner')[2].text)
        except Exception as e:
            if repr:
                time.sleep(1)
            try:
                cof_wrap = browser.find_element(By.CLASS_NAME, 'oddsRow')
                obj['cof1'] = float(cof_wrap.find_elements(By.CLASS_NAME, 'oddsValueInner')[0].text)
                obj['cofx'] = float(cof_wrap.find_elements(By.CLASS_NAME, 'oddsValueInner')[1].text)
                obj['cof2'] = float(cof_wrap.find_elements(By.CLASS_NAME, 'oddsValueInner')[2].text)
            except Exception as e:
                obj['cof1'] = ''
                obj['cofx'] = ''
                obj['cof2'] = ''
        
        # Атаки
        item_wrapp = get_static_item("Атаки")
        obj["atach_1"] = item_wrapp[0]
        obj["atach_2"] = item_wrapp[1]
        
        # Небезпечні Атаки
        item_wrapp = get_static_item("Небезпечні атаки")
        obj["den_atach_1"] = item_wrapp[0]
        obj["den_atach_2"] = item_wrapp[1]
        
        # Удари
        item_wrapp = get_static_item("Удари")
        obj["shot_1"] = item_wrapp[0]
        obj["shot_2"] = item_wrapp[1]

        # Володіння мячем
        item_wrapp = get_static_item("Володіння м'ячем", "%")
        pos1 = ''
        pos2 = ''
        try:
            pos1 = item_wrapp[0] / 100
            pos2 = item_wrapp[1] / 100
        except:
            exec

        obj["poss_1"] = pos1
        obj["poss_2"] = pos2

        print(f'H {obj["cof1"]} | X {obj["cofx"]} | G {obj["cof2"]}')
        return obj
        
    for ligue_data in ligue_datas:
        # ligue_link = ligue_data["href"]
        # ligue_country = ligue_data["country"]
        # ligue_season = ligue_data["season"]
        # ligue_name = ligue_data["ligue"]
        browser.get(ligue_data)
        if newM :
            browser.get(ligue_data + 'fixtures/')
        else :
            browser.get(ligue_data)
        print(ligue_data)
        time.sleep(5) # for load all results
        moreBtnEvent = True
        
        while moreBtnEvent:
             moreBtnEvent = click_btn_country_more(browser)

        items = browser.find_elements(By.CLASS_NAME, 'event__match')

        country = browser.find_elements(By.CLASS_NAME, 'breadcrumb__link')[-1].text.strip()
        season = browser.find_element(By.CLASS_NAME, 'heading__info').text.strip()
        name_l = browser.find_element(By.CLASS_NAME, 'heading__name').text.strip()

        for item in items:
            event_time = item.find_element(By.CLASS_NAME, 'event__time').text
            event_id = item.get_attribute('id')
            event_half_id = event_id.split('_')[-1]
            # def checkDate () :

            #     def get_y (mn):
            #         if mn >= 8:
            #             return 0
            #         else:
            #             return 1

            #     event_time_day = int(event_time.split('.')[0])
            #     event_time_mn = int(event_time.split('.')[1])
            #     event_time_y = get_y(event_time_mn)

            #     time_to_day = int(date_to.split('-')[2])
            #     time_to_mn = int(date_to.split('-')[1])
            #     time_to_y = get_y(time_to_mn)

            #     time_from_day = int(date_from.split('-')[2])
            #     time_from_mn = int(date_from.split('-')[1])
            #     time_from_y = get_y(time_from_mn)


            #     if time_to_y == event_time_y:
            #         if time_to_mn > event_time_mn:
            #             # return True
            #             exec
            #         elif time_to_mn == event_time_mn:
            #             if time_to_day >= event_time_day:
            #                 exec
            #                 # return True
            #             else:
            #                 return False
            #         else:
            #             return False
            #     elif time_to_y > event_time_y :
            #         exec
            #         # return True
            #     else:
            #         return False

            #     if time_from_y == event_time_y:
            #         if time_from_mn < event_time_mn:
            #             return True
            #         elif time_from_mn == event_time_mn:
            #             if time_from_day <= event_time_day:
            #                 print(f'Day to {time_to_day} vs now day {event_time_day}')
            #                 return True
            #             else:
            #                 return False
            #         else:
            #             return False
            #     elif time_from_y < event_time_y:
            #         return True
            #     else:
            #         return False

            
            # if checkDate() == False :
            #     continue

            print(f'Event time - {event_time} | ID match : {event_half_id}')
            browser.switch_to.window(window_list[1])
            browser.get(f'https://www.flashscore.ua/match/{event_half_id}/#/match-summary/match-statistics')
            time.sleep(0.6)
            result = get_match_data(browser)
            result['country'] =  country
            result['season'] = season
            result['name'] = name_l
            print(f'Result data : {result}')
            result_data.append(result)
            time.sleep(0.1)
            browser.switch_to.window(window_list[0])
    try:
        name_writer = "result"
        if newM :
            name_writer = "calendar"
        # writer(result_data, name_writer)
        with open('./RESULT/data.json', 'r', encoding='utf-8') as file:
            total_data = json.load(file)
        total_data = total_data + result_data
        with open('./RESULT/data.json', 'w', encoding='utf-8') as file:
            json.dump(total_data, file, indent = 4)

    except Exception as e :
        print(f'Err in `writer` ~ | {e} |')
        traceback.print_exc()
        print(f'-------------------------')

data_test = [
    {
        "country" : "Україна",
        "ligue" : 'Друга ліга',
        "season": "Друга ліга 2022/2023",
        "href": "https://www.flashscore.ua/soccer/ukraine/premier-league-2021-2022/"
    }
]
# program(data_test)