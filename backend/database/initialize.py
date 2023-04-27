## create all the main tables,
import pymysql
import pymysql.cursors


cursorType = pymysql.cursors.DictCursor

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='8155',
    cursorclass=cursorType,
)
cursorinstance = connection.cursor()
cursorinstance.execute("CREATE DATABASE optionsdb")

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='8155',
    database = "optionsdb",
    cursorclass=cursorType,
)

cursorinstance = connection.cursor()

## 2 main tables
## tickers table,

#normal stocks
sql = '''CREATE TABLE tickersS(
    SYMBOLS CHAR(5) NOT NULL,
    SECTORS VARCHAR(255) NOT NULL,
    INDUSTRY VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    OptionSize int NOT NULL,
    description VARCHAR(255) NOT NULL,
    pricechange float NOT NULL,
    percentchange float NOT NULL,
    closingprice float NOT NULL,
    PRIMARY KEY (SYMBOLS)
    )'''

cursorinstance.execute(sql)


#etfs
sql = '''CREATE TABLE tickersE(
    SYMBOLS CHAR(5) NOT NULL,
    CATEGORY VARCHAR(255) NOT NULL,
    OptionSize int NOT NULL,
    description VARCHAR(255) NOT NULL,
    pricechange float NOT NULL,
    percentchange float NOT NULL,
    closingprice float NOT NULL,
    PRIMARY KEY (SYMBOLS)
    )'''

cursorinstance.execute(sql)


## options table
sql = '''CREATE TABLE options(
    optionkey VARCHAR(255) NOT NULL,
    type CHAR(1) NOT NULL,
    SYMBOLS CHAR(5) NOT NULL,
    strikeprice float NOT NULL,
    marketprice float NOT NULL,
    bid float NOT NULL,
    ask float NOT NULL,
    daysToExpiration int NOT NULL,
    lowPrice float NOT NULL,
    highPrice float NOT NULL,
    absLow float NOT NULL,
    absHigh float NOT NULL,
    absLDate DATE NOT NULL,
    absHDate DATE NOT NULL,
    volatility float NOT NULL,
    volume int NOT NULL,
    openinterest int NOT NULL,
    delta float NOT NULL,
    gamma float NOT NULL,
    theta float NOT NULL,
    vega float NOT NULL,
    theoreticalOptionValue float NOT NULL,
    lastupdate DATE NOT NULL,
    upperformance float NOT NULL,
    downperformance float NOT NULL,
    rho float NOT NULL,
    isetf CHAR(1) NOT NULL,
    PRIMARY KEY (optionkey)
    )'''

cursorinstance.execute(sql)



sql = '''CREATE TABLE sectoraggre(
    INDUSTRY VARCHAR(255) NOT NULL,
    volatility float NOT NULL,
    avgvolatility float NOT NULL,
    dollarestimate INT NOT NULL,
    avgdollar INT NOT NULL,
    volume INT NOT NULL,
    avgvolume INT NOT NULL,
    avgcallperf float NOT NULL,
    avgputperf float NOT NULL,
    PRIMARY KEY (INDUSTRY)
    )'''
cursorinstance.execute(sql)


## other small tables for data feed.
#stock insight
#performance aggregated
sql = '''CREATE TABLE stockaggre(
    SYMBOLS CHAR(5) NOT NULL,
    type CHAR(1) NOT NULL,
    bcallkey VARCHAR(255) NOT NULL,
    bcallperf float NOT NULL,
    bcalldate DATE NOT NULL,
    avgcall float NOT NULL,
    worstcallperf float NOT NULL,
    worstcalldate DATE NOT NULL,
    worstcall VARCHAR(255) NOT NULL,
    bputkey VARCHAR(255) NOT NULL,
    bputperf float NOT NULL,
    bputdate DATE NOT NULL,
    avgput float NOT NULL,
    worstputperf float NOT NULL,
    worstputdate DATE NOT NULL,
    worstput VARCHAR(255) NOT NULL,
    volume INT NOT NULL,
    avgvolume INT NOT NULL,
    dollarestimate INT NOT NULL,
    avgdollar INT NOT NULL,
    totalcalldollar INT NOT NULL,
    totalputdollar INT NOT NULL,
    volatility float NOT NULL,
    avgvola float NOT NULL,
    PRIMARY KEY (SYMBOLS)
    )'''
cursorinstance.execute(sql)

#dateaggregated table

sql = '''CREATE TABLE dstock(
    record_date DATE NOT NULL,
    symbol CHAR(5) NOT NULL,
    compiledate CHAR(8) NOT NULL,
    pcdiff float NOT NULL,
    callvol INT NOT NULL,
    putvol INT NOT NULL
)'''
cursorinstance.execute(sql)

sql = '''CREATE TABLE sstock(
    record_date DATE NOT NULL,
    SECTORS VARCHAR(255) NOT NULL,
    compiledate CHAR(8) NOT NULL,
    pcdiff float NOT NULL,
    callvol INT NOT NULL,
    putvol INT NOT NULL
)'''
cursorinstance.execute(sql)


#the four tables that shows ranking below..

sql = '''CREATE TABLE top100bcperf(
    SYMBOLS CHAR(5) NOT NULL,
    bcallperf float NOT NULL,
    bcalldate VARCHAR(255) NOT NULL,
    avgcall float NOT NULL,
    avgvola float NOT NULL,
    volume INT NOT NULL,
    avgvolume INT NOT NULL,
    description VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    pricechange float NOT NULL,
    percentchange float NOT NULL,
    closingprice float NOT NULL,
    strikedate VARCHAR(255) NOT NULL,
    strikeprice VARCHAR(255) NOT NULL
    )'''
cursorinstance.execute(sql)

sql = '''CREATE TABLE top100bpperf(
    SYMBOLS CHAR(5) NOT NULL,
    bputperf float NOT NULL,
    bputdate VARCHAR(255) NOT NULL,
    avgput float NOT NULL,
    avgvola float NOT NULL,
    volume INT NOT NULL,
    avgvolume INT NOT NULL,
    description VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    pricechange float NOT NULL,
    percentchange float NOT NULL,
    closingprice float NOT NULL,
    strikedate VARCHAR(255) NOT NULL,
    strikeprice VARCHAR(255) NOT NULL
    )'''
cursorinstance.execute(sql)

sql = '''CREATE TABLE top100wcperf(
    SYMBOLS CHAR(5) NOT NULL,
    wcallperf float NOT NULL,
    wcalldate VARCHAR(255) NOT NULL,
    avgcall float NOT NULL,
    avgvola float NOT NULL,
    volume INT NOT NULL,
    avgvolume INT NOT NULL,
    description VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    pricechange float NOT NULL,
    percentchange float NOT NULL,
    closingprice float NOT NULL,
    strikedate VARCHAR(255) NOT NULL,
    strikeprice VARCHAR(255) NOT NULL
    )'''
cursorinstance.execute(sql)

sql = '''CREATE TABLE top100wpperf(
    SYMBOLS CHAR(5) NOT NULL,
    wputperf float NOT NULL,
    wputdate VARCHAR(255) NOT NULL,
    avgput float NOT NULL,
    avgvola float NOT NULL,
    volume INT NOT NULL,
    avgvolume INT NOT NULL,
    description VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    pricechange float NOT NULL,
    percentchange float NOT NULL,
    closingprice float NOT NULL,
    strikedate VARCHAR(255) NOT NULL,
    strikeprice VARCHAR(255) NOT NULL
    )'''
cursorinstance.execute(sql)


# chart that shows future expectation of stocks.
# and maybe a graph of something similar put-call skew, with x axis being dates,
# and y axis being the price difference between call & puts, like a dot.
# maybe use redis, directly call it from the big options table.

sql = '''CREATE TABLE miscellaneous(
    timestamp VARCHAR(255) NOT NULL
)'''
