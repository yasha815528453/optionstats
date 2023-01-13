import yahoo_fin.stock_info as yf
import pandas as pd
import atexit
from tda.auth import easy_client
from tda.client import Client
from tda.streaming import StreamClient
import tda
import datetime
from time import sleep
import json
from tdamodule import toke
from datetime import date
from database import methods

def make_webdriver():
        # Import selenium here because it's slow to import
        from selenium import webdriver

        driver = webdriver.Chrome("C:/Users/spam8/scanneranalyze/tdameri/chromedriver.exe")
        atexit.register(lambda: driver.quit())
        return driver


client = easy_client(toke.api_key, toke.redirect_url, toke.token_path, make_webdriver)


def givesize(symbol):
    volume =0
    oi = 0
    data = client.get_option_chain(symbol, strike_count=40, include_quotes=True, from_date=datetime.datetime(2023,1,3), to_date=datetime.datetime(2023,2,5))


    for item in data.json()["putExpDateMap"]:
        for each in data.json()["putExpDateMap"][item]:
            volume += data.json()["putExpDateMap"][item][each][0]["totalVolume"]
            oi += data.json()["putExpDateMap"][item][each][0]["openInterest"]

    for item in data.json()["callExpDateMap"]:
        for each in data.json()["callExpDateMap"][item]:
            volume += data.json()["callExpDateMap"][item][each][0]["totalVolume"]
            oi += data.json()["callExpDateMap"][item][each][0]["openInterest"]

    total = volume + oi

    if total>1000000:
        return 40
    elif total > 11000:
        return 25
    else:
        return 12

def initializeOptionData(symbol, strikesize):
    datetoday = date.today()
    upPerformance = 0.1
    downPerformance = -0.1
    time_change = datetime.timedelta(days=365)
    data = client.get_option_chain(symbol, strike_count=strikesize, include_quotes=True, from_date=datetoday, to_date= datetoday + time_change)
    datetoday = str(datetoday.year)+"-"+str(datetoday.month)+"-"+str(datetoday.day)
    for expDate in data.json()['putExpDateMap']:
        for strikeprice in data.json()['putExpDateMap'][expDate]:
            for item in data.json()['putExpDateMap'][expDate][strikeprice]:
                optionkey = item['symbol']
                highprice = item['highPrice']
                lowprice = item['lowPrice']
                daystoexp = item['daysToExpiration']
                volatility = item['volatility']
                delta = item['delta']
                gamma = item['gamma']
                theta = item['theta']
                vega = item['vega']
                theorPrice = item['theoreticalOptionValue']
                if volatility=="NaN" or delta=="NaN" or gamma =="NaN" or theta=="NaN" or theorPrice=="NaN":
                    continue
                insertData = (optionkey, symbol, daystoexp, lowprice, highprice, lowprice, highprice, datetoday, datetoday, volatility, delta, gamma, theta, vega, theorPrice, datetoday, upPerformance, downPerformance)
                sqlstmt = "INSERT INTO options (optionkey, SYMBOLS, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                methods.execute(sqlstmt, insertData)
    for expDate in data.json()['callExpDateMap']:
        for strikeprice in data.json()['callExpDateMap'][expDate]:
            for item in data.json()['callExpDateMap'][expDate][strikeprice]:
                optionkey = item['symbol']
                highprice = item['highPrice']
                lowprice = item['lowPrice']
                daystoexp = item['daysToExpiration']
                volatility = item['volatility']
                delta = item['delta']
                gamma = item['gamma']
                theta = item['theta']
                vega = item['vega']
                theorPrice = item['theoreticalOptionValue']
                if volatility=="NaN" or delta=="NaN" or gamma =="NaN" or theta=="NaN" or theorPrice=="NaN":
                    continue
                insertData = (optionkey, symbol, daystoexp, lowprice, highprice, lowprice, highprice, datetoday, datetoday, volatility, delta, gamma, theta, vega, theorPrice, datetoday, upPerformance, downPerformance)
                sqlstmt = "INSERT INTO options (optionkey, SYMBOLS, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                methods.execute(sqlstmt, insertData)
