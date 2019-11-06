from flask import Flask, redirect, url_for, session,render_template,request
from register import reg
from config import LOGGED_IN_USER_EMAIL
from pymongo import MongoClient
import json
import os

client = MongoClient("mongodb://localhost:27017")

app = Flask(__name__)
app.register_blueprint(reg)

@app.errorhandler(405)
def error405(code):
    print(code)
    return "<h1>Ooops!!, How did you get here??"
@app.route("/")
def mainPage():
    return render_template("login.html")
@app.route("/login/auth",methods=['POST'])
def loginAuth():
    user = request.form['email']
    print(user)
    password = request.form['psw']
    print(password)
    db = client.logindb
    res=db.loginAuth.find_one({"user":user,"passw":password})
    print(res)
    if res == None:
        return "<h1>Invalid Password</h1>"
    elif res["passw"] == password:
        db.loggedin.insert_one({"user":user})
        return render_template("dashboard.html")
    else:
        return "<h1>Invalid Password</h1>"
    return "<h1>Hello</h1>"
@app.route("/logout")
def logout():
    db = client.logindb
    res=db.loggedin.find_one()
    if(res!=None):
        db.loggedin.delete_one(res)
        return render_template("login.html")
    else:
        return "<h1>Not Logged In</h1>"

if __name__ == "__main__":
    app.run("localhost",port=5000,threaded=True,debug=True)
