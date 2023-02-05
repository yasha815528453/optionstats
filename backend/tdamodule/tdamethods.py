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
from database import methods as DBmethods

def make_webdriver():
        # Import selenium here because it's slow to import
        from selenium import webdriver

        driver = webdriver.Chrome("C:/Users/spam8/scanneranalyze/tdameri/chromedriver.exe")
        atexit.register(lambda: driver.quit())
        return driver


client = easy_client(toke.api_key, toke.redirect_url, toke.token_path, make_webdriver)



def initializeOptionData(symbol, strikesize, etf):
    datetoday = date.today()
    upPerformance = 0.1
    downPerformance = -0.1
    time_change = datetime.timedelta(days=730)
    if etf:
        isetf = "Y"
    else:
        isetf = "N"
    data = client.get_option_chain(symbol, strike_count=strikesize, include_quotes=True, from_date=datetoday, to_date= datetoday + time_change)
    datetoday = str(datetoday.year)+"-"+str(datetoday.month)+"-"+str(datetoday.day)
    for expDate in data.json()['putExpDateMap']:
        for strikeprice in data.json()['putExpDateMap'][expDate]:
            for item in data.json()['putExpDateMap'][expDate][strikeprice]:
                marketprice = item['mark']
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
                upperformance = (highprice/records[0]['absLow']) * 100
                downperformance = (lowprice/records[0]['absHigh']) * 100
                absLDate = records[0]['absLDate']
                absHDate = records[0]['absHDate']
                if records[0]['absLow'] > lowprice:
                    absLow = lowprice
                    absLDate = datetoday
                else:
                    absLow = records[0]['absLow']
                if records[0]['absHigh'] < highprice:
                    absHigh = highprice
                    absHDate = datetoday
                else:
                    absHigh = records[0]['absHigh']
                
                insertData = (optionkey, "P", symbol, marketprice, daystoexp, lowprice, highprice, lowprice, highprice, datetoday, datetoday, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetoday, upPerformance, downPerformance, isetf)
                sqlstmt = "INSERT INTO options (optionkey, type, SYMBOLS, marketprice, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, volume, oi, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance, etf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                DBmethods.execute(sqlstmt, insertData)

                

    for expDate in data.json()['callExpDateMap']:
        for strikeprice in data.json()['callExpDateMap'][expDate]:
            for item in data.json()['callExpDateMap'][expDate][strikeprice]:

                optionkey = item['symbol']
                records = DBmethods.checkOptionPK(optionkey)
                marketprice = item['mark']
                highprice = item['highPrice']
                lowprice = item['lowPrice']
                daystoexp = item['daysToExpiration']
                volatility = item['volatility']
                delta = item['delta']
                gamma = item['gamma']
                theta = item['theta']
                vega = item['vega']
                volume = item['volume']
                oi = item['openinterest']
                theorPrice = item['theoreticalOptionValue']
                if volatility=="NaN" or delta=="NaN" or gamma =="NaN" or theta=="NaN" or theorPrice=="NaN":
                    continue

                upperformance = (highprice/records[0]['absLow']) * 100
                downperformance = (lowprice/records[0]['absHigh']) * 100
                absLDate = records[0]['absLDate']
                absHDate = records[0]['absHDate']
                if records[0]['absLow'] > lowprice:
                    absLow = lowprice
                    absLDate = datetoday
                else:
                    absLow = records[0]['absLow']
                if records[0]['absHigh'] < highprice:
                    absHigh = highprice
                    absHDate = datetoday
                else:
                    absHigh = records[0]['absHigh']
                    
                insertData = (optionkey, "C", symbol, marketprice, daystoexp, lowprice, highprice, lowprice, highprice, datetoday, datetoday, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetoday, upPerformance, downPerformance, isetf)
                sqlstmt = "INSERT INTO options (optionkey, type, SYMBOLS, marketprice, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, volume, oi, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance, etf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                DBmethods.execute(sqlstmt, insertData)
                
                


# updating table -> get new data, use primary key to see if exists or not, 
## if exists, update the existing row; if not, then insert into database.
# after new data done, do delete operation on expired options, with 

def updateOptionData(symbol, strikesize, etf):
    datetoday = date.today()
    time_change = datetime.timedelta(days=730)
    data = client.get_option_chain(symbol, strike_count=strikesize, include_quotes=True, from_date=datetoday, to_date= datetoday + time_change)
    datetoday = str(datetoday.year)+"-"+str(datetoday.month)+"-"+str(datetoday.day)
    if etf:
        isetf = "Y"
    else:
        isetf = "N"
    for expDate in data.json()['putExpDateMap']:
        for strikeprice in data.json()['putExpDateMap'][expDate]:
            for item in data.json()['putExpDateMap'][expDate][strikeprice]:
                optionkey = item['symbol']
                marketprice = item['mark']
                records = DBmethods.checkOptionPK(optionkey)
                highprice = item['highPrice']
                lowprice = item['lowPrice']
                daystoexp = item['daysToExpiration']
                volatility = item['volatility']
                delta = item['delta']
                gamma = item['gamma']
                theta = item['theta']
                vega = item['vega']
                volume = item['volume']
                oi = item['openinterest']
                theorPrice = item['theoreticalOptionValue']
                if volatility=="NaN" or delta=="NaN" or gamma =="NaN" or theta=="NaN" or theorPrice=="NaN":
                    continue
                if records:
                    #records exists, so update it.
                    upperformance = (highprice/records[0]['absLow']) * 100
                    downperformance = (lowprice/records[0]['absHigh']) * 100
                    absLDate = records[0]['absLDate']
                    absHDate = records[0]['absHDate']
                    if records[0]['absLow'] > lowprice:
                        absLow = lowprice
                        absLDate = datetoday
                    else:
                        absLow = records[0]['absLow']
                    if records[0]['absHigh'] < highprice:
                        absHigh = highprice
                        absHDate = datetoday
                    else:
                        absHigh = records[0]['absHigh']
                    
                    # update daystoexp,  low,high price,  then conditionally absolute low,high price, then the respective dates. volatility, all the greeks, theorprice, lastupdate, up/down performance.
                    sqlstmt = "UPDATE options SET daysToExpiration = %s, markprice = %s, lowPrice = %s, highPrice = %s, absLow = %s, absHigh = %s, absLDate = %s, absHDate = %s, volatility = %s, volume = %s, oi = %s, delta = %s, gamma = %s, theta = %s, vega = %s, theoreticalOptionValue = %s, lastupdate = %s, upperformance = %s, downperformance = %s, etf = %s" 
                    updateData = (daystoexp, marketprice, lowprice, highprice, absLow, absHigh, absLDate, absHDate, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetoday, upperformance, downperformance, isetf)
                    DBmethods.execute(sqlstmt, updateData)

                else:
                    #record does not exist, insert it.
                    insertData = (optionkey, 'P', symbol, marketprice, daystoexp, lowprice, highprice, lowprice, highprice, datetoday, datetoday, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetoday, upperformance, downperformance, isetf)
                    sqlstmt = "INSERT INTO options (optionkey, type, SYMBOLS, marketprice, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, volume, oi, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance, etf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    DBmethods.execute(sqlstmt, insertData)

    for expDate in data.json()['callExpDateMap']:
        for strikeprice in data.json()['callExpDateMap'][expDate]:
            for item in data.json()['callExpDateMap'][expDate][strikeprice]:
                marketprice = item['mark']
                optionkey = item['symbol']
                records = DBmethods.checkOptionPK(optionkey)

                highprice = item['highPrice']
                lowprice = item['lowPrice']
                daystoexp = item['daysToExpiration']
                volatility = item['volatility']
                volume = item['volume']
                oi = item['openinterest']
                delta = item['delta']
                gamma = item['gamma']
                theta = item['theta']
                vega = item['vega']
                theorPrice = item['theoreticalOptionValue']
                if volatility=="NaN" or delta=="NaN" or gamma =="NaN" or theta=="NaN" or theorPrice=="NaN":
                    continue
                    
                if records:
                    upperformance = (highprice/records[0]['absLow']) * 100
                    downperformance = (lowprice/records[0]['absHigh']) * 100
                    absLDate = records[0]['absLDate']
                    absHDate = records[0]['absHDate']
                    if records[0]['absLow'] > lowprice:
                        absLow = lowprice
                        absLDate = datetoday
                    else:
                        absLow = records[0]['absLow']
                    if records[0]['absHigh'] < highprice:
                        absHigh = highprice
                        absHDate = datetoday
                    else:
                        absHigh = records[0]['absHigh']
                    
                    # update daystoexp,  low,high price,  then conditionally absolute low,high price, then the respective dates. volatility, all the greeks, theorprice, lastupdate, up/down performance.
                    sqlstmt = "UPDATE options SET daysToExpiration = %s, marketprice = %s, lowPrice = %s, highPrice = %s, absLow = %s, absHigh = %s, absLDate = %s, absHDate = %s, volatility = %s, volume = %s, oi = %s, delta = %s, gamma = %s, theta = %s, vega = %s, theoreticalOptionValue = %s, lastupdate = %s, upperformance = %s, downperformance = %s, etf = %s" 
                    updateData = (daystoexp, marketprice, lowprice, highprice, absLow, absHigh, absLDate, absHDate, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetoday, upperformance, downperformance, isetf)
                    DBmethods.execute(sqlstmt, updateData)
                
                else:
                    insertData = (optionkey, 'C', symbol, marketprice, daystoexp, lowprice, highprice, lowprice, highprice, datetoday, datetoday, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetoday, upperformance, downperformance, isetf)
                    sqlstmt = "INSERT INTO options (optionkey, type, SYMBOLS, marketprice, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, volume, oi, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance, etf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    DBmethods.execute(sqlstmt, insertData)
    

    # get marketopen[i forgot, 'hours?']
    # if closed, then dont update, 
    # if open, continue with all the updating, 
    
    # step 1, check open or not.
    # step 2, update rows, insert, etc.. 
    # step 3, only get rid of options that have expiration date of 0, and date is earlier than (todaysdate). 
    
    # should be able to function well, which is showing fresh insights on market days, monday after hours... friday afterhours,  
    # saturday sunday holidays will display the last trading day.
    # only the options that have expired, will not show up/update, and have different dates than new ones


def optionSize(ticker):
    size = 0
    largest = 0
    data = client.get_option_chain(ticker, from_date= date.today(), to_date= date.today() + datetime.timedelta(days=30))
    for expDate in data.json()['callExpDateMap']:
        for strikeprice in data.json()['callExpDateMap'][expDate]:
            for item in data.json()['callExpDateMap'][expDate][strikeprice]:
                if item['volume'] != 0 or item['openInterest'] != 0:
                    size += 1
        if size > largest:
            largest = size
        size = 0
    return largest

    



