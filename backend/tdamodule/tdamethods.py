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
import pandas as pd
from tdamodule import ratelimit
from time import sleep
import traceback
import os

class TdaClient:
    def __init__(self):
        self.client = easy_client(os.getenv("API_KEY"), os.getenv("REDIRECT_URL"), os.getenv("TOKEN_PATH", self.make_webdriver))

    def make_webdriver():
            # Import selenium here because it's slow to import
            from selenium import webdriver

            driver = webdriver.Chrome("chromedriver.exe")
            atexit.register(lambda: driver.quit())
            return driver

def make_webdriver():
        # Import selenium here because it's slow to import
        from selenium import webdriver

        driver = webdriver.Chrome("chromedriver.exe")
        atexit.register(lambda: driver.quit())
        return driver

client = easy_client(toke.api_key, toke.redirect_url, toke.token_path, make_webdriver)

def initializeOptionData(symbol, strikesize, etf, datetoday, datetodayinsert, time_change, limiter):
    connection = DBmethods.acquire_connection()
    upPerformance = 0
    downPerformance = 0


    lastputvola = 30
    lastputdelta = -0.45
    lastputgamma = 0.05
    lastputtheta = -0.04
    lastputrho = -0.05
    lastputtheor = 5

    lastcallvola = 30
    lastcalldelta = 0.45
    lastcallgamma =0.05
    lastcallthetha = -0.04
    lastcallrho = 0.05
    lastcalltheor = 5
    delta = 0.5
    gamma = 0.3
    volatility = 35.1
    vega = 0.001
    theta = -0.003
    rho = -0.001
    if etf:
        isetf = "Y"
    else:
        isetf = "N"
    try:
        for retry in range(5):
            if limiter.get_token():
                data = client.get_option_chain(symbol, strike_count=strikesize, include_quotes=True, from_date=datetoday, to_date= datetoday + time_change)
                data = data.json()
                break
            else:
                sleep(0.5)

        description = data['underlying']['description']
        pricechange = data['underlying']['change']
        percentchange = data['underlying']['percentChange']
        stockprice = data['underlying']['close']
        DBmethods.updateprice(symbol, (description, pricechange, percentchange, stockprice), etf, connection)
        datetoday = str(datetoday.year)+"-"+str(datetoday.month)+"-"+str(datetoday.day)
        for expDate, items in data['putExpDateMap'].items():
            for strikeprice, valuez in items.items():
                item = valuez[0]
                strike = float(strikeprice)


                marketprice = item['mark']
                optionkey = item['symbol']
                highprice = item['highPrice']
                lowprice = item['lowPrice']
                daystoexp = item['daysToExpiration']
                if item['volatility'] == -999:
                    pass
                else:
                    volatility = item['volatility']
                if item['delta'] == -999:
                    pass
                else:
                    delta = item['delta']
                if item['gamma'] == -999:
                    pass
                else:
                    gamma = item['gamma']
                if item['theta'] == -999:
                    pass
                else:
                    theta = item['theta']
                if item['vega'] == -999:
                    pass
                else:
                    vega = item['vega']
                bid = item['bid']
                ask = item['ask']
                if item['rho'] == -999:
                    pass
                else:
                    rho = item['rho']
                oi = item['openInterest']
                volume = item['totalVolume']
                last = item['last']
                if lowprice == 0 and last != 0:
                    lowprice = last

                if highprice == 0 and last != 0:
                    highprice = last

                theorPrice = item['theoreticalOptionValue']
                if volatility == "NaN" or delta == "NaN" or gamma == "NaN" or theta == "NaN" or rho == "NaN" or theorPrice == "NaN":
                    volatility, delta, gamma, theta, rho, theorPrice = lastputvola, lastputdelta, lastputgamma, lastputtheta, lastputrho, lastputtheor
                if volume == 0:
                    insertData = (optionkey, "P", symbol, strike, marketprice, bid, ask, daystoexp, lowprice, highprice, lowprice, highprice, datetoday, datetoday, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetodayinsert, 0, 0, rho, isetf)
                    sqlstmt = "INSERT INTO options (optionkey, type, SYMBOLS, strikeprice, marketprice, bid, ask, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, volume, openinterest, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance, rho, isetf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    DBmethods.execute(sqlstmt, insertData, connection)
                else:
                    insertData = (optionkey, "P", symbol, strike, marketprice, bid, ask, daystoexp, lowprice, highprice, lowprice, highprice, datetoday, datetoday, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetodayinsert, upPerformance, downPerformance, rho, isetf)
                    sqlstmt = "INSERT INTO options (optionkey, type, SYMBOLS, strikeprice, marketprice, bid, ask, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, volume, openinterest, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance, rho, isetf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    DBmethods.execute(sqlstmt, insertData, connection)

                lastputvola = volatility
                lastputdelta = delta
                lastputgamma = gamma
                lastputtheta = theta
                lastputrho = rho
                lastputtheor = theorPrice



        for expDate, items in data['callExpDateMap'].items():
            for strikeprice, valuez in items.items():
                item = valuez[0]
                strike = float(strikeprice)
                optionkey = item['symbol']
                marketprice = item['mark']
                highprice = item['highPrice']
                lowprice = item['lowPrice']
                daystoexp = item['daysToExpiration']
                if item['volatility'] == -999:
                    pass
                else:
                    volatility = item['volatility']
                if item['delta'] == -999:
                    pass
                else:
                    delta = item['delta']
                if item['gamma'] == -999:
                    pass
                else:
                    gamma = item['gamma']
                if item['theta'] == -999:
                    pass
                else:
                    theta = item['theta']
                if item['vega'] == -999:
                    pass
                else:
                    vega = item['vega']
                if item['rho'] == -999:
                    pass
                else:
                    rho = item['rho']
                volume = item['totalVolume']
                oi = item['openInterest']
                theorPrice = item['theoreticalOptionValue']
                bid = item['bid']
                ask = item['ask']

                last = item['last']
                if lowprice == 0 and last != 0:
                    lowprice = last

                if highprice == 0 and last != 0:
                    highprice = last

                if volatility == "NaN" or delta == "NaN" or gamma == "NaN" or theta == "NaN" or rho == "NaN":
                    volatility, delta, gamma, theta, rho, theorPrice = lastcallvola, lastcalldelta, lastcallgamma, lastcallthetha, lastcallrho, lastcalltheor

                if volume == 0:
                    insertData = (optionkey, "C", symbol, strike, marketprice, bid, ask, daystoexp, lowprice, highprice, lowprice, highprice, datetoday, datetoday, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetodayinsert, 0, 0, rho, isetf)
                    sqlstmt = "INSERT INTO options (optionkey, type, SYMBOLS, strikeprice, marketprice, bid, ask, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, volume, openinterest, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance, rho, isetf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    DBmethods.execute(sqlstmt, insertData, connection)
                else:

                    insertData = (optionkey, "C", symbol, strike, marketprice, bid, ask, daystoexp, lowprice, highprice, lowprice, highprice, datetoday, datetoday, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetodayinsert, upPerformance, downPerformance, rho, isetf)
                    sqlstmt = "INSERT INTO options (optionkey, type, SYMBOLS, strikeprice, marketprice, bid, ask, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, volume, openinterest, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance, rho, isetf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    DBmethods.execute(sqlstmt, insertData, connection)

                lastcallvola = volatility
                lastcalldelta = delta
                lastcallgamma = gamma
                lastcallthetha = theta
                lastcallrho = rho
                lastcalltheor = theorPrice
    except Exception as e:
        print(symbol)
        print(e)
        print(data)
    finally:
        DBmethods.release_connection(connection)







# updating table -> get new data, use primary key to see if exists or not,
## if exists, update the existing row; if not, then insert into database.
# after new data done, do delete operation on expired options, with

def updateOptionData(symbol, strikesize, etf):
    datetoday = date.today()
    time_change = datetime.timedelta(days=730)
    connection1 = DBmethods.acquire_connection()
    limiter = ratelimit.RateLimiter(rate_limit=120, time_window=60)
    lastputvola = 30
    lastputdelta = -0.45
    lastputgamma = 0.05
    lastputtheta = -0.04
    lastputrho = -0.05
    lastputtheor = 5
    lastcallvola = 30
    lastcalldelta = 0.45
    lastcallgamma =0.05
    lastcallthetha = -0.04
    lastcallrho = 0.05
    lastcalltheor = 5
    delta = 0.5
    gamma = 0.3
    volatility = 35.1
    vega = 0.001
    theta = -0.003
    rho = -0.001
    if etf:
        isetf = "Y"
    else:
        isetf = "N"
    try:

        for retry in range(5):
            if limiter.get_token():
                data = client.get_option_chain(symbol, strike_count=strikesize, include_quotes=True, from_date=datetoday, to_date= datetoday + time_change)
                break
            else:
                sleep(0.5)
        description = data.json()['underlying']['description']
        pricechange = data.json()['underlying']['change']
        percentchange = data.json()['underlying']['percentChange']
        stockprice = data.json()['underlying']['close']


        DBmethods.updateprice(symbol, (description, pricechange, percentchange, stockprice), etf, connection1)
        data = data.json()
        datetoday = str(datetoday.year)+"-"+str(datetoday.month)+"-"+str(datetoday.day)
        for expDate, items in data['putExpDateMap'].items():
            for strikeprice, valuez in items.items():
                strike = float(strikeprice)
                item = valuez[0]
                optionkey = item['symbol']
                marketprice = item['mark']

                records = DBmethods.checkOptionPK(optionkey, connection1)

                highprice = item['bid']
                lowprice = item['ask']
                daystoexp = item['daysToExpiration']
                if item['volatility'] == -999:
                    pass
                else:
                    volatility = item['volatility']
                if item['delta'] == -999:
                    pass
                else:
                    delta = item['delta']
                if item['gamma'] == -999:
                    pass
                else:
                    gamma = item['gamma']
                if item['theta'] == -999:
                    pass
                else:
                    theta = item['theta']
                if item['vega'] == -999:
                    pass
                else:
                    vega = item['vega']
                volume = item['totalVolume']
                oi = item['openInterest']
                theorPrice = item['theoreticalOptionValue']
                bid = item['bid']
                ask = item['ask']

                if item['rho'] == -999:
                    pass
                else:
                    rho = item['rho']
                last = item['last']
                if lowprice == 0 and last != 0:
                    lowprice = last
                if highprice == 0 and last != 0:
                    highprice = last

                if volatility == "NaN" or delta == "NaN" or gamma == "NaN" or theta == "NaN" or rho == "NaN" or theorPrice == "NaN":
                    volatility, delta, gamma, theta, rho, theorPrice = lastputvola, lastputdelta, lastputgamma, lastputtheta, lastputrho, lastputtheor

                if volume == 0:
                    if records:
                        sqlstmt = "UPDATE options SET marketprice = %s, bid = %s, ask = %s, daysToExpiration = %s, upperformance = %s, downperformance = %s WHERE optionkey = %s"
                        # get upperformance and down to 0, no performance, flat.
                        upperformance = 10
                        downperformance = -10
                        updateData = (marketprice, bid, ask, daystoexp, upperformance, downperformance, optionkey)

                        DBmethods.execute(sqlstmt, updateData, connection1)
                        continue
                    else:
                        insertData = (optionkey, 'P', symbol, strike, marketprice, bid, ask, daystoexp, lowprice, highprice, lowprice, highprice, datetoday, datetoday, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetoday, 0, 100, rho, isetf)
                        sqlstmt = "INSERT INTO options (optionkey, type, SYMBOLS, strikeprice, marketprice, bid, ask, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, volume, openinterest, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance, rho, isetf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        DBmethods.execute(sqlstmt, insertData, connection1)
                        continue

                if records:
                    #records exists, so update it.

                    absLDate = records[0]['absLDate']
                    absHDate = records[0]['absHDate']

                    #updating the new absolute high/low out of todays and befores.

                    if records[0]['absLow'] == 0:

                        upperformance = 10
                    else:
                        upperformance = round((highprice/records[0]['absLow']) * 100, 1)

                    if records[0]['absHigh'] == 0:
                        downperformance = -10
                    else:
                        downperformance = round((lowprice - records[0]['absHigh'])/records[0]['absHigh'] * 100, 1)

                    if daystoexp != 0:

                        if item['lowPrice'] <= records[0]['absLow']:
                            absLow = item['lowPrice']
                            absLDate = datetoday
                        else:
                            absLow = records[0]['absLow']
                            absLDate = records[0]['absLDate']

                        if item['highPrice'] >= records[0]['absHigh']:
                            absHigh = item['highPrice']
                            absHDate = datetoday
                        else:
                            absHigh = records[0]['absHigh']
                            absHDate = records[0]['absHDate']
                    else:
                        absLow = 9999
                        absHigh = 0.01

                    #get todays performance, if abslow or abshigh is 0, then no performance.



                    # update daystoexp,  low,high price,  then conditionally absolute low,high price, then the respective dates. volatility, all the greeks, theorprice, lastupdate, up/down performance.
                    sqlstmt = "UPDATE options SET daysToExpiration = %s, marketprice = %s, bid = %s, ask = %s, lowPrice = %s, highPrice = %s, absLow = %s, absHigh = %s, absLDate = %s, absHDate = %s, volatility = %s, volume = %s, openinterest = %s, delta = %s, gamma = %s, theta = %s, vega = %s, theoreticalOptionValue = %s, lastupdate = %s, upperformance = %s, downperformance = %s, rho = %s, isetf = %s WHERE optionkey = %s"
                    updateData = (daystoexp, marketprice, bid, ask, lowprice, highprice, absLow, absHigh, absLDate, absHDate, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetoday, upperformance, downperformance, rho, isetf, optionkey)
                    DBmethods.execute(sqlstmt, updateData, connection1)

                else:

                    #record does not exist, insert it.
                    insertData = (optionkey, 'P', symbol, strike, marketprice, bid, ask, daystoexp, lowprice, highprice, lowprice, highprice, datetoday, datetoday, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetoday, 0, 100, rho, isetf)


                    sqlstmt = "INSERT INTO options (optionkey, type, SYMBOLS, strikeprice, marketprice, bid, ask, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, volume, openinterest, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance, rho, isetf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                    DBmethods.execute(sqlstmt, insertData, connection1)
                lastputvola = volatility
                lastputdelta = delta
                lastputgamma = gamma
                lastputtheta = theta
                lastputrho = rho
                lastputtheor = theorPrice


        for expDate, items in data['callExpDateMap'].items():
            for strikeprice, valuez in items.items():
                strike = float(strikeprice)
                item = valuez[0]
                marketprice = item['mark']
                optionkey = item['symbol']
                records = DBmethods.checkOptionPK(optionkey, connection1)
                highprice = item['bid']
                lowprice = item['ask']
                daystoexp = item['daysToExpiration']
                if item['volatility'] == -999:
                    pass
                else:
                    volatility = item['volatility']
                if item['delta'] == -999:
                    pass
                else:
                    delta = item['delta']
                if item['gamma'] == -999:
                    pass
                else:
                    gamma = item['gamma']
                if item['theta'] == -999:
                    pass
                else:
                    theta = item['theta']
                if item['vega'] == -999:
                    pass
                else:
                    vega = item['vega']
                if item['rho'] == -999:
                    pass
                else:
                    rho = item['rho']
                volume = item['totalVolume']
                oi = item['openInterest']

                bid = item['bid']
                ask = item['ask']
                theorPrice = item['theoreticalOptionValue']
                last = item['last']
                if lowprice == 0 and last != 0:
                    lowprice = last
                if highprice == 0 and last != 0:
                    highprice = last

                if volatility == "NaN" or delta == "NaN" or gamma == "NaN" or theta == "NaN" or rho == "NaN" or theorPrice == "NaN":
                    volatility, delta, gamma, theta, rho, theorPrice = lastcallvola, lastcalldelta, lastcallgamma, lastcallthetha, lastcallrho, lastcalltheor

                if volume == 0:
                    if records:
                        sqlstmt = "UPDATE options SET marketprice = %s, bid = %s, ask = %s, daysToExpiration = %s, upperformance = %s, downperformance = %s WHERE optionkey = %s"
                        # get upperformance and down to 0, no performance, flat.
                        upperformance = 10
                        downperformance = -10
                        updateData = (marketprice, bid, ask, daystoexp, upperformance, downperformance, optionkey)
                        DBmethods.execute(sqlstmt, updateData, connection1)

                        continue
                    else:
                        insertData = (optionkey, 'C', symbol, strike, marketprice, bid, ask, daystoexp, lowprice, highprice, lowprice, highprice, datetoday, datetoday, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetoday, 0, 100, rho, isetf)

                        sqlstmt = "INSERT INTO options (optionkey, type, SYMBOLS, strikeprice, marketprice, bid, ask, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, volume, openinterest, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance, rho, isetf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        DBmethods.execute(sqlstmt, insertData, connection1)
                        continue

                if records:

                    absLDate = records[0]['absLDate']
                    absHDate = records[0]['absHDate']

                    #updating the new absolute high/low out of todays and befores.
                    if records[0]['absLow'] == 0:
                        upperformance = 0
                    else:
                        upperformance = round((highprice/records[0]['absLow']) * 100, 1)

                    if records[0]['absHigh'] == 0:
                        downperformance = 100
                    else:
                        downperformance = round((lowprice - records[0]['absHigh'])/records[0]['absHigh'] * 100, 1)


                    if daystoexp != 0:

                        if item['lowPrice'] <= records[0]['absLow']:
                            absLow = item['lowPrice']
                            absLDate = datetoday
                        else:
                            absLow = records[0]['absLow']
                            absLDate = records[0]['absLDate']

                        if item['highPrice'] >= records[0]['absHigh']:
                            absHigh = item['highPrice']
                            absHDate = datetoday

                        else:
                            absHigh = records[0]['absHigh']
                            absHDate = records[0]['absHDate']
                    else:
                        absLow = 9999
                        absHigh = 0.01


                    #get todays performance, if abslow or abshigh is 0, then no performance.



                    # update daystoexp,  low,high price,  then conditionally absolute low,high price, then the respective dates. volatility, all the greeks, theorprice, lastupdate, up/down performance.
                    sqlstmt = "UPDATE options SET daysToExpiration = %s, marketprice = %s, bid = %s, ask = %s, lowPrice = %s, highPrice = %s, absLow = %s, absHigh = %s, absLDate = %s, absHDate = %s, volatility = %s, volume = %s, openinterest = %s, delta = %s, gamma = %s, theta = %s, vega = %s, theoreticalOptionValue = %s, lastupdate = %s, upperformance = %s, downperformance = %s, rho = %s, isetf = %s WHERE optionkey = %s"
                    updateData = (daystoexp, marketprice, bid, ask, lowprice, highprice, absLow, absHigh, absLDate, absHDate, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetoday, upperformance, downperformance, rho, isetf, optionkey)
                    DBmethods.execute(sqlstmt, updateData, connection1)

                else:
                    insertData = (optionkey, 'C', symbol, strike, marketprice, bid, ask, daystoexp, lowprice, highprice, lowprice, highprice, datetoday, datetoday, volatility, volume, oi, delta, gamma, theta, vega, theorPrice, datetoday, 0, 100, rho, isetf)
                    sqlstmt = "INSERT INTO options (optionkey, type, SYMBOLS, strikeprice, marketprice, bid, ask, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, volume, openinterest, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance, rho, isetf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    DBmethods.execute(sqlstmt, insertData, connection1)
                lastcallvola = volatility
                lastcalldelta = delta
                lastcallgamma =gamma
                lastcallthetha = theta
                lastcallrho = rho
                lastcalltheor = theorPrice
        return 10
    except Exception as e:
        print(symbol)
        print(e)
        print(type(e))
        traceback.print_tb(e.__traceback__)
        print(data)
    finally:
        DBmethods.release_connection(connection1)



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
    smallest = 1000
    data = client.get_option_chain(ticker, from_date= date.today(), to_date= date.today() + datetime.timedelta(days=30))
    for expDate in data.json()['callExpDateMap']:
        for strikeprice in data.json()['callExpDateMap'][expDate]:
            for item in data.json()['callExpDateMap'][expDate][strikeprice]:
                if item['totalVolume'] != 0 or item['openInterest'] != 0:
                    size += 1
        if size < smallest:
            smallest = size
        if size > largest:
            largest = size
        size = 0
    size = (smallest + largest)//2
    if size % 2 == 0 and size > 10:
        size += 1
    if size >= 40:
        size = 39
    return size
