from database import database_client
from tdamodule import tdamethods
import pandas_market_calendars as mcal
from datetime import date
from tdamodule import tdamethods
from stockanalyzer import analytics
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
optionsHelper = analytics.OptionsAnalyzer()


if marketopen:
    try:
        DBwriter.delete_expired_options()
        DBwriter.decrement_expire_day()
        interest_rate = TDAclient.get_optionchain("SPY").json()['interestRate']
        etf_records = DBreader.get_all('tickerse')
        for stock in etf_records:
            option_size = DBreader.get_one_val("tickersE", "SYMBOLS", stock['SYMBOLS'], "OptionSize")
            closingprice = DBreader.get_one_val("tickersE", "SYMBOLS", stock['SYMBOLS'], "closingprice")
            options_data = TDAclient.get_optionchain(stock['SYMBOLS'], option_size)
            optionsHelper.daily_api_options_breakdown(options_data.json())
            optionsHelper.option_perf_aggregate(stock['SYMBOLS'], options_data.json())
            optionsHelper.option_stats_aggregate(options_data.json(), stock['SYMBOLS'])
            optionsHelper.speculative_ratio(stock['SYMBOLS'])
            optionsHelper.price_skews_bydate(stock['SYMBOLS'], interest_rate, closingprice)

        normal_stocks = DBreader.get_all('tickerss')
        for stock in normal_stocks:
            option_size = DBreader.get_one_val("tickersS", "SYMBOLS", stock['SYMBOLS'], "OptionSize")
            closingprice = DBreader.get_one_val("tickersE", "SYMBOLS", stock['SYMBOLS'], "closingprice")
            options_data = TDAclient.get_optionchain(stock['SYMBOLS'], option_size)
            optionsHelper.daily_api_options_breakdown(options_data.json())
            optionsHelper.option_perf_aggregate(stock['SYMBOLS'], options_data.json())
            optionsHelper.option_stats_aggregate(options_data.json(), stock['SYMBOLS'])
            optionsHelper.speculative_ratio(stock['SYMBOLS'])
            optionsHelper.price_skews_bydate(stock['SYMBOLS'], interest_rate, closingprice)

        ################################ updating updateoptiondata for tda...
        ### DONE go next->.

        DBmethods.stockAggregate(connection)
        DBmethods.distribute(connection)
        # when doing the date aggregated table, the first loop should update
        # the price of the stock
        DBmethods.dateAggregate(connection)
        DBmethods.sector_perf_aggre(connection)
        DBmethods.new_timestamp(connection)
    finally:
        DBmethods.release_connection(connection)
        #call the function that create the table.
else:
    #no update
    connection = DBmethods.acquire_connection()
    DBmethods.decrementExpday(connection)
    DBmethods.deleteExpired(connection)
    DBmethods.release_connection(connection)
