import datetime
import json
import os
import traceback
from datetime import date
from contextlib import contextmanager
import pymysql
import pymysql.cursors
import pymysqlpool
from flask import jsonify
from scrape import scrapeclient
from tdamodule import tdamethods
from utility import date_util, string_util


class DbWritingManager:

    VALID_TABLES = ["overallstats", "oitable", "miscellaneous", "sectoraggre",
                    "perfaggre", "statsaggre", "specu_ratio", "top100bcperf",
                    "top100bpperf", "top100wcperf", "top100wpperf", "dstock", "tickerse", "tickerss"]
    MAJOR_INDICES = ["SPY", "QQQ", "IWM", "DIA"]

    def __init__(self):

        self.cursorType = pymysql.cursors.DictCursor
        self.pool = pymysqlpool.ConnectionPool(
            host= os.getenv('DB_HOST'),
            user= os.getenv('DB_USER'),
            password= os.getenv('DB_PASSWORD'),
            database = os.getenv("DB_DATABASE"),
            cursorclass= self.cursorType,
            autocommit= True,
            maxsize= 3
        )
        self.datehelper = date_util.DateHelper()
        self.stringhelper = string_util.StringHelper()

    @contextmanager
    def acquire_connection(self):
        connection = self.pool.get_connection()
        try:
            yield connection
        finally:
            self.pool._put_connection(connection)

    def insert_options(self, option_data):
        with self.acquire_connection() as connection:

            SQLstmt = '''
                INSERT INTO options
                (optionkey, type, SYMBOLS, strikeprice, strikedate, marketprice, bid, ask,
                daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate,
                absHDate, volatility, volume, openinterest, delta, gamma, lastupdate, upperformance,
                downperformance, rho, ITM)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
            self._execute_sql(connection, SQLstmt, option_data)

    def update_options(self, option_data):
        with self.acquire_connection() as connection:
            connection.begin()
            SQLstmt = '''UPDATE options SET daysToExpiration = %s, marketprice = %s,
                        bid = %s, ask = %s, lowPrice = %s, highPrice = %s, absLow = %s,
                        absHigh = %s, absLDate = %s, absHDate = %s, volatility = %s,
                        volume = %s, openinterest = %s, delta = %s, gamma = %s,
                        lastupdate = %s, upperformance = %s, downperformance = %s,
                        rho = %s, ITM = %s WHERE optionkey = %s
                        '''

            self._execute_sql(connection, SQLstmt, option_data)

    def insert_ticker_common(self, ticker_data):
        with self.acquire_connection() as connection:
            SQLstmt = '''
                INSERT INTO tickersS
                (SYMBOLS, SECTORS, industry, country, OptionSize, description,
                pricechange, percentchange, closingprice)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''

            self._execute_sql(connection, SQLstmt, ticker_data)


    def insert_ticker_etf(self, ticker_data):
        with self.acquire_connection() as connection:
            SQLstmt = '''
                INSERT INTO tickersE (SYMBOLS, CATEGORY, OptionSize, description,
                pricechange, percentchange, closingprice) VALUES (%s, %s, %s, %s, %s, %s, %s)
                '''

            self._execute_sql(connection, SQLstmt, ticker_data)

    def insert_date_aggre(self, insertdata):
        with self.acquire_connection() as connection:
            connection.begin()
            SQLstmt = "INSERT INTO dstock (record_date, symbol, compiledate, pcdiff, callvol, putvol) VALUES (%s, %s, %s, %s, %s, %s)"

            self._execute_sql(connection, SQLstmt, insertdata)

    def update_sector_dateaggre(self):
        with self.acquire_connection() as connection:
            dateutil = date_util.DateHelper()
            exp_date = dateutil.get_datetime_delta(15)
            self.delete_expired_options("sstock", exp_date)
            SQLstmt = '''INSERT INTO sstock(record_date, SECTORS, compiledate, pcdiff, callvol, putvol)
                    SELECT
                        CURDATE() as record_date,
                        t2.INDUSTRY,
                        t1.compiledate,
                        AVG(t1.pcdiff) AS pcdiff,
                        SUM(t1.callvol) AS callvol
                        SUM(t1.putvol) AS putvol
            '''
            self._execute_sql(connection, SQLstmt)


    def insert_timestamp(self):
        with self.acquire_connection() as connection:
            dateutil = date_util.DateHelper()
            self.clear_table("miscellaneous")
            SQLstmt = "INSERT INTO miscellaneous(timestamp) VALUES (%s)"
            timestamp = dateutil.get_timestamp()
            self._execute_sql(connection, SQLstmt, (timestamp,))

    def delete_old_records(self, table, cutoff_date):
        with self.acquire_connection() as connection:
            if table not in self.VALID_TABLES:
                raise ValueError(f"Invalid Table : {table}")
            SQLstmt = f"DELETE FROM {table} WHERE record_date <= %s"
            self._execute_sql(connection, SQLstmt, (cutoff_date, ))

    def delete_expired_options(self):
        with self.acquire_connection() as connection:
            SQLstmt = "DELETE FROM options WHERE daysToExpiration <= 0"
            self._execute_sql(connection, SQLstmt)


    def decrement_expire_day(self):
        with self.acquire_connection() as connection:
            SQLstmt = "UPDATE options SET daysToExpiration = daysToExpiration - 1"
            self._execute_sql(connection, SQLstmt)


    def clear_table(self, table):
        with self.acquire_connection() as connection:
            if table not in self.VALID_TABLES:
                raise ValueError(f"Invalid Table : {table}")

            SQLstmt = f"DELETE FROM {table}"
            self._execute_sql(connection, SQLstmt)

    def update_option_perf(self, update_data):
        with self.acquire_connection() as connection:
            SQLstmt = '''UPDATE perfaggre SET bcallkey = %s, bcallperf = %s, bcalldate = %s,
                        worstcallperf = %s, worstcalldate = %s, worstcall = %s, bputkey = %s,
                        bputperf = %s, bputdate = %s, worstputperf = %s, worstputdate = %s,
                        worstput = %s WHERE SYMBOLS = %s'''
            self._execute_sql(connection, SQLstmt, update_data)

    def update_option_stats(self, update_data):
        with self.acquire_connection() as connection:
            SQLstmt = '''UPDATE statsaggre SET callvolume = %s, putvolume = %s, calloi = %s,
                        putoi = %s, otmcallvolume = %s, itmcallvolume = %s, otmputvolume = %s,
                        itmputvolume = %s, otmcalloi = %s, itmcalloi = %s, otmputoi = %s, itmputoi = %s,
                        volatility = %s, avgvola = %s, oi = %s, avgoi = %s, volume = %s,
                        avgvolume = %s WHERE SYMBOLS = %s'''
            self._execute_sql(connection, SQLstmt, update_data)

    def update_specu_ratio(self, update_data):
        with self.acquire_connection() as connection:
            SQLstmt = '''UPDATE specu_ratio SET otmitmcratio = %s, otmitmpratio = %s, otmitmcoiratio = %s,
                        otmitmpoiratio = %s, voloi = %s, cpratio = %s WHERE SYMBOLS = %s'''
            self._execute_sql(connection, SQLstmt, update_data)

    def update_ticker(self, table, price):
        with self.acquire_connection() as connection:
            if table not in self.VALID_TABLES:
                raise ValueError(f"Invalid Table : {table}")
            SQLstmt = f"UPDATE {table} SET pricechange = %s, percentchange = %s, closingprice = %s WHERE SYMBOLS = %s"
            self._execute_sql(connection, SQLstmt, price)

    def distribute_top100(self):
        with self.acquire_connection() as connection:
            dis_tables = ["top100bcperf", "top100bpperf", "top100wcperf", "top100wpperf"]
            dis_tables_var = [["bcallperf", "bcalldate", "bcallkey"], ["bputperf", "bputdate", "bputkey"], ["worstcallperf", "worstcalldate", "worstcall"], ["worstputperf", "worstputdate", "worstput"]]
            for i in range(4):
                self.clear_table(dis_tables[i])
                SQLstmt = self.stringhelper.distribute_sql_build(dis_tables[i], dis_tables_var[i][0], dis_tables_var[i][1], dis_tables_var[i][2])
                self._execute_sql(connection, SQLstmt)

    def sector_aggre(self):
        with self.acquire_connection() as connection:
            self.clear_table("sectoraggre")
            SQLstmt = '''INSERT INTO sectoraggre(INDUSTRY, volatility, avgvola, oi, avgoi,
                        volume, avgvolume, avgperf)
                        SELECT
                            t2.INDUSTRY AS INDUSTRY,
                            AVG(t1.volatility) AS volatility,
                            AVG(t1.avgvola) AS avgvola,
                            SUM(t1.oi) AS oi,
                            SUM(t1.avgoi) AS avgoi,
                            SUM(t1.volume) AS volume,
                            SUM(t1.avgvolume) AS avgvolume,
                            AVG(t2.percentchange) AS avgperf
                        FROM statsaggre AS t1
                        JOIN tickerss AS t2 ON t1.SYMBOLS = t2.SYMBOLS
                        GROUP BY t2.INDUSTRY
                    '''
            self._execute_sql(connection, SQLstmt)

    def dstock_aggregate(self):
        with self.acquire_connection() as connection:
            exp_date = self.datehelper.get_datetime_delta(15)
            self.delete_old_records("sstock", exp_date)
            SQLstmt = '''INSERT INTO sstock(record_date, SECTORS, compiledate, pcdiff, callvol, putvol)
                        SELECT
                            CURDATE() AS record_date,
                            t2.INDUSTRY,
                            t1.compiledate,
                            AVG(t1.pcdiff) AS pcdiff,
                            SUM(t1.callvol) AS callvol,
                            SUM(t1.putvol) AS putvol
                        FROM dstock AS t1
                        JOIN tickersS AS t2 ON t1.symbol = t2.SYMBOLS
                        WHERE t1.record_date = CURDATE()
                        GROUP BY t2.INDUSTRY, t1.compiledate
                '''
            self._execute_sql(connection, SQLstmt)

    def init_option_perf(self, symbol, etftype):
        with self.acquire_connection() as connection:
            todays_date = self.datehelper.get_todays_string()
            SQLstmt = '''INSERT INTO perfaggre (SYMBOLS, type, bcallkey, bcallperf, bcalldate,
                        worstcallperf, worstcalldate, worstcall, bputkey, bputperf, bputdate,
                        worstputperf, worstputdate, worstput) VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        '''
            insertdata = (symbol, etftype, "dummy", 0, todays_date, 0, todays_date, "dummy",
                        "dummy", 0, todays_date, 0, todays_date, "dummy")
            self._execute_sql(connection, SQLstmt, insertdata)


    def init_option_stats(self, symbol, etftype):
        with self.acquire_connection() as connection:
            SQLstmt = '''INSERT INTO statsaggre (SYMBOLS, type, callvolume, putvolume, calloi, putoi,
                        otmcallvolume, itmcallvolume, otmputvolume, itmputvolume, otmcalloi, itmcalloi, otmputoi, itmputoi,
                        volatility, avgvola, oi, avgoi, volume, avgvolume)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    '''
            insertdata = (symbol, etftype, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,
                        1000, 1000, 30, 30, 1000, 1000, 1000, 1000)

            self._execute_sql(connection, SQLstmt, insertdata)

    def init_specu_ratio(self, symbol):
        with self.acquire_connection() as connection:
            SQLstmt = '''INSERT INTO specu_ratio (SYMBOLS, otmitmcratio, otmitmpratio, otmitmcoiratio, otmitmpoiratio, voloi, cpratio)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            insertdata = (symbol, 1, 1, 1, 1, 1, 1)
            self._execute_sql(connection, SQLstmt, insertdata)


    def _execute_sql(self, connection, SQLstmt, data=None):
        cursorinstance = connection.cursor()
        cursorinstance.execute(SQLstmt, data)
        connection.commit()


class DbReadingManager:

    VALID_TABLES = ["overallstats", "oitable", "tickerse", "tickerss", "dstock", "miscellaneous", "tickerse", "tickerss"]

    def __init__(self):
        self.cursorType = pymysql.cursors.DictCursor
        self.pool = pymysqlpool.ConnectionPool(
            host= os.getenv('DB_HOST'),
            user= os.getenv('DB_USER'),
            password= os.getenv('DB_PASSWORD'),
            database = os.getenv("DB_DATABASE"),
            cursorclass= self.cursorType,
            autocommit= True,
            maxsize= 3
        )
        self.connection = self.acquire_connection()
        self.stringhelper = string_util.StringHelper()

    @contextmanager
    def acquire_connection(self):
        connection = self.pool.get_connection()
        try:
            yield connection
        finally:
            self.pool._put_connection(connection)

    def get_all(self, table):
        with self.acquire_connection() as connection:
            if table not in self.VALID_TABLES:
                raise ValueError(f"Invalid table : {table}")

            SQLstmt = f"select * from {table}"
            return self._execute_sql(connection, SQLstmt)


    def get_options(self):
        with self.acquire_connection() as connection:
            SQLstmt = '''
                select * from options ORDER BY SYMBOLS ASC, daysToExpiration ASC,
                type ASC, strikeprice ASC
            '''
            return self._execute_sql(connection, SQLstmt)


    def check_option_exist(self, key):
        with self.acquire_connection() as connection:
            SQLstmt = "SELECT * FROM options WHERE optionkey = %s"
            return self._execute_sql(connection, SQLstmt, key)


    def get_stock_data(self, symbol):
        with self.acquire_connection() as connection:
            SQLstmt = '''
                SELECT SYMBOLS as symbol, INDUSTRY as category, description, pricechange, percentchange, closingprice
                FROM tickerss WHERE SYMBOLS = %s
                UNION
                SELECT SYMBOLS as symbol, CATEGORY as category, description, pricechange, percentchange, closingprice
                FROM tickerse WHERE SYMBOLS = %s
            '''
            return self._execute_sql(connection, SQLstmt, (symbol, symbol))

    def get_options_sorted(self, symbol):
        with self.acquire_connection() as connection:
            SQLstmt = "select * from options WHERE SYMBOLS = %s ORDER BY daysToExpiration ASC, type ASC, strikeprice ASC"
            return self._execute_sql(connection, SQLstmt, (symbol, ))

    def get_options_sorted_batch(self, symbol_list):
        with self.acquire_connection() as connection:
            SQLstmt = """
            SELECT * FROM options
            WHERE SYMBOLS IN (%s)
            ORDER BY  daysToExpiration ASC, type ASC, strikeprice ASC
            """ % ','.join(["'" + str(stock_id) + "'" for stock_id in symbol_list])
            return self._execute_sql(connection, SQLstmt)

    def get_expec_chart(self, symbol): #skip for now,
        # check out business logic if i need to change how expected movement is calculated

        with self.acquire_connection() as connection:

            SQLstmt = '''
            SELECT t1.compiledate, t1.pcdiff, t1.putvol, t1.callvol, t2.pcdiff AS 10pcdiff
            FROM dstock AS t1
            JOIN dstock AS t2 ON t1.symbol = t2.symbol AND t1.compiledate = t2.compiledate
            WHERE t1.symbol = %s AND t1.record_date = (SELECT MAX(record_date) FROM dstock)
            AND t2.record_date = (SELECT MAX(record_date) FROM dstock
            WHERE record_date < DATE_SUB((SELECT MAX(record_date) FROM dstock), INTERVAL 5 DAY));
            '''
            result = self._execute_sql(connection, SQLstmt, (symbol, ))
            positive = 0
            for dict in result:
                positive += dict['pcdiff']
            if positive >= 0:
                ispositive = True
            else:
                ispositive = False
            response = {'result' : result, 'ispositive': ispositive}
            print(response)
            return response

    def get_sector_aggre(self):
        with self.acquire_connection() as connection:
            SQLstmt = "select * from sectoraggre"
            records = self._execute_sql(connection, SQLstmt)
            records = records[1:]
            return json.dumps(records)

    def get_stock_info(self, symbol):
        with self.acquire_connection() as connection:
            SQLstmt = '''
            SELECT SYMBOLS as symbol, INDUSTRY as category, description, pricechange, percentchange, closingprice
            FROM tickerss WHERE SYMBOLS = %s
            UNION
            SELECT SYMBOLS as symbol, CATEGORY as category, description, pricechange, percentchange, closingprice
            FROM tickerse WHERE SYMBOLS = %s
            '''
            return self._execute_sql(connection, SQLstmt, (symbol, symbol))

    def get_stock_options_stats(self, symbol):

        with self.acquire_connection() as connection:
            SQLstmt = "SELECT * from statsaggre WHERE SYMBOLS = %s"
            return self._execute_sql(connection, SQLstmt, (symbol, ))

    def get_top_10(self, order, item):
        with self.acquire_connection() as connection:

            if order == "lowest":
                order = "ASC"
            else:
                order = "DESC"
            SQLstmt = """
                SELECT lefttable.SYMBOLS, {}, lefttable.description, lefttable.closingprice
                FROM (
                    SELECT SYMBOLS, description, closingprice FROM tickerse
                    UNION
                    SELECT SYMBOLS, description, closingprice FROM tickerss
                ) AS lefttable
                JOIN specu_ratio
                ON lefttable.SYMBOLS = specu_ratio.SYMBOLS
                WHERE {} != 0
                ORDER BY {} {}
                LIMIT 10;
            """.format(item, item, item, order)
            result = self._execute_sql(connection, SQLstmt)
            return result

    def get_stats(self, symbol):
        with self.acquire_connection() as connection:
            SQLstmt = "select * from statsaggre WHERE symbols = %s"
            return json.dumps(self._execute_sql(connection, SQLstmt, (symbol, ))[0])

    def get_table_json(self, table):
        with self.acquire_connection() as connection:
            SQLstmt = "select * from {}".format(table)
            result = self._execute_sql(connection, SQLstmt)
            return json.dumps(result)

    def get_perf_aggre(self, symbol):
        with self.acquire_connection() as connection:
            SQLstmt = "SELECT * FROM perfaggre WHERE SYMBOLS = %s"
            return self._execute_sql(connection, SQLstmt, (symbol, ))

    def get_stats_aggre(self, symbol):
        with self.acquire_connection() as connection:
            SQLstmt = "SELECT * FROM statsaggre WHERE SYMBOLS = %s"
            return self._execute_sql(connection, SQLstmt, (symbol, ))

    def get_time_stamp(self):
        with self.acquire_connection() as connection:
            SQLstmt = "SELECT * from miscellaneous"
            records = self._execute_sql(connection, SQLstmt)
            return json.dumps(records)

    def get_one_val(self, table, key_col, key_val, target_col):
        with self.acquire_connection() as connection:
            SQLstmt = f"SELECT {target_col} FROM {table} WHERE {key_col} = %s"

            result = self._execute_sql(connection, SQLstmt, (key_val, ))
            return result[0][target_col]



    def _execute_sql(self, connection, SQLstmt, data=None):
        cursorinstance = connection.cursor()
        cursorinstance.execute(SQLstmt, data)
        result = cursorinstance.fetchall()
        return result
