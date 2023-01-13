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
import toke



def make_webdriver():
        # Import selenium here because it's slow to import
        from selenium import webdriver

        driver = webdriver.Chrome("C:/Users/spam8/scanneranalyze/tdameri/chromedriver.exe")
        atexit.register(lambda: driver.quit())
        return driver


client = easy_client(toke.api_key, toke.redirect_url, toke.token_path, make_webdriver)
datetoday = datetime.date.today()

time_change = datetime.timedelta(days=36)

data = client.get_option_chain("AMZN", strike_count=1, include_quotes=True, from_date=datetime.date.today(), to_date= datetoday + time_change)

for item in data.json()['putExpDateMap']:
    for each in data.json()['putExpDateMap'][item]:
        for items in data.json()['putExpDateMap'][item][each]:
            print(items)
