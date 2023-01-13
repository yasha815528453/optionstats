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


# sql = '''CREATE TABLE tickersS(
#     SYMBOLS CHAR(5) NOT NULL,
#     SECTORS VARCHAR(255) NOT NULL,
#     INDUSTRY VARCHAR(255) NOT NULL,
#     OptionSize int NOT NULL,
#     PRIMARY KEY (SYMBOLS)
#     )'''

# cursorinstance.execute(sql)

# sql = '''CREATE TABLE tickersE(
#     SYMBOLS CHAR(5) NOT NULL,
#     CATEGORY VARCHAR(255) NOT NULL,
#     OptionSize int NOT NULL,
#     PRIMARY KEY (SYMBOLS)
#     )'''

# cursorinstance.execute(sql)


## options table

sql = '''CREATE TABLE options(
    optionkey VARCHAR(255) NOT NULL,
    SYMBOLS CHAR(5) NOT NULL,
    daysToExpiration int NOT NULL,
    lowPrice float NOT NULL,
    highPrice float NOT NULL,
    absLow float NOT NULL,
    absHigh float NOT NULL,
    absLDate DATE NOT NULL,
    absHDate DATE NOT NULL,
    volatility float NOT NULL,
    delta float NOT NULL,
    gamma float NOT NULL,
    theta float NOT NULL,
    vega float NOT NULL,
    theoreticalOptionValue float NOT NULL,
    lastupdate DATE NOT NULL,
    upperformance float NOT NULL,
    downperformance float NOT NULL,
    PRIMARY KEY (optionkey)
    )'''

cursorinstance.execute(sql)



## other small tables for data feed.
