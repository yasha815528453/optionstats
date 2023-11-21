import yahoo_fin.stock_info as yf
from tdamodule import ratelimit
from tdamodule import tdamethods
from time import sleep
import os
import csv


class FileHelper:

    class_path = os.path.abspath(__file__)
    class_dir = os.path.dirname(class_path)
    parent_dir = os.path.join(class_dir, '..')

    optional_stock_csv_path = os.path.join(parent_dir, 'stock_list.csv')

    def create_optional_stocks_csv(self):
        tdaclient = tdamethods.TdaClient()
        limiter = ratelimit.RateLimiter(rate_limit=120, time_window=60)

        stocklis = yf.tickers_nasdaq() + yf.tickers_other()
        seen = set()
        processed_list = [s for s in stocklis if all(c not in s for c in "$.") and not (s in seen or seen.add(s))]

        optional_list = []

        for symb in stocklis:
            for retry in range(5):
                if limiter.get_token():
                    data = tdaclient.get_optionchain(symb)
                    if data['status'] == 'FAILED':
                        print(symb + " has failed")
                        break

                    else:
                        optional_list.append(symb)
                        break
                else:
                    sleep(0.5)
        good_list = []
        for sym in optional_list:
            for retry in range(5):
                if limiter.get_token():
                    data = tdaclient.get_quote(sym)
                    if data[sym]['closePrice'] < 0.7:
                        print("noob stock = " + sym)
                        break
                    else:
                        good_list.append({'symbol':sym, 'description':data[sym]['description'],
                                    'type' : 'S' if data[sym]['assetType'] == '' else 'E'})
                else:
                    sleep(0.5)
        with open(self.optional_stock_csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(good_list)

    def get_optional_stock_list(self):

        with open(self.optional_stock_csv_path, mode='r', newline='') as file:
            reader = csv.reader(file)

        return list(reader)
