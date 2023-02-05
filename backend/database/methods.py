import pymysql
import pymysql.cursors

cursorType = pymysql.cursors.DictCursor
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='8155',
    database = "testdatabase",
    cursorclass=cursorType,
)

cursorinstance = connection.cursor()

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

def execute(sqlstmt, data):
    cursorinstance.execute(sqlstmt, data)
    connection.commit()

def getTable(table):
    sql = "select * from {}".format(table)
    cursorinstance.execute(sql)
    records = cursorinstance.fetchall()
    return records

def getETF():
    sql = "select * from tickerse"
    cursorinstance.execute(sql)
    records = cursorinstance.fetchall()
    return records

def getStock():
    sql = "select * from tickerss"
    cursorinstance.execute(sql)
    records = cursorinstance.fetchall()
    return records

def deleteALL(table):
    sql = "DELETE FROM {}".format(table)
    cursorinstance.execute(sql)
    connection.commit()

def checkOptionPK(key):
    sql = "SELECT * FROM options WHERE optionkey = %s"
    cursorinstance.execute(sql, key)
    records = cursorinstance.fetchall()
    return records

def deleteExpired():
    sql = "DELETE FROM options WHERE daysToExpiration = 0"
    cursorinstance.execute(sql)
    connection.commit()


# creates 2 tables with top 100 up and down.
def stockAggregate():

    deleteALL("stockaggre")
    deleteALL("stockeaggre")

    sql = "select * from stocks ORDER BY SYMBOLS ASC" # get stock symbols, then select * with symbol.
    cursorinstance.execute(sql)
    records = cursorinstance.fetchall()
    prevstock = records[0]['SYMBOL']
    denominator = 0
    dollarestimate = 0
    callperf = 0
    best_call_perf = 0
    worst_call_perf = 0
    totalvolume = 0
    totalcalldollar = 0
    totalputdollar = 0
    best_put_perf = 0
    worst_put_perf = 0
    putperf = 0
    for i in range(records):
        
        if prevstock == records[i]['SYMBOL']:
            denominator += 1
            dollarestimate += records[i]['volume'] * (records[i]['highPrice'] + records[i]['lowPrice'])/2

            totalvolume += records[i]['volume']
            if records[i]['type'] == 'C':
                type = 'C'
                if records[i]['upperformance'] > best_call_perf:
                    best_call_perf = records[i]['upperformance']
                    best_call_perf_date = records[i]['absLDate']
                    bestcall = records[i]['optionkey']
                if records[i]['downperformance'] < worst_call_perf:
                    worst_call_perf = records[i]['downperformance']
                    worst_call_perf_date = records[i]['absHDate']
                    worstcall = records[i]['optionkey']
                callperf += records[i]['upperformance']
                totalcalldollar += records[i]['volume'] * (records[i]['highPrice'] + records[i]['lowPrice'])/2
            else:
                type = 'P'
                if records[i]['upperformance'] > best_put_perf:
                    best_put_perf = records[i]['upperformance']
                    best_put_perf_date = records[i]['absLDaate']
                    bestput = records[i]['optionkey']
                if records[i]['downperformance'] < worst_put_perf:
                    worst_put_perf = records[i]['downperformance']
                    worst_put_perf_date = records[i]['absHDate']
                    worstput = records[i]['optionkey']
                putperf += records[i]['downperformance']
                totalputdollar += records[i]['volume'] * (records[i]['highPrice'] + records[i]['lowPrice'])/2
            
            #add to volume and price and etc..   the best performing option, and the average performance of options; on both calls/puts. 
            #add counter to divide later.
        else:
            sql = "INSERT INTO stockaggre (SYMBOLS, etf, bcallkey, bcallperf, bcalldate, avgcall, worstcallperf, worstcalldate, worstcall, bputkey, bputperf, bputdate, avgput, worstputperf, worstputdate, worstput, volume, totalcalldollar, totalputdollar) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            insertdata = (prevstock, type, bestcall, best_call_perf, best_call_perf_date, callperf/denominator, worst_call_perf, worst_call_perf_date, worstcall, bestput, best_put_perf, best_put_perf_date, putperf/denominator, worst_put_perf, worst_put_perf_date, worstput,dollarestimate, totalcalldollar, totalputdollar)
            execute(sql, insertdata)
            prevstock = records[i]['SYMBOL']
            denominator = 1
            totalvolume = records[i]['volume']
            dollarestimate = records[i]['volume'] * (records[i]['highPrice'] + records[i]['lowPrice'])/2
            if records[i]['type'] == 'C':
                type = 'C'
                if records[i]['upperformance'] > best_call_perf:
                    best_call_perf = records[i]['upperformance']
                    best_call_perf_date = records[i]['absLDate']
                    bestcall = records[i]['optionkey']
                if records[i]['downperformance'] < worst_call_perf:
                    worst_call_perf = records[i]['downperformance']
                    worst_call_perf_date = records[i]['absHDate']
                    worstcall = records[i]['optionkey']
                callperf = records[i]['upperformance']
                totalcalldollar = records[i]['volume'] * (records[i]['highPrice'] + records[i]['lowPrice'])/2
            else:
                type = 'P'
                if records[i]['upperformance'] > best_put_perf:
                    best_put_perf = records[i]['upperformance']
                    best_put_perf_date = records[i]['absLDaate']
                    bestput = records[i]['optionkey']
                if records[i]['downperformance'] < worst_put_perf:
                    worst_call_perf = records[i]['downperformance']
                    worst_put_perf_date = records[i]['absHDate']
                    worstput = records[i]['optionkey']
                putperf = records[i]['upperformance']
                totalputdollar = records[i]['volume'] * (records[i]['highPrice'] + records[i]['lowPrice'])/2

def distribute():
    deleteALL("top100bcperf")
    top100bcperf = "INSERT INTO top100bcperf (SELECT * FROM stockaggre ORDER BY bcallperf ASC LIMIT 100)"
    cursorinstance.execute(top100bcperf)

    deleteALL("top100bpperf")
    top100bpperf = "INSERT INTO top100bpperf (SELECT * FROM stockaggre ORDER BY bputperf ASC LIMIT 100)"
    cursorinstance.execute(top100bpperf)

    deleteALL("top100wcperf")
    top100wcperf = "INSERT INTO top100bwcerf (SELECT * FROM stockaggre ORDER BY worstcallperf ASC LIMIT 100)"
    cursorinstance.execute(top100wcperf)

    deleteALL("top100wpperf")
    top100wpperf = "INSERT INTO top100wpperf (SELECT * FROM stockaggre ORDER BY worstputperf ASC LIMIT 100)"
    cursorinstance.execute(top100wpperf)


