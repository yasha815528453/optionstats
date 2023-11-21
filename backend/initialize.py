from database import database_client
from scrape import scrapeclient
from tdamodule import tdamethods
from utility import file_util
from stockanalyzer.analytics import OptionsAnalyzer
from stockanalyzer.stockinfo import StockHelper

def initialize():

    fileHelper = file_util.FileHelper()
    scraper = scrapeclient.ScrapeClient()
    DBwriter = database_client.DbWritingManager()
    stockHelper = StockHelper()
    TDAclient = tdamethods.TdaClient()

    Optionhelper = OptionsAnalyzer(DBwriter)
    optional_stock = fileHelper.get_optional_stock_list()

    for stock in optional_stock:


        option_data = TDAclient.get_optionchain(stock['symbol'])
        stock_price = option_data['underlyingPrice']
        option_size = stockHelper.useful_options_size(option_data)
        DBwriter.init_specu_ratio(stock['symbol'])
        # if common stock
        if stock['type'] == 'S':
            sector, industry, country = scraper.get_sector_industry_country(stock['symbol'])
            DBwriter.insert_ticker_common((stock['symbol'], sector, industry, country,
                                                option_size, stock['description'], 0, 0, stock_price))
            DBwriter.init_option_perf(stock['symbol'], stock['type'])
            DBwriter.init_option_stats(stock['symbol'], stock['type'])

        # ETFs
        else:
            category = scraper.get_category(stock['symbol'])
            DBwriter.insert_ticker_etf((stock['symbol'], category, option_size, stock['description'], 0, 0, stock_price))
            DBwriter.init_option_perf(stock['symbol'], stock['type'])
            DBwriter.init_option_stats(stock['symbol'], stock['type'])

        sized_options_data = TDAclient.get_optionchain(stock['symbol'], option_size)
        Optionhelper.initial_api_options_break(sized_options_data.json())


initialize()
