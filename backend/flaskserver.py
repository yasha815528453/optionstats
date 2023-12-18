from dotenv import load_dotenv
load_dotenv()
from flask import Flask, g, request
import tdamodule.tdamethods
from database.database_client import DbReadingManager, DbWritingManager
from flask import jsonify
import json

DBWriteManager = DbWritingManager()
DBReadManager = DbReadingManager()
app = Flask("OPTIONSTATS")


@app.route('/api/stats/<symbol>')
def get_stats(symbol):
    try:

        stats = DBReadManager.get_stats(symbol)

        return stats
    except Exception as e:
        print(e)

@app.route('/api/top10/<order>/<value>')
def get_topten(order, value):

    try:
        top10 = DBReadManager.get_top_10(order, value)

        return json.dumps(top10)
    except Exception as e:
        print(e)



@app.route('/api/sectors')
def get_sectors():
    try:
        sectors = DBReadManager.get_sector_aggre()
        return sectors
    except Exception as e:
        print(e)

@app.route('/api/<table>')
def gettable(table):
    try:
        data = DBReadManager.get_table_json(table)

        return data
    # return json format, like
    # return {'data': data}, need to make sure what json format react table requires.
    except Exception as e:
        print(e)


@app.route('/api/timestamp')
def getTime():
    try:

        timestamp = DBReadManager.get_time_stamp()
        return timestamp
    except Exception as e:
        print(e)

@app.route('/api/expectation/<symbol>')
def get_expectation(symbol):
    try:

        chartdata = DBReadManager.get_expec_chart(symbol)
        stockdata = DBReadManager.get_stock_info(symbol)
        result = {
            'chartdata': chartdata,
            'stockdata': stockdata,
        }
        return json.dumps(result)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    app.run(debug=True)
