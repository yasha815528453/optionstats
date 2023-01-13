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


sqlstmt = "SHOW DATABASES"
cursorinstance.execute(sqlstmt)

datablist = cursorinstance.fetchall()

for datab in datablist:
    print(datab)
