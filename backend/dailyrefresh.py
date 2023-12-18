from database import database_client
from tdamodule import tdamethods
import pandas_market_calendars as mcal
from datetime import date
from tdamodule import tdamethods
from stockanalyzer import analytics
from dotenv import load_dotenv
from utility import string_util
import time
import pandas as pd
import traceback

load_dotenv()
"""
refresh the big option table daily, first.
then the sub tables.
"""

## example ->
#  call refreshtable()
## then refreshtableOthers()...
# frontend uses the other tables.

datetoday = date.today()
market = mcal.get_calendar('NYSE')
marketopenlis = market.valid_days(start_date=datetoday, end_date=datetoday)
marketopenlis = marketopenlis.to_list
marketopen = marketopenlis()
TDAclient = tdamethods.TdaClient()
DBwriter = database_client.DbWritingManager()
DBreader = database_client.DbReadingManager()
optionsHelper = analytics.OptionsAnalyzer(DBwriter, DBreader)
Stringhelper = string_util.StringHelper()


# if marketopen:
batch = 100
interest_rate = TDAclient.get_optionchain("SPY")['interestRate']
etf_records = DBreader.get_all('tickerse')
for i in range(0, len(etf_records), 100):

    stock_list = [etf_record['SYMBOLS'] for etf_record in etf_records[i:i+100]]
    mapping = {}
    for stock in stock_list:
        try:
            option_size = DBreader.get_one_val("tickerse", "SYMBOLS", stock, "OptionSize")
            options_data = TDAclient.get_optionchain(stock, option_size)
            optionsHelper.daily_api_options_breakdown(options_data)
            update_info = (options_data['underlying']['change'], options_data['underlying']['percentChange'], options_data['underlying']['close'], stock)
            DBwriter.update_ticker('tickerse', update_info)
            expiration_map = Stringhelper.create_key_expiration(options_data)
            mapping[stock] = expiration_map
        except Exception as e:
            print(e)
    options_sorted = DBreader.get_options_sorted_batch(stock_list)
    df = pd.DataFrame(options_sorted)
    for stock in stock_list:
        try:
            stock_info = df[df['SYMBOLS'] == stock]
            closingprice = DBreader.get_one_val("tickerse", "SYMBOLS", stock, "closingprice")
            expiration_map = mapping[stock]
            optionsHelper.option_perf_aggregate(stock, stock_info.copy())
            optionsHelper.option_stats_aggregate(stock_info.copy(), stock)
            optionsHelper.speculative_ratio(stock)
            optionsHelper.price_skews_bydate(stock, interest_rate, closingprice, expiration_map, stock_info)
        except Exception as e:
            print(stock)
            tb = traceback.format_exc()
            print(tb)
            print(e)


    normal_stocks = DBreader.get_all('tickerss')
    for i in range(0, len(normal_stocks), 100):
        stock_list = [normal_stock['SYMBOLS'] for normal_stock in normal_stocks[i:i+100]]
        mapping = {}
        for stock in stock_list:
            try:
                option_size = DBreader.get_one_val("tickerss", "SYMBOLS", stock, "OptionSize")
                options_data = TDAclient.get_optionchain(stock, option_size)
                optionsHelper.daily_api_options_breakdown(options_data)
                update_info = (options_data['underlying']['change'], options_data['underlying']['percentChange'], options_data['underlying']['close'], stock)
                DBwriter.update_ticker('tickerss', update_info)
                expiration_map = Stringhelper.create_key_expiration(options_data)
                mapping[stock] = expiration_map
            except Exception as e:
                print(e)
        options_sorted = DBreader.get_options_sorted_batch(stock_list)
        df = pd.DataFrame(options_sorted)
        for stock in stock_list:
            try:
                stock_info = df[df['SYMBOLS'] == stock]
                closingprice = DBreader.get_one_val("tickerss", "SYMBOLS", stock, "closingprice")
                expiration_map = mapping[stock]
                optionsHelper.option_perf_aggregate(stock, stock_info.copy())
                optionsHelper.option_stats_aggregate(stock_info.copy(), stock)
                optionsHelper.speculative_ratio(stock)
                optionsHelper.price_skews_bydate(stock, interest_rate, closingprice, expiration_map, stock_info)

            except Exception as e:
                print(stock)
                tb = traceback.format_exc()
                print(tb)
                print(e)
    DBwriter.sector_aggre()
    DBwriter.distribute_top100()
    DBwriter.insert_timestamp()
    DBwriter.delete_expired_options()
    DBwriter.decrement_expire_day()


# else:
#     #no update
#     DBwriter.decrement_expire_day()
#     DBwriter.delete_expired_options()
