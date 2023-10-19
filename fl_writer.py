import xlsxwriter
import time
import datetime

def writer(parametr, name):
    category_name = name
    category_name_refact = category_name.replace(' ', '_')
    book = xlsxwriter.Workbook(f'./RESULT/{category_name_refact}.xlsx', {'strings_to_numbers': True})
    page = book.add_worksheet('products')

    row = 1
    column = 0
    
    # ширина колонок
    page.set_column("A:A", 20)
    page.set_column("B:B", 20)
    page.set_column("C:C", 20)
    page.set_column("D:D", 20)
    page.set_column("E:E", 20)
    page.set_column("F:F", 20)
    page.set_column("G:G", 20)
    page.set_column("H:H", 20)
    page.set_column("I:I", 20)
    page.set_column("J:J", 20)
    page.set_column("K:K", 20)
    page.set_column("L:L", 20)
    page.set_column("M:M", 20)
    page.set_column("N:N", 20)
    page.set_column("O:O", 20)
    page.set_column("P:P", 20)
    page.set_column("Q:Q", 20)
    page.set_column("R:R", 20)
    page.set_column("S:S", 20)
    page.set_column("T:T", 20)

    page.write(0, 0, 'Страна')
    page.write(0, 1, 'Лига')
    page.write(0, 2, 'Сезон')
    page.write(0, 3, 'Тур')
    page.write(0, 4, 'Дата')
    page.write(0, 5, 'Команда 1')
    page.write(0, 6, 'Команда 2')
    page.write(0, 7, 'Счет команда 1')
    page.write(0, 8, 'Счет команда 2')
    page.write(0, 9, 'Владение мячом команда 1')
    page.write(0, 10, 'Владение мячом команда 2')
    page.write(0, 11, 'Удары команда 1')
    page.write(0, 12, 'Удары команда 2')
    page.write(0, 13, 'Атаки команда 1')
    page.write(0, 14, 'Атаки команда 2')
    page.write(0, 15, 'Опасные атаки команда 1')
    page.write(0, 16, 'Опасные атаки команда 2')
    page.write(0, 17, 'Коэф 1')
    page.write(0, 18, 'Коэф X')
    page.write(0, 19, 'Коэф 2')

    count = 0

    sorted_data = sorted(parametr, key=lambda x: x["date"]) 


    for item in sorted_data:
        count += 1
        # print(f"{item[1]} ({count})")
        page.write(row, column, item["country"])
        page.write(row, column + 1, item['name'])
        page.write(row, column + 2, item["season"])
        page.write(row, column + 3, item['tour'])
        
        if item["date"] == '':
            page.write(row, column + 4, item["date"])
        else:
            page.write_datetime(row, column + 4, datetime.datetime(int(item["date"][2]), int(item["date"][1]), int(item["date"][0])), book.add_format({'num_format': 'dd/mm/yyyy'}))
            
        page.write(row, column + 5, item["name_1"])
        page.write(row, column + 6, item["name_2"])
        page.write(row, column + 7, item["score_1"])
        page.write(row, column + 8, item["score_2"])
        page.write(row, column + 9, item['poss_1'] , book.add_format({'num_format': '0%'}))
        page.write(row, column + 10, item["poss_2"], book.add_format({'num_format': '0%'}))
        page.write(row, column + 11, item["shot_1"])
        page.write(row, column + 12, item["shot_2"])
        page.write(row, column + 13, item["atach_1"])
        page.write(row, column + 14, item["atach_2"])
        page.write(row, column + 15, item["den_atach_1"])
        page.write(row, column + 16, item["den_atach_2"])
        page.write(row, column + 17, item["cof1"])
        page.write(row, column + 18, item["cofx"])
        page.write(row, column + 19, item["cof2"])
        row += 1

    book.close()
