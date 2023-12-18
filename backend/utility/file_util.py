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

        stocklis = yf.tickers_nasdaq() + yf.tickers_other()
        seen = set()
        processed_list = [s for s in stocklis if all(c not in s for c in "$.") and not (s in seen or seen.add(s))]

        optional_list = []

        for symb in processed_list:
            data = tdaclient.get_optionchain(symb)
            if data == None:
                pass
            elif data['underlying']['description'] == "Symbol not found":
                pass
            elif data['underlying']['mark'] == None:
                pass
            elif len(data['putExpDateMap']) == 0:
                pass
            else:
                optional_list.append(symb)


        good_list = []
        for sym in optional_list:
            data = tdaclient.get_quote(sym)
            if data == None or data[sym]['closePrice'] < 1.1:
                pass
            else:
                good_list.append([sym, data[sym]["description"], 'S' if data[sym]['assetType'] == "EQUITY" else 'E'])

        with open(self.optional_stock_csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['symbol', 'description', 'type'])
            writer.writerows(good_list)

    def get_optional_stock_list(self):

        with open(self.optional_stock_csv_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)

            return list(reader)
