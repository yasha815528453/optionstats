from flask import Flask
from backend import test

app = Flask(__name__)

@app.route("/")
def serve():
    return test.somethingjson()

@app.route("/lel")
def givehimlel():
    return "its lel!"


if __name__ == '__main__':
    app.run(debug=True, port=80)

