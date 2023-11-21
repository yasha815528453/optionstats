import yahoo_fin.stock_info as yf
import pandas as pd
import atexit
from tda.auth import easy_client
from tda.client import Client
from tda.streaming import StreamClient
import tda
import datetime
from datetime import date
from time import sleep
import json
import yahoo_fin.stock_info as yf
import ratelimit
import csv
import traceback
from dotenv import load_dotenv
import os
import toke
# from tdamethods import TdaClient
load_dotenv()
def make_webdriver():
        # Import selenium here because it's slow to import
        from selenium import webdriver

        driver = webdriver.Chrome("chromedriver.exe")
        atexit.register(lambda: driver.quit())
        return driver

datetoday = date.today()
datetodayinsert = str(datetoday.year)+"-"+str(datetoday.month)+"-"+str(datetoday.day)
time_change = datetime.timedelta(days=730)
client = easy_client(toke.api_key, toke.redirect_url, toke.token_path, make_webdriver)
limiter = ratelimit.RateLimiter(rate_limit=120, time_window=60)
# data = client.get_option_chain("SPY")
# print(len(data.json()['callExpDateMap']["2024-02-16:115"]))
# seconddata = client.get_price_history_every_minute("SPY", start_datetime=datetime.datetime.today(), end_datetime=datetime.datetime.today())
# class_path = os.path.abspath(__file__)
# class_dir = os.path.dirname(class_path)
# parent_dir = os.path.join(class_dir, '..')

# optional_stock_csv_path = os.path.join(parent_dir, 'stock_list.csv')
# # print(seconddata.json()['candles'][554]['close'])

# # Tdaclient = TdaClient()
# data = client.get_option_chain("MARA")
# data = data.json()
# print(data)

# # data = client.get_quote("SPY")
# # print(data.json())

# # lel = [[1,2,3], [3,4,5], ["rofl","lmao","lel"]]
# with open(optional_stock_csv_path, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(data)
# with open(optional_stock_csv_path, mode='r', newline='') as file:
#     reader = csv.reader(file)
#     print(list(reader))



# for dates, strike in data.json()['putExpDateMap'].items():
#         print(dates, '    :   ', len(strike.keys()))

data = client.get_option_chain("BITO")
with open ('temp.json', 'w') as file:
        json.dump(data.json(), file, indent=4)
# data = data.json()['putExpDateMap']

# for i, j in data.items():
#         for dates, strikes in j.items():
#                 if strikes[0]['inTheMoney'] == true:
#                         print("lol")
#  def func(timestamp):
# ...  temp = timestamp/1000
# ...  dt = datetime.datetime.fromtimestamp(temp)
# ...  print(dt)

# data = client.get_option_chain("AACG")
# print(data.json())
# data = client.get_quote("AACG")
# print(data.json())
# stocklis = yf.tickers_nasdaq() + yf.tickers_other()
# print(stocklis)
# seen = set()
# stocklis = [s for s in stocklis if all(c not in s for c in "$.") and not (s in seen or seen.add(s))]

# newlist = []

# for symb in stocklis:
#     for retry in range(5):
#         if limiter.get_token():
#             data = client.get_option_chain(symb)
#             if data.json()['status'] == 'FAILED':
#                 print(symb + " has failed")
#                 break

#             else:
#                 newlist.append(symb)
#                 break
#         else:
#             sleep(0.5)
# newnewlist = []
# for sym in newlist:
#     for retry in range(5):
#         if limiter.get_token():
#             data = client.get_quote(sym)
#             if data.json()[sym]['closePrice'] < 1.0:
#                 print("noob stock = " + sym)
#                 break
#             else:
#                 newnewlist.append(sym)
#         else:
#             sleep(0.5)

# print(len(newnewlist))
# print(newnewlist)


# def optionSize(ticker):
#     size = 0
#     sizetwo = 0
#     largest = 0
#     largesttwo = 0
#     smallest = 1000
#     dat = "lel"
#     smallesttwo = 1000
#     data = client.get_option_chain(ticker, from_date= date.today(), to_date= date.today() + datetime.timedelta(days=365))
#     data = data.json()
#     for expDate in data['callExpDateMap']:
#         for strikeprice in data['callExpDateMap'][expDate]:
#             for item in data['callExpDateMap'][expDate][strikeprice]:
#                 if item['totalVolume'] >= 10 or item['openInterest'] >= 10:
#                     size += 1
#         if size < smallest:
#             smallest = size
#             dat = expDate
#         if size > largest:
#             largest = size
#         size = 0

#     if size % 2 == 0 and size > 10:
#         size += 1
#     elif size >= 60:
#         size = 60
#     elif size < 10:
#         size = 10

#     return (str(smallest) + '  siz1 -  siz2 '  + str(largest))


# print(optionSize("AMZN"))
