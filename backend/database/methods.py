import pymysql
import pymysql.cursors
import datetime
from datetime import date
from tdamodule import tdamethods
from scrape import scrapeclient
import json
import pymysqlpool
import traceback
from flask import jsonify
import os


class DbWritingManager:

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

    def acquire_connection(self):
        return self.pool.get_connection()

    def release_connection(self, connection):
        connection.close()

    def insert_options(self, option_data):
        sqlstmt = """
        INSERT INTO options (optionkey, type, SYMBOLS, strikeprice, marketprice, bid, ask, daysToExpiration, lowPrice, highPrice, absLow, absHigh, absLDate, absHDate, volatility, volume, openinterest, delta, gamma, theta, vega, theoreticalOptionValue, lastupdate, upperformance, downperformance, rho, isetf))
        """

class DbReadingManager:

    def __init__(self):
        self.cursorType = pymysql.cursors.DictCursor
        self.pool = pymysqlpool.ConnectionPool(
            host= os.getenv('DB_HOST'),
            user= os.getenv('DB_USER'),
            password= os.getenv('DB_PASSWORD'),
            database = os.getenv("DB_DATABASE"),
            cursorclass= self.cursorType,
            autocommit= True,
            maxsize= 1
        )

    def acquire_connection(self):
        return self.pool.get_connection()

    def release_connection(self, connection):
        connection.close()


cursorType = pymysql.cursors.DictCursor
pool = pymysqlpool.ConnectionPool(
    host='localhost',
    user='root',
    password='8155',
    database = "optionsdb",
    cursorclass=cursorType,
    autocommit=True,
    maxsize=3
)


def acquire_connection():
    connection = pool.get_connection()
    return connection

def release_connection(connection):
    connection.close()

def execute(sqlstmt, data, connection):

    cursorinstance = connection.cursor()
    cursorinstance.execute(sqlstmt, data)
    connection.commit()

def get_sector(connection):
    cursorinstance = connection.cursor()
    sql = "select * from sectoraggre"
    cursorinstance.execute(sql)
    records = cursorinstance.fetchall()
    records = records[1:]
    return json.dumps(records)

def get_overallstats(connection):
    cursorinstance = connection.cursor()
    sql = "select * from overallstats"
    cursorinstance.execute(sql)
    records = cursorinstance.fetchall()
    return json.dumps(records)

def get_oitable(symbol, connection):
    cursorinstance = connection.cursor()
    sql = "select * from oitable WHERE symbol = '{}'".format(symbol)
    cursorinstance.execute(sql)
    records = cursorinstance.fetchall()
    return json.dumps(records)

def get_topten(connection, order, item):
    cursorinstance = connection.cursor()
    if order == "lowest":
        order = "ASC"
    else:
        order = "DESC"
    sql = """
        SELECT lefttable.SYMBOLS, {}, lefttable.description, lefttable.closingprice
        FROM (
            SELECT SYMBOLS, description, closingprice FROM tickerse
            UNION
            SELECT SYMBOLS, description, closingprice FROM tickerss
        ) AS lefttable
        JOIN stockaggre
        ON lefttable.SYMBOLS = stockaggre.SYMBOLS
        WHERE {} != 0
        ORDER BY {} {}
        LIMIT 10;
    """.format(item, item, item, order)
    cursorinstance.execute(sql)
    records = cursorinstance.fetchall()
    return json.dumps(records)


def get_stock_info(symbol, connection):
    cursorinstance = connection.cursor()
    sql = '''
    SELECT SYMBOLS as symbol, INDUSTRY as category, description, pricechange, percentchange, closingprice
    FROM tickerss WHERE SYMBOLS = %s
    UNION
    SELECT SYMBOLS as symbol, CATEGORY as category, description, pricechange, percentchange, closingprice
    FROM tickerse WHERE SYMBOLS = %s
    '''
    cursorinstance.execute(sql, (symbol, symbol))
    result = cursorinstance.fetchall()
    return jsonify(result)

def get_chartdata(symbol, connection):
    try:
        cursorinstance = connection.cursor()
        cursorinstance.execute("(SELECT MAX(record_date) FROM dstock WHERE symbol = 'SPY')")
        res = cursorinstance.fetchall()
        print(res)
        sql = '''
        SELECT t1.compiledate, t1.pcdiff, t1.putvol, t1.callvol, t2.pcdiff AS 10pcdiff
        FROM dstock AS t1
        JOIN dstock AS t2 ON t1.symbol = t2.symbol AND t1.compiledate = t2.compiledate
        WHERE t1.symbol = %s AND t1.record_date = (SELECT MAX(record_date) FROM dstock) AND t2.record_date = (SELECT MAX(record_date) FROM dstock WHERE record_date < DATE_SUB((SELECT MAX(record_date) FROM dstock), INTERVAL 1 DAY));
        '''
        cursorinstance.execute(sql, (symbol, ))
        print(cursorinstance._last_executed)
        result = cursorinstance.fetchall()
        print("huh")
        print(result)
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
    except Exception as e:
        print(e)
        print("error?")


def executemany( sqlstmt, data, connection):

    cursorinstance = connection.cursor()
    cursorinstance.executemany(sqlstmt, data)
    connection.commit()

def getTable(table, connection):

    cursorinstance = connection.cursor()
    sql = "select * from {}".format(table)
    cursorinstance.execute(sql)
    records = cursorinstance.fetchall()
    return records


def getETF(connection):

    cursorinstance = connection.cursor()
    sql = "select * from tickerse"
    cursorinstance.execute(sql)
    records = cursorinstance.fetchall()
    return records


def getTableJson(table, connection):

    cursorinstance = connection.cursor()
    sql = "select * from {}".format(table)
    cursorinstance.execute(sql)
    records = cursorinstance.fetchall()
    for dict in records:
        for key, item in dict.items():
            if type(item) == datetime.date:
                dict[key] = str(item.year) + '-' + str(item.month) + '-' + str(item.day)
    return json.dumps(records)

def new_timestamp(connection):
    cursorinstance = connection.cursor()
    sql = "DELETE FROM miscellaneous"
    cursorinstance.execute(sql)
    connection.commit()
    sql = "INSERT INTO miscellaneous(timestamp) VALUES (%s)"
    dt = datetime.datetime.now()
    timestamp = str(dt.year)+'-'+str(dt.month)+'-'+str(dt.day)+' '+str(dt.hour)+':'+str(dt.minute)
    execute(sql, (timestamp,), connection)

def get_timestamp(connection):
    cursorinstance = connection.cursor()
    sql = "SELECT * from miscellaneous"
    cursorinstance.execute(sql)
    records = cursorinstance.fetchall()
    return json.dumps(records)


def getStock(connection):

    cursorinstance = connection.cursor()
    sql = "select * from tickerss"
    cursorinstance.execute(sql)
    records = cursorinstance.fetchall()
    return records


def deleteALL(table, connection):

    cursorinstance = connection.cursor()
    sql = "DELETE FROM {}".format(table)
    cursorinstance.execute(sql)
    connection.commit()


def getclosingprice(symbol, etf, connection):

    cursorinstance = connection.cursor()
    if etf:
        sql = "SELECT closingprice FROM tickerse WHERE SYMBOLS = %s"
        cursorinstance.execute(sql, (symbol, ))
        price = cursorinstance.fetchone()
        return price['closingprice']
    else:
        sql = "SELECT closingprice FROM tickerss WHERE SYMBOLS = %s"
        cursorinstance.execute(sql, (symbol, ))
        price = cursorinstance.fetchone()
        return price['closingprice']



def checkOptionPK(key, connection):

    cursorinstance = connection.cursor()
    sql = "SELECT * FROM options WHERE optionkey = %s"
    cursorinstance.execute(sql, key)
    records = cursorinstance.fetchall()
    return records


def updateprice(ticker, price, etf, connection):
    if etf:
        sql = "UPDATE tickerse SET description = %s, pricechange = %s, percentchange = %s, closingprice = %s WHERE SYMBOLS = %s"
        data = (price[0], price[1], price[2], price[3], ticker)
        execute(sql, data, connection)
    else:
        sql = "UPDATE tickerss SET description = %s, pricechange = %s, percentchange = %s, closingprice = %s WHERE SYMBOLS = %s"
        data = (price[0], price[1], price[2], price[3], ticker)
        execute(sql, data, connection)

def get_records(sql, connection):
    cursorinstance = connection.cursor()
    cursorinstance.execute(sql)
    records = cursorinstance.fetchall()
    return records

def deleteExpired(connection):

    cursorinstance = connection.cursor()
    sql = "DELETE FROM options WHERE daysToExpiration <= 0"
    cursorinstance.execute(sql)
    connection.commit()

def decrementExpday(connection):
    cursorinstance = connection.cursor()
    sql = "UPDATE options SET daysToExpiration = daysToExpiration - 1"
    cursorinstance.execute(sql)
    connection.commit()

def sector_perf_aggre(connection):
    cursorinstance = connection.cursor()
    deleteALL("sectoraggre", connection)
    sql = '''
    INSERT INTO sectoraggre(
        INDUSTRY ,
        volatility,
        avgvolatility,
        dollarestimate,
        avgdollar,
        volume,
        avgvolume,
        avgcallperf,
        avgputperf
    )
    SELECT
        t2.INDUSTRY AS INDUSTRY,
        AVG(t1.volatility) AS volatility,
        AVG(t1.avgvola) AS avgvolatility,
        SUM(t1.totalcalldollar + t1.totalputdollar) AS dollarestimate,
        AVG(t1.avgdollar) AS avgdollar,
        SUM(t1.volume) AS volume,
        SUM(t1.avgvolume) AS avgvolume,
        ROUND(AVG(t1.avgcall), 1) AS avgcallperf,
        ROUND(AVG(t1.avgput), 1) AS avgputperf
    FROM stockaggre as t1
    JOIN tickersS as t2 ON t1.SYMBOLS = t2.SYMBOLS
    GROUP BY t2.INDUSTRY
    '''
    cursorinstance.execute(sql)
    connection.commit()

    today = date.today()
    eleven_days_ago = today - datetime.timedelta(days=15)
    delete_sql = "DELETE FROM dstock WHERE record_date <= %s"
    execute(delete_sql, eleven_days_ago, connection)



    sql = '''
    INSERT INTO sstock (
        record_date,
        SECTORS,
        compiledate,
        pcdiff,
        callvol,
        putvol
    )
    SELECT
        CURDATE() as record_date,
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
    cursorinstance.execute(sql)
    connection.commit()
    ##create a new table everyday like dateaggre, but for sectors. look down.
    ## query results, divide by total amount or sum up. is all to do.

def gettop10(connection):
    cursorinstance = connection.cursor()
    sql = ""

def dateAggregate(connection):
    #create a new date aggregated table everyday.
    # then refer to older ones, if the referred one doesnt exist, just skip.
    #this is for the charts.
    cursorinstance = connection.cursor()
    fed_funds_rate = scrapeclient.get_fed_funds_rate()

    today = date.today()
    fifteen_days_ago = today - datetime.timedelta(days=15)
    delete_sql = "DELETE FROM dstock WHERE record_date <= %s"
    execute(delete_sql, fifteen_days_ago, connection)
    if today.month < 10:
        month = '0'+str(today.month)
    else:
        month = str(today.month)
    if today.day < 10:
        day = '0'+str(today.day)
    else:
        day = str(today.day)
    year = str(today.year - 2000)

    sql = "select * from options ORDER BY SYMBOLS ASC, daysToExpiration ASC, type ASC, strikeprice ASC"
    cursorinstance.execute(sql)
    options = cursorinstance.fetchall()
    prevexpiration = options[0]['daysToExpiration']
    closingprice = getclosingprice(options[0]['SYMBOLS'], options[0]['isetf'] == 'Y', connection)
    prevstock = options[0]['SYMBOLS']
    call_list = []
    put_list = []
    callvolume = 0
    putvolume = 0
    denominator = 0
    todaystring = month+'-'+day+'-'+year
    sql = "INSERT INTO dstock (record_date, symbol, compiledate, pcdiff, callvol, putvol) VALUES (%s, %s, %s, %s, %s, %s)"
    sql2 = "INSERT INTO oitable (symbol, compiledate, position, openinterest) VALUES (%s, %s, %s, %s)"
    for i in range(len(options)):
        try:

            if prevexpiration == options[i]['daysToExpiration']:
                datetoinsert = options[i]['optionkey'].split("_")[1][0:6]
                datetoinsert = datetoinsert[0:2]+'-'+datetoinsert[2:4]+'-'+datetoinsert[4:6]
                denominator += 1
                if options[i]['type'] == 'C':
                    strike = options[i]['strikeprice']
                    market = (options[i]['bid'] + options[i]['ask'])/2
                    rho = options[i]['rho']
                    callvolume += options[i]['volume']
                    delta = options[i]['delta']
                    gamma = options[i]['gamma']
                    oi = options[i]['openinterest']
                    option_list = [market, strike, rho, delta, gamma, oi]
                    call_list.append(option_list)

                else:
                    market = (options[i]['bid'] + options[i]['ask'])/2
                    strike = options[i]['strikeprice']
                    putvolume += options[i]['volume']
                    rho = options[i]['rho']
                    delta = options[i]['delta']
                    gamma = options[i]['gamma']
                    oi = options[i]['openinterest']
                    option_list = [market, strike, rho, delta, gamma, oi]
                    put_list.append(option_list)

            else:
                prevexpiration = options[i]['daysToExpiration']
                if not call_list:
                    continue

                midpoint = len(call_list)//2
                adjusted_price = call_list[midpoint][1]
                all_price_diff = adjusted_price - closingprice
                price_diff = 0
                if all_price_diff >= 2:
                    change_price = lambda market, deltachange, gammachange, rho: market + deltachange*all_price_diff + 0.5*gammachange*all_price_diff**2 - fed_funds_rate*rho
                else:
                    change_price = lambda market, deltachange, gammachange, rho: market + deltachange*all_price_diff + gammachange*all_price_diff - fed_funds_rate*rho

                for z in range(len(call_list)):
                    price_diff += change_price(call_list[z][0], call_list[z][3], call_list[z][4], call_list[z][2])
                    price_diff -= change_price(put_list[-z-1][0], put_list[-z-1][3], put_list[-z-1][4], put_list[-z-1][2])
                    if datetoinsert==(todaystring):
                        pass
                    else:
                        openint = call_list[z][5] - put_list[z][5]
                        execute(sql2, (prevstock, datetoinsert, z, openint), connection)

                #use call_list and put_list
                closingprice = getclosingprice(options[i]['SYMBOLS'], options[i]['isetf'] == 'Y', connection)
                if (price_diff/denominator) < -closingprice:
                    price_diff_insert = -closingprice
                elif (price_diff/denominator) > closingprice*5:
                    price_diff_insert = closingprice*5
                else:
                    price_diff_insert = price_diff/denominator
                call_list = []
                put_list = []
                ## GET THE MAX BETWEEN PRICE/DIFF AND PRICE

                if datetoinsert==(todaystring):
                    price_diff = 0
                    callvolume = 0
                    putvolume = 0
                    denominator = 1
                    prevstock = options[i]['SYMBOLS']
                    continue
                datatoinsert = (date.today(), prevstock, datetoinsert, price_diff_insert, callvolume, putvolume)
                execute(sql, datatoinsert, connection)
                datetoinsert = options[i]['optionkey'].split("_")[1][0:6]
                datetoinsert = datetoinsert[0:2]+'-'+datetoinsert[2:4]+'-'+datetoinsert[4:6]
                price_diff = 0
                callvolume = 0
                putvolume = 0
                denominator = 1
                prevstock = options[i]['SYMBOLS']



        except Exception as e:
            print(e)
            print(prevstock)
            print(type(e))
            traceback.print_tb(e.__traceback__)



# creates 2 tables with top 100 up and down.
def stockAggregate(connection):
    cursorinstance = connection.cursor()
    itmcall = 0
    otmcall = 0
    itmput = 0
    otmput = 0
    itmcalldollar = 0
    otmcalldollar = 0
    itmputdollar = 0
    otmputdollar = 0
    itmcalloi = 0
    otmcalloi = 0
    itmputoi = 0
    otmputoi = 0
    callvolume = 0
    putvolume = 0
    calloi = 0
    putoi = 0
    sql = "select * from options ORDER BY SYMBOLS ASC" # get stock symbols, then select * with symbol.
    cursorinstance.execute(sql)
    today = str(date.today().year) + '-' + str(date.today().month) + '-' + str(date.today().day)
    records = cursorinstance.fetchall()
    prevstock = records[0]['SYMBOLS']
    denominator = 0
    dollarestimate = 0
    callperf = 0
    bestcall = records[0]['optionkey']
    worstcall = records[0]['optionkey']
    worstput = ""
    best_call_perf = -1
    best_call_perf_date = today
    worst_call_perf = 999999
    worst_call_perf_date = today
    totalvolume = 0
    totalcalldollar = 0
    totalputdollar = 0
    best_put_perf = -1
    worst_put_perf = 999999
    best_put_perf_date = today
    bestput = ""
    worst_put_perf_date = today
    denominator = 1
    voldenom = 1
    totalotmcall = 0
    totalotmput = 0
    totalitmcall = 0
    totalitmput = 0
    totalotmcoi = 0
    totalotmpoi = 0
    totalitmcoi = 0
    totalitmpoi = 0
    totaldollar = 0
    volatility = 0
    putperf = 0
    type = 'E' if records[0]['isetf'] == 'Y' else 'S'
    sqlstockprice = '''
    SELECT closingprice FROM tickerss WHERE SYMBOLS = %s
    UNION
    SELECT closingprice FROM tickerse WHERE SYMBOLS = %s
    '''
    cursorinstance.execute(sqlstockprice, (prevstock, prevstock))
    result = cursorinstance.fetchone()

    stockprice = result['closingprice']
    for i in range(len(records)):

        if prevstock == records[i]['SYMBOLS']:
            denominator += 1
            dollarestimate += records[i]['volume'] * (records[i]['highPrice'] + records[i]['lowPrice'])/2

            totalvolume += records[i]['volume']
            if records[i]['volume'] != 0:
                volatility += records[i]['volatility']*records[i]['volume']
                voldenom += records[i]['volume']
            if records[i]['volume'] >= 10:
                if records[i]['type'] == 'C':
                    if records[i]['upperformance'] >= best_call_perf:
                        best_call_perf = records[i]['upperformance']
                        best_call_perf_date = records[i]['absLDate']
                        bestcall = records[i]['optionkey']
                    if records[i]['downperformance'] < worst_call_perf:
                        if records[i]['downperformance'] == 0:
                            continue
                        worst_call_perf = records[i]['downperformance']
                        worst_call_perf_date = records[i]['absHDate']
                        worstcall = records[i]['optionkey']
                    callperf += records[i]['upperformance']
                    callvolume += records[i]['volume']
                    calloi += records[i]['openinterest']
                    totalcalldollar += records[i]['volume'] * (records[i]['highPrice'] + records[i]['lowPrice'])/2
                    if stockprice < records[i]['strikeprice']:
                        totalotmcall += records[i]['volume']
                        totalotmcoi += records[i]['openinterest']
                        otmcall += records[i]['volume']
                        totaldollar += (records[i]['highPrice'] + records[i]['lowPrice'])/2 * records[i]['volume']
                        otmcalldollar += (records[i]['highPrice'] + records[i]['lowPrice'])/2 * records[i]['volume']
                        otmcalloi += records[i]['openinterest']
                    elif stockprice >= records[i]['strikeprice']:
                        totalitmcall += records[i]['volume']
                        totalitmcoi += records[i]['openinterest']
                        itmcall += records[i]['volume']
                        totaldollar += (records[i]['highPrice'] + records[i]['lowPrice'])/2 * records[i]['volume']
                        itmcalldollar += (records[i]['highPrice'] + records[i]['lowPrice'])/2 * records[i]['volume']
                        itmcalloi += records[i]['openinterest']
                else:
                    if records[i]['upperformance'] >= best_put_perf:
                        best_put_perf = records[i]['upperformance']
                        best_put_perf_date = records[i]['absLDate']
                        bestput = records[i]['optionkey']
                    if records[i]['downperformance'] < worst_put_perf:
                        if records[i]['downperformance'] == 0:
                            continue
                        worst_put_perf = records[i]['downperformance']
                        worst_put_perf_date = records[i]['absHDate']
                        worstput = records[i]['optionkey']
                    putperf += records[i]['downperformance']
                    totalputdollar += records[i]['volume'] * (records[i]['highPrice'] + records[i]['lowPrice'])/2
                    putvolume += records[i]['volume']
                    putoi += records[i]['openinterest']
                    if stockprice < records[i]['strikeprice']:
                        itmput += records[i]['volume']
                        itmputdollar += (records[i]['highPrice'] + records[i]['lowPrice'])/2 * records[i]['volume']
                        itmputoi += records[i]['openinterest']
                        totalitmput += records[i]['volume']
                        totalitmpoi += records[i]['openinterest']
                        totaldollar += (records[i]['highPrice'] + records[i]['lowPrice'])/2 * records[i]['volume']
                    elif stockprice >= records[i]['strikeprice']:
                        otmput += records[i]['volume']
                        totalotmput += records[i]['volume']
                        totalotmpoi += records[i]['openinterest']
                        otmputdollar += (records[i]['highPrice'] + records[i]['lowPrice'])/2 * records[i]['volume']
                        otmputoi += records[i]['openinterest']
                        totaldollar += (records[i]['highPrice'] + records[i]['lowPrice'])/2 * records[i]['volume']

            #add to volume and price and etc..   the best performing option, and the average performance of options; on both calls/puts.
            #add counter to divide later.
        else:
            try:
                sql = "SELECT avgvola FROM stockaggre WHERE SYMBOLS = '{}'".format(prevstock)
                sqldata = get_records(sql, connection)
                avgvola = volatility/voldenom if len(sqldata)==0 else (sqldata[0]['avgvola'] + volatility/voldenom)/2
                sql = "SELECT avgvolume FROM stockaggre WHERE SYMBOLS = '{}'".format(prevstock)
                sqldata = get_records(sql, connection)
                avgvolume = totalvolume if len(sqldata)==0 else (sqldata[0]['avgvolume'] + totalvolume)/2
                sql = "SELECT avgdollar FROM stockaggre WHERE SYMBOLS = '{}'".format(prevstock)
                sqldata = get_records(sql, connection)
                avgdollar = dollarestimate if len(sqldata)==0 else(sqldata[0]['avgdollar'] + dollarestimate)/2
                if len(sqldata) == 0:
                    sql = '''INSERT INTO stockaggre (SYMBOLS, type, bcallkey, bcallperf, bcalldate, avgcall, worstcallperf,
                    worstcalldate, worstcall, bputkey, bputperf, bputdate, avgput, worstputperf, worstputdate, worstput, callvolume,
                    putvolume, calloi, putoi, volume, avgvolume, dollarestimate, avgdollar, totalcalldollar, totalputdollar, volatility, avgvola,
                    itmotmcratio, itmotmpratio, itmotmcdollarratio, itmotmpdollarratio, itmotmcoiratio, itmotmpoiratio) VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s)'''
                    insertdata = (prevstock, type, bestcall, best_call_perf, best_call_perf_date, callperf/denominator, worst_call_perf, worst_call_perf_date,
                                  worstcall, bestput, best_put_perf, best_put_perf_date, putperf/denominator, worst_put_perf, worst_put_perf_date, worstput,
                                  callvolume, putvolume, calloi, putoi, totalvolume, avgvolume, dollarestimate, avgdollar, totalcalldollar, totalputdollar, volatility/voldenom, avgvola,
                                  1 if itmcall < 50 or otmcall < 50 else itmcall/otmcall, 1 if itmput < 50 or otmput < 50 else itmput/otmput,
                                  1 if itmcalldollar < 5000 or otmcalldollar < 5000 else itmcalldollar/otmcalldollar,
                                  1 if itmputdollar < 5000 or otmputdollar < 5000 else itmputdollar/otmputdollar,
                                  1 if itmcalloi < 100 or otmcalloi < 100 else itmcalloi/otmcalloi,
                                  1 if itmputoi < 100 or otmputoi < 100 else itmputoi/otmputoi)
                    execute(sql, insertdata, connection)
                elif dollarestimate < 5000:
                    sql = "UPDATE stockaggre SET bcallperf = %s, worstcallperf = %s, bputperf = %s, worstputperf = %s WHERE SYMBOLS = %s"
                    insertdata = (50, 50, 50, 50, prevstock)
                    execute(sql, insertdata, connection)
                else:
                    sql = '''UPDATE stockaggre SET  bcallkey = %s, bcallperf = %s, bcalldate = %s, avgcall = %s, worstcallperf = %s, worstcalldate = %s,
                    worstcall = %s, bputkey = %s, bputperf = %s, bputdate = %s, avgput = %s, worstputperf = %s, worstputdate = %s, worstput = %s, callvolume = %s,
                    putvolume = %s, calloi = %s, putoi = %s, volume = %s, avgvolume = %s, dollarestimate = %s, avgdollar = %s, totalcalldollar = %s, totalputdollar = %s, volatility = %s,
                    avgvola = %s, itmotmcratio = %s, itmotmpratio = %s, itmotmcdollarratio = %s, itmotmpdollarratio = %s, itmotmcoiratio = %s,
                    itmotmpoiratio = %s WHERE SYMBOLS = %s'''
                    insertdata = (bestcall, best_call_perf, best_call_perf_date, callperf/denominator, worst_call_perf, worst_call_perf_date, worstcall,
                                  bestput, best_put_perf, best_put_perf_date, putperf/denominator, worst_put_perf, worst_put_perf_date, worstput, callvolume,
                                  putvolume, calloi, putoi, totalvolume, avgvolume, dollarestimate, avgdollar, totalcalldollar, totalputdollar, volatility/voldenom, avgvola,
                                  1 if itmcall < 50 or otmcall < 50 else itmcall/otmcall,
                                  1 if itmput < 50 or otmput < 50 else itmput/otmput,
                                  1 if itmcalldollar < 5000 or otmcalldollar < 5000 else itmcalldollar/otmcalldollar,
                                  1 if itmputdollar < 5000 or otmputdollar < 5000 else itmputdollar/otmputdollar,
                                  1 if itmcalloi < 100 or otmcalloi < 100 else itmcalloi/otmcalloi,
                                  1 if itmputoi < 100 or otmputoi < 100 else itmputoi/otmputoi, prevstock)
                    execute(sql, insertdata, connection)
            except Exception as e:
                print(f"Exception: {e}")
                traceback.print_tb(e.__traceback__)
            prevstock = records[i]['SYMBOLS']
            denominator = 1
            totalvolume = records[i]['volume']
            volatility = records[i]['volatility']*records[i]['volume']
            voldenom = 1 if records[i]['volume']==0 else records[i]['volume']
            type = 'E' if records[i]['isetf'] == 'Y' else 'S'

            dollarestimate = records[i]['volume'] * (records[i]['highPrice'] + records[i]['lowPrice'])/2

            cursorinstance.execute(sqlstockprice, (prevstock, prevstock))
            result = cursorinstance.fetchone()


            stockprice = result['closingprice']
            itmcall = 0
            otmcall = 0
            itmput = 0
            otmput = 0
            itmcalldollar = 0
            otmcalldollar = 0
            itmputdollar = 0
            otmputdollar = 0
            itmcalloi = 0
            otmcalloi = 0
            calloi = 0
            putoi = 0
            itmputoi = 0
            callvolume = 0
            putvolume = 0
            otmputoi = 0
            if records[i]['type'] == 'C':
                if stockprice < records[i]['strikeprice']:
                    otmcall += records[i]['volume']
                    otmcalldollar += (records[i]['highPrice'] + records[i]['lowPrice'])/2 * records[i]['volume']
                    otmcalloi += records[i]['openinterest']
                elif stockprice >= records[i]['strikeprice']:
                    itmcall += records[i]['volume']
                    itmcalldollar += (records[i]['highPrice'] + records[i]['lowPrice'])/2 * records[i]['volume']
                    itmcalloi += records[i]['openinterest']
                best_call_perf = records[i]['upperformance']
                best_call_perf_date = records[i]['absLDate']
                bestcall = records[i]['optionkey']
                worst_call_perf = records[i]['downperformance']
                worst_call_perf_date = records[i]['absHDate']
                worstcall = records[i]['optionkey']
                callperf = records[i]['upperformance']
                totalcalldollar = records[i]['volume'] * (records[i]['highPrice'] + records[i]['lowPrice'])/2
                worst_put_perf = 99999
                callvolume = records[i]['volume']
                calloi = records[i]['openinterest']
                best_put_perf = -1
                best_put_perf_date = today
                bestput = ""
                worst_call_perf = 99999
                worst_put_perf_date = today
                worstput = ""
                putperf = 0
                totalputdollar = 0
            else:
                if stockprice < records[i]['strikeprice']:
                    itmput += records[i]['volume']
                    itmputdollar += (records[i]['highPrice'] + records[i]['lowPrice'])/2 * records[i]['volume']
                    itmputoi += records[i]['openinterest']
                elif stockprice >= records[i]['strikeprice']:
                    otmput += records[i]['volume']
                    otmputdollar += (records[i]['highPrice'] + records[i]['lowPrice'])/2 * records[i]['volume']
                    otmputoi += records[i]['openinterest']
                best_put_perf = records[i]['upperformance']
                best_put_perf_date = records[i]['absLDate']
                bestput = records[i]['optionkey']
                worst_call_perf = records[i]['downperformance']
                worst_put_perf_date = records[i]['absHDate']
                worstput = records[i]['optionkey']
                worst_put_perf = 99999
                putperf = records[i]['upperformance']
                totalputdollar = records[i]['volume'] * (records[i]['highPrice'] + records[i]['lowPrice'])/2
                putvolume = records[i]['volume']
                putoi = records[i]['openinterest']
                best_call_perf = -1
                best_call_perf_date = today
                bestcall = ""
                worst_call_perf = 999999
                worst_call_perf_date = today
                worstcall = ""
                callperf = 0
                totalcalldollar = 0
    sqlfinal = "SELECT * from overallstats"
    cursorinstance.execute(sqlfinal)
    records = cursorinstance.fetchall()
    deleteALL("overallstats", connection)
    if len(records) == 0:
        datatoinsert = (totalotmcall, totalotmput, totalitmcall, totalitmput, totalotmcoi, totalitmcoi, totalotmpoi, totalitmpoi,
                        totaldollar, totalotmcall, totalotmput, totalitmcall, totalitmput, totalotmcoi, totalitmcoi, totalotmpoi,
                        totalitmpoi, totaldollar)
    else:
        datatoinsert = (totalotmcall, totalotmput, totalitmcall, totalitmput, totalotmcoi, totalitmcoi, totalotmpoi, totalitmpoi,
                        totaldollar, (records[0]['avgtotalotmcall']+totalotmcall)/2, (records[0]['avgtotalotmput']+totalotmput)/2,
                        (records[0]['avgtotalitmcall']+totalitmcall)/2, (records[0]['avgtotalitmput']+totalitmput)/2,
                        (records[0]['avgtotalotmcoi']+totalotmcoi)/2, (records[0]['avgtotalotmpoi']+totalotmpoi)/2,
                        (records[0]['avgtotalitmcoi']+totalitmcoi)/2, (records[0]['avgtotalitmpoi']+totalitmpoi)/2,
                        (records[0]['avgtotaldollar']+totaldollar)/2)
    sqlfinal = '''INSERT INTO overallstats (totalotmcall, totalotmput, totalitmcall, totalitmput, totalotmcoi,totalitmcoi,totalotmpoi,totalitmpoi,totaldollar,avgtotalotmcall,
    avgtotalotmput,avgtotalitmcall,avgtotalitmput,avgtotalotmcoi,avgtotalotmpoi,avgtotalitmcoi,avgtotalitmpoi,avgtotaldollar) VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    execute(sqlfinal, datatoinsert, connection)

def keybreakdown(key):
    underscore_index = key.index("_") + 1
    CP_index = key.index("C", underscore_index) if "C" in key[underscore_index:] else key.index("P", underscore_index)
    dat = key[underscore_index:CP_index]
    dat = dat[0:2]+'-'+dat[2:4]+'-'+"20"+dat[4:6]
    strike = key[CP_index + 1:]
    return (dat, strike)

def distribute(connection):
    cursorinstance = connection.cursor()
    deleteALL("top100bcperf", connection)

    select_query = "SELECT bcallkey from stockaggre ORDER BY bcallperf DESC LIMIT 100"
    cursorinstance.execute(select_query)
    results = cursorinstance.fetchall()
    processed_key = [keybreakdown(row['bcallkey']) for row in results]

    select_query = '''
    SELECT stockaggre.SYMBOLS, stockaggre.bcallperf, stockaggre.bcalldate,
    stockaggre.avgcall, stockaggre.avgvola, stockaggre.volume, stockaggre.avgvolume,
    COALESCE(tickerss.description, tickerse.description) as description,
    COALESCE(tickerss.INDUSTRY, tickerse.CATEGORY) as CATEGORY,
    COALESCE(tickerss.pricechange, tickerse.pricechange) as pricechange,
    COALESCE(tickerss.percentchange, tickerse.percentchange) as percentchange,
    COALESCE(tickerss.closingprice, tickerse.closingprice) as closingprice FROM stockaggre
    LEFT JOIN tickerss ON stockaggre.SYMBOLS = tickerss.SYMBOLS
    LEFT JOIN tickerse ON stockaggre.SYMBOLS = tickerse.SYMBOLS
    ORDER BY bcallperf DESC LIMIT 100;
    '''
    insertdata = []
    cursorinstance.execute(select_query)
    results = cursorinstance.fetchall()
    print(results)
    for i in range(len(results)):
        insertdata.append((results[i]["SYMBOLS"], results[i]['bcallperf'], results[i]['bcalldate'], results[i]['avgcall'],
        results[i]['avgvola'], results[i]['volume'], results[i]['avgvolume'], results[i]['description'], results[i]['CATEGORY'], results[i]['pricechange'],
        results[i]['percentchange'], results[i]['closingprice'], processed_key[i][0], processed_key[i][1]))
    print(insertdata)
    sql = '''INSERT INTO top100bcperf (SYMBOLS, bcallperf, bcalldate, avgcall, avgvola, volume, avgvolume, description,
            category, pricechange, percentchange, closingprice, strikedate, strikeprice)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
    executemany(sql, insertdata, connection)
    print("hi")




    deleteALL("top100bpperf", connection)
    select_query = "SELECT stockaggre.bputkey from stockaggre ORDER BY bputperf DESC LIMIT 100"
    cursorinstance.execute(select_query)
    results = cursorinstance.fetchall()

    processed_key = [keybreakdown(row['bputkey']) for row in results]

    select_query = '''
    SELECT stockaggre.SYMBOLS, stockaggre.bputperf, stockaggre.bputdate,
    stockaggre.avgput, stockaggre.avgvola, stockaggre.volume, stockaggre.avgvolume,
    COALESCE(tickerss.description, tickerse.description) as description,
    COALESCE(tickerss.INDUSTRY, tickerse.CATEGORY) as CATEGORY,
    COALESCE(tickerss.pricechange, tickerse.pricechange) as pricechange,
    COALESCE(tickerss.percentchange, tickerse.percentchange) as percentchange,
    COALESCE(tickerss.closingprice, tickerse.closingprice) as closingprice FROM stockaggre
    LEFT JOIN tickerss ON stockaggre.SYMBOLS = tickerss.SYMBOLS
    LEFT JOIN tickerse ON stockaggre.SYMBOLS = tickerse.SYMBOLS
    ORDER BY bputperf DESC LIMIT 100;
    '''
    insertdata = []
    cursorinstance.execute(select_query)
    results = cursorinstance.fetchall()
    print(results)
    for i in range(len(results)):
        insertdata.append((results[i]["SYMBOLS"], results[i]['bputperf'], results[i]['bputdate'], results[i]['avgput'],
        results[i]['avgvola'], results[i]['volume'], results[i]['avgvolume'],results[i]['description'], results[i]['CATEGORY'], results[i]['pricechange'],
        results[i]['percentchange'], results[i]['closingprice'], processed_key[i][0], processed_key[i][1]))
    sql = '''INSERT INTO top100bpperf (SYMBOLS, bputperf, bputdate, avgput, avgvola, volume, avgvolume, description,
            category, pricechange, percentchange, closingprice, strikedate, strikeprice)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
    executemany(sql, insertdata, connection)


    ## worst calls from below
    deleteALL("top100wcperf", connection)
    select_query = "SELECT worstcall from stockaggre ORDER BY worstcallperf ASC LIMIT 100"
    cursorinstance.execute(select_query)
    results = cursorinstance.fetchall()

    processed_key = [keybreakdown(row["worstcall"]) for row in results]

    select_query = '''
    SELECT stockaggre.SYMBOLS, stockaggre.worstcallperf, stockaggre.worstcalldate,
    stockaggre.avgcall, stockaggre.avgvola, stockaggre.volume, stockaggre.avgvolume,
    COALESCE(tickerss.description, tickerse.description) as description,
    COALESCE(tickerss.INDUSTRY, tickerse.CATEGORY) as CATEGORY,
    COALESCE(tickerss.pricechange, tickerse.pricechange) as pricechange,
    COALESCE(tickerss.percentchange, tickerse.percentchange) as percentchange,
    COALESCE(tickerss.closingprice, tickerse.closingprice) as closingprice FROM stockaggre
    LEFT JOIN tickerss ON stockaggre.SYMBOLS = tickerss.SYMBOLS
    LEFT JOIN tickerse ON stockaggre.SYMBOLS = tickerse.SYMBOLS

    ORDER BY worstcallperf ASC LIMIT 100;
    '''
    insertdata = []
    cursorinstance.execute(select_query)
    results = cursorinstance.fetchall()
    for i in range(len(results)):
        insertdata.append((results[i]["SYMBOLS"], results[i]['worstcallperf'], results[i]['worstcalldate'], results[i]['avgcall'],
        results[i]['avgvola'], results[i]['volume'], results[i]['avgvolume'],results[i]['description'], results[i]['CATEGORY'], results[i]['pricechange'],
        results[i]['percentchange'], results[i]['closingprice'], processed_key[i][0], processed_key[i][1]))
    sql = '''INSERT INTO top100wcperf (SYMBOLS, wcallperf, wcalldate, avgcall, avgvola, volume, avgvolume, description,
            category, pricechange, percentchange, closingprice, strikedate, strikeprice)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
    executemany(sql, insertdata, connection)






    ## worst puts from below

    deleteALL("top100wpperf", connection)

    select_query = "SELECT worstput from stockaggre ORDER BY worstputperf ASC LIMIT 100"
    cursorinstance.execute(select_query)
    results = cursorinstance.fetchall()

    processed_key = [keybreakdown(row["worstput"]) for row in results]

    select_query = '''
    SELECT stockaggre.SYMBOLS, stockaggre.worstputperf, stockaggre.worstputdate,
    stockaggre.avgput, stockaggre.avgvola, stockaggre.volume, stockaggre.avgvolume,
    COALESCE(tickerss.description, tickerse.description) as description,
    COALESCE(tickerss.INDUSTRY, tickerse.CATEGORY) as CATEGORY,
    COALESCE(tickerss.pricechange, tickerse.pricechange) as pricechange,
    COALESCE(tickerss.percentchange, tickerse.percentchange) as percentchange,
    COALESCE(tickerss.closingprice, tickerse.closingprice) as closingprice FROM stockaggre
    LEFT JOIN tickerss ON stockaggre.SYMBOLS = tickerss.SYMBOLS
    LEFT JOIN tickerse ON stockaggre.SYMBOLS = tickerse.SYMBOLS

    ORDER BY worstputperf ASC LIMIT 100;
    '''
    insertdata = []
    cursorinstance.execute(select_query)
    results = cursorinstance.fetchall()
    for i in range(len(results)):
        insertdata.append((results[i]["SYMBOLS"], results[i]['worstputperf'], results[i]['worstputdate'], results[i]['avgput'],
        results[i]['avgvola'], results[i]['volume'], results[i]['avgvolume'], results[i]['description'], results[i]['CATEGORY'], results[i]['pricechange'],
        results[i]['percentchange'], results[i]['closingprice'], processed_key[i][0], processed_key[i][1]))
    sql = '''INSERT INTO top100wpperf (SYMBOLS, wputperf, wputdate, avgput, avgvola, volume, avgvolume, description,
            category, pricechange, percentchange, closingprice, strikedate, strikeprice)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
    executemany(sql, insertdata, connection)
