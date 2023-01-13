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
