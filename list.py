import datetime


items = [
    {"date" : datetime.datetime(2001, 1, 1)},
    {"date" : datetime.datetime(1998,5, 1)},
    {"date" : datetime.datetime(2000,5, 1)}
]

sorted_data = sorted(items, key=lambda x: x["date"])

print(sorted_data)
