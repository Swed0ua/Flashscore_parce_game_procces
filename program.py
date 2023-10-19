import eel
import json
import traceback
from py import program
import multiprocessing
from fl_writer import writer

@eel.expose
def get_seasons_data():
    with open('leagues_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    # print(data)
    return data

def refact_list_data (data):
    nw_res = []
    for item in data:
        item_txt = item.split('/')
        max_sum = 6
        nw_text = ''
        for nm in range(0, max_sum):
            nw_text += item_txt[nm] + '/'
        nw_res.append(nw_text)
    print(nw_res)
    return nw_res

@eel.expose
def get_list_data():
    with open('./DATA/list.txt', 'r', encoding='utf-8') as file:
        res = file.read()
    return res.split('\n')

@eel.expose
def set_list_data(data):
    txt = ''
    for item in data:
        txt += item + ' \n'
    with open('./DATA/list.txt', 'w', encoding='utf-8') as file:
        file.read(txt)

@eel.expose
def get_listcount_data():
    with open('list.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

@eel.expose
def set_listcount_data(value):
    data = get_listcount_data()
    data['count'] = int(value)
    with open('list.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent = 4)
    return data
    

@eel.expose
def start(data, act, value):
    dt = get_list_data()
    nw_dt = refact_list_data(dt)
    set_listcount_data(value)
    count_prog = int(value)
    if count_prog > len(nw_dt):
        count_prog = len(nw_dt)
    dt_check = []
    td_count = 0
    for ind in range(0, count_prog):
        dt_check.append([])
    for ind in range(0, len(nw_dt)):
        print(td_count)
        dt_check[td_count].append(nw_dt[ind])
        if td_count < count_prog-1:
            td_count += 1
        else:
            td_count = 0
    try:
        processes = [multiprocessing.Process(target=program, args=[dt_check, act]) for _ in range(count_prog)]
        for process in processes:
            process.start()
        for process in processes:
            process.join()
        
        name_writer = "result"
        if act :
            name_writer = "calendar"
        
        with open('./RESULT/data.json', 'r', encoding='utf-8') as file:
            total_data = json.load(file)
        writer(total_data, name_writer)
        
        
        # program(nw_dt, act)
        return True
    except Exception as e:
        traceback.print_exc()
        print(f'Err ~ | {e} |')
        return False
    

    
if __name__ == '__main__':
    eel.init('web')
    eel.start('index.html')