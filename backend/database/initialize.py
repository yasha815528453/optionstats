## create all the main tables,
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

## 2 main tables
## tickers table,

#normal stocks
sql = '''CREATE TABLE tickersS(
    SYMBOLS CHAR(5) NOT NULL,
    SECTORS VARCHAR(255) NOT NULL,
    INDUSTRY VARCHAR(255) NOT NULL,
    OptionSize int NOT NULL,
    PRIMARY KEY (SYMBOLS)
    )'''

cursorinstance.execute(sql)


#etfs 
sql = '''CREATE TABLE tickersE(
    SYMBOLS CHAR(5) NOT NULL,
    CATEGORY VARCHAR(255) NOT NULL,
    OptionSize int NOT NULL,
    PRIMARY KEY (SYMBOLS)
    )'''

cursorinstance.execute(sql)


## options table
sql = '''CREATE TABLE options(
    optionkey VARCHAR(255) NOT NULL,
    type CHAR(1) NOT NULL,
    SYMBOLS CHAR(5) NOT NULL,
    marketprice float NOT NULL,
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
    isetf CHAR(1) NOT NULL,
    PRIMARY KEY (optionkey)
    )'''

cursorinstance.execute(sql)



## other small tables for data feed.



#most gains 
sql = '''CREATE TABLE gains(
    optionkey VARCHAR(255) NOT NULL,
    SYMBOLS CHAR(5) NOT NULL,
    absLow float NOT NULL,
    absHigh float NOT NULL,
    absLDate DATE NOT NULL,
    absHDate DATE NOT NULL,
    volatility float NOT NULL,
    performance float NOT NULL,
    )'''
cursorinstance.execute(sql)


#most losses
sql = '''CREATE TABLE losses(
    optionkey VARCHAR(255) NOT NULL,
    SYMBOLS CHAR(5) NOT NULL,
    absLow float NOT NULL,
    absHigh float NOT NULL,
    absLDate DATE NOT NULL,
    absHDate DATE NOT NULL,
    volatility float NOT NULL,
    performance float NOT NULL,
    )'''
cursorinstance.execute(sql)


#stock insight
#performance aggregated 
sql = '''CREATE TABLE stockaggre(
    SYMBOLS CHAR(5) NOT NULL,
    type CHAR(1) NOT NULL,
    bcallkey VARCHAR(255) NOT NULL,
    bcallperf float NOT NULL,
    bcalldate DATE NOT NULL,
    avgcall float NOT NULL,
    bputkey VARCHAR(255) NOT NULL,
    bputperf float NOT NULL,
    bputdate DATE NOT NULL,
    avgput float NOT NULL,
    volume INT NOT NULL,
    totalcalldollar INT NOT NULL,
    totalputdollar INT NOT NULL,
    PRIMARY KEY (SYMBOLS)
    )'''
cursorinstance.execute(sql)

sql = '''CREATE TABLE top100perf(
    SYMBOLS CHAR(5) NOT NULL,
    type CHAR(1) NOT NULL,
    bcallkey VARCHAR(255) NOT NULL,
    bcallperf float NOT NULL,
    bcalldate DATE NOT NULL,
    avgcall float NOT NULL,
    bputkey VARCHAR(255) NOT NULL,
    bputperf float NOT NULL,
    bputdate DATE NOT NULL,
    avgput float NOT NULL,
    volume INT NOT NULL,
    totalcalldollar INT NOT NULL,
    totalputdollar INT NOT NULL,
    PRIMARY KEY (SYMBOLS)
    )'''
cursorinstance.execute(sql)

