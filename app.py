from flask import Flask, redirect, url_for, session,render_template,request
from register import reg
from config import LOGGED_IN_USER_EMAIL
from pymongo import MongoClient
import json
import os

client = MongoClient("mongodb+srv://tejas:1234@pocketsdb-i09wt.mongodb.net/test?retryWrites=true&w=majority")

app = Flask(__name__)
app.register_blueprint(reg)

@app.errorhandler(405)
def error405(code):
    print(code)
    return "<h1>Ooops!!, How did you get here??"
@app.route("/")
def mainPage():
    return render_template("dashboard.html")
@app.route("/loginPage" ,methods=['GET','POST'])
def loginPage():
    return render_template("login.html")
@app.route("/login/auth",methods=['POST'])
def loginAuth():
    user = request.form['user']
    password = request.form['password']
    db = client.logindb
    res = db.loginAuth.find_one({""+user+"":""+password+""})
    print(res)
    if res == None:
        return "<h1>Invalid Password</h1>"
    elif res[user] == password:
        return redirect(url_for("mainPage"))
    else:
        return "<h1>Invalid Password</h1>"
    return "<h1>Hello</h1>"
    
if __name__ == "__main__":
    app.run("localhost",port=5000,threaded=True)
