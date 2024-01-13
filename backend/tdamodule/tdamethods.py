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
import functools
from datetime import date
# from database import methods as DBmethods
import pandas as pd
from tdamodule import ratelimit
from time import sleep
import traceback
import os

class TdaClient:

    limiter = ratelimit.RateLimiter(rate_limit=2, time_window=1)


    def __init__(self):
        self.client = easy_client(os.getenv("API_KEY"), os.getenv("REDIRECT_URL"), os.getenv("TOKEN_PATH", self.make_webdriver))

    def api_limiter(client_methods):
        def wrapper(self, *args, **kwargs):
            for retry in range(15):
                try:
                    if TdaClient.limiter.get_token():
                        response = client_methods(self, *args, **kwargs)
                        return response
                except Exception as e:
                    print(e)
                    pass
                sleep(0.1)
        return wrapper

    def make_webdriver(self):
            # Import selenium here because it's slow to import
            from selenium import webdriver

            driver = webdriver.Chrome("chromedriver.exe")
            atexit.register(lambda: driver.quit())
            return driver

    # get stock data function, for closing price, opening, etc..
    @api_limiter
    def get_closingprice(self, symbol):

        data = self.client.get_price_history_every_minute(symbol, start_datetime=datetime.datetime.today(),
                                                           end_datetime=datetime.datetime.today())
        return data.json()['candles'][540]['close']

    # get candles function, to get the 13:15 candle for accurate price
    @api_limiter
    def get_candlestick_indicesclose(self, symbol):
        data = self.client.get_price_history_every_minute(symbol, start_datetime=datetime.datetime.today(),
                                                           end_datetime=datetime.datetime.today())
        return data.json()['candles'][554]['close']

    #get options function,
    @api_limiter
    def get_optionchain(self, symbol, size=None):

        if size:
            data = self.client.get_option_chain(symbol, strike_count = size, include_quotes=True)
        else:
            data = self.client.get_option_chain(symbol, include_quotes=True)

        if data.json()['status'] == 'FAILED':
            return None
        return data.json()

    @api_limiter
    def get_quote(self, symbol):
        data = self.client.get_quote(symbol)
        if data.json()[symbol]['closePrice'] < 1.0:
            print(f"bad stock => {symbol}")
            return None
        return data.json()



def make_webdriver():
        # Import selenium here because it's slow to import
        from selenium import webdriver

        driver = webdriver.Chrome("chromedriver.exe")
        atexit.register(lambda: driver.quit())
        return driver
