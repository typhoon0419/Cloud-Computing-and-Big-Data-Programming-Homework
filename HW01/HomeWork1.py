from flask import Flask,render_template,request
from gevent import pywsgi
import numpy as np
app = Flask(__name__)

@app.route('/')
def start():
    return render_template("main.html")

@app.route('/account', methods = ["post"])
def firstQ():
    return render_template("01_account/account.html")

@app.route("/account/submit", methods = ["post"])
def account(): # The function is to submit the user and password
    username = request.values["username"]
    password = request.values["password"]
    if username == "MinShuang" and password == "711083104":
        return "尼蒿 " + username
    else:
        return "WHO! ARE! YOU!"

@app.route('/input', methods = ["post"])
def secondQ():
    return render_template("02_input/input.html")

@app.route('/input/result', methods = ["post"])
def input():
    whatever = request.values["whatever"]
    return render_template("02_input/input.html", **locals())


@app.route('/math', methods = ["post"])
def thirdQ():
    return render_template("03_math/math.html")

@app.route('/math/result', methods = ["post"])
def calculate():
    nums = request.values["nums"]
    x = np.fromstring(nums, dtype=int,sep=' ')
    maxNum = x.max()
    minNum = x.min()
    meanNum = x.mean()
    SDNum = x.std()
    return render_template("03_math/math.html", **locals())


if __name__ == '__main__':

    WEB_SERVER_HOST = '0.0.0.0'
    WEB_SERVER_PORT = 5000

    server = pywsgi.WSGIServer((WEB_SERVER_HOST, WEB_SERVER_PORT), app)
    server.serve_forever()