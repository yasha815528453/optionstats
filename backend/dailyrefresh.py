from database import methods as DBmethods
from tdamodule import tdamethods
import pandas_market_calendars as mcal
from datetime import date
import datetime
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


if marketopen:
    try:
        connection = DBmethods.acquire_connection()
        DBmethods.deleteExpired(connection)
        DBmethods.decrementExpday(connection)

        records = DBmethods.getETF(connection)
        for stock in records:
            tdamethods.updateOptionData(stock['SYMBOLS'], stock['OptionSize'], True)

        stockrecords = DBmethods.getStock(connection)
        for stock in stockrecords:
            tdamethods.updateOptionData(stock['SYMBOLS'], stock['OptionSize'], False)
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
