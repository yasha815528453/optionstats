from database import methods as DBmethods
from tdamodule import tdamethods
import pandas_market_calendars as mcal
from datetime import date

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
marketopenlis = market.to_list
marketopen = marketopenlis()

if marketopen:
    #update
    tdamethods.updateOptionData()
    DBmethods.distribute()
else:
    #no update
    DBmethods.deleteExpired()


#then delete expired contracts.


