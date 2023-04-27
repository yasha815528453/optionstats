from database import methods
from scrape import scrapeclient
from tdamodule import tdamethods
import pandas as pd
from datetime import date
import datetime
from tdamodule import ratelimit

def initialize():
    connection = methods.acquire_connection()
    df = pd.read_csv("liquidoptions5.csv")
    for i in range(len(df)):
        if df.iloc[i]['ETF'] == 'N':
            try:
                ticker = df.iloc[i]['Symbol']
                sector, industry, country = scrapeclient.get_sector_industry_country(ticker)
                size = tdamethods.optionSize(ticker)
                data = (ticker, sector, industry, country, size, 'initialize', 1.1, 1.1, 10.0)

                sql = "INSERT INTO tickersS (SYMBOLS, SECTORS, industry, country, OptionSize, description, pricechange, percentchange, closingprice) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                methods.execute(sql, data, connection)

            except Exception as e:
                print(data)
                print(ticker)
                print(e)


        else:
            try:
                ticker = df.iloc[i]['Symbol']
                category = scrapeclient.get_category(ticker)
                size = tdamethods.optionSize(ticker)
                data = (ticker, category, size, 'initialize', 1.1, 1.1, 10.0)
                sql = "INSERT INTO tickersE (SYMBOLS, CATEGORY, OptionSize, description, pricechange, percentchange, closingprice) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                methods.execute(sql, data, connection)
            except Exception as e:
                print(data)
                print(ticker)
                print(e)

    limiter = ratelimit.RateLimiter(rate_limit=120, time_window=60)
    datetoday = date.today()
    datetodayinsert = str(datetoday.year)+"-"+str(datetoday.month)+"-"+str(datetoday.day)
    time_change = datetime.timedelta(days=730)
    records = methods.getETF(connection)
    count = 0
    for stock in records:
        count += 1
        print(count)
        tdamethods.initializeOptionData(stock['SYMBOLS'], stock['OptionSize'], True, datetoday, datetodayinsert, time_change, limiter)

    stockrecords = methods.getStock(connection)
    for stock in stockrecords:
        tdamethods.initializeOptionData(stock['SYMBOLS'], stock['OptionSize'], False, datetoday, datetodayinsert, time_change, limiter)
    methods.release_connection(connection)

initialize()
# methods.deleteALL("options")
