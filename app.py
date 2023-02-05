from flask import Flask
from backend import test


app = Flask(__name__)

app.config.from_pyfile('flaskconfig.py')



@app.route("/")
def serve():
    return "lel"

@app.route("/lel")
def givehimlel():
    return "its lel!"



if __name__ == '__main__':
    ## async function start, generating new data in pure backend.
    ## 
    app.run(debug=True, port=80)

