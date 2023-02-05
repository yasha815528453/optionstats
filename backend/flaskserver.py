from flask import Flask
import tdamodule.tdamethods
import database.methods as DBmethods

app = Flask("OPTIONSTATS")

@app.route('/api/<table>')
def gettable(table):
    data = DBmethods.getTable(table)
    return data
    # return json format, like
    # return {'data': data}, need to make sure what json format react table requires.



if __name__ == "__main__":
    app.run(debug=True)
