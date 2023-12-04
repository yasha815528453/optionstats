from database import database_client
from tdamodule import tdamethods
import pandas_market_calendars as mcal
from datetime import date
from tdamodule import tdamethods
from stockanalyzer import analytics
from dotenv import load_dotenv
from utility import string_util
import time

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


if marketopen:
    batch = 100
    try:
        interest_rate = TDAclient.get_optionchain("SPY")['interestRate']
        etf_records = DBreader.get_all('tickerse')

        for stock in etf_records:

            option_size = DBreader.get_one_val("tickersE", "SYMBOLS", stock['SYMBOLS'], "OptionSize")

            closingprice = DBreader.get_one_val("tickersE", "SYMBOLS", stock['SYMBOLS'], "closingprice")

            options_data = TDAclient.get_optionchain(stock['SYMBOLS'], option_size)

            expiration_map = Stringhelper.create_key_expiration(options_data)

            options_sorted = DBreader.get_options_sorted(stock['SYMBOLS'])

            optionsHelper.daily_api_options_breakdown(options_data)

            optionsHelper.option_perf_aggregate(stock['SYMBOLS'], options_sorted)

            optionsHelper.option_stats_aggregate(options_sorted, stock['SYMBOLS'])

            optionsHelper.speculative_ratio(stock['SYMBOLS'])

            optionsHelper.price_skews_bydate(stock['SYMBOLS'], interest_rate, closingprice, expiration_map, options_sorted)

        normal_stocks = DBreader.get_all('tickerss')
        for stock in normal_stocks:
            option_size = DBreader.get_one_val("tickersS", "SYMBOLS", stock['SYMBOLS'], "OptionSize")
            closingprice = DBreader.get_one_val("tickersE", "SYMBOLS", stock['SYMBOLS'], "closingprice")
            options_data = TDAclient.get_optionchain(stock['SYMBOLS'], option_size)
            expiration_map = Stringhelper.create_key_expiration(options_data)
            optionsHelper.daily_api_options_breakdown(options_data)
            options_records = DBreader.get_options_sorted(stock['SYMBOLS'])
            optionsHelper.option_perf_aggregate(stock['SYMBOLS'], options_records)
            optionsHelper.option_stats_aggregate(options_records, stock['SYMBOLS'])
            optionsHelper.speculative_ratio(stock['SYMBOLS'])
            optionsHelper.price_skews_bydate(stock['SYMBOLS'], interest_rate, closingprice, options_data, expiration_map)
            print(stock)
        DBwriter.distribute_top100()
        DBwriter.insert_timestamp()
        DBwriter.delete_expired_options()
        DBwriter.decrement_expire_day()

    except Exception as e:
        print(e)
else:
    #no update
    DBwriter.decrement_expire_day()
    DBwriter.delete_expired_options()
