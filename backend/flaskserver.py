from flask import Flask
import tdamodule.tdamethods
import database.methods as DBmethods
from flask import jsonify

app = Flask("OPTIONSTATS")

@app.route('/api/sectors')
def get_sectors():
    try:
        connection = DBmethods.acquire_connection()
        sectors = DBmethods.get_sector(connection)

        return sectors
    finally:
        DBmethods.release_connection(connection)

@app.route('/api/<table>')
def gettable(table):
    try:
        connection = DBmethods.acquire_connection()
        print("connection acquired")
        data = DBmethods.getTableJson(table, connection)
        print("data got")
        return data
    # return json format, like
    # return {'data': data}, need to make sure what json format react table requires.
    finally:
        print("releasing connection back to pool")
        DBmethods.release_connection(connection)

@app.route('/api/expectation/<symbol>')
def get_expectation(symbol):
    try:
        connection = DBmethods.acquire_connection()
        chartdata = DBmethods.get_chartdata(symbol, connection)
        stockdata = DBmethods.get_stock_info(symbol, connection)
        result = {
            'chartdata': chartdata,
            'stockdata': stockdata.get_json()
        }
        return result
    except Exception as e:
        print(e)
    finally:
        DBmethods.release_connection(connection)

if __name__ == "__main__":
    app.run(debug=True)
