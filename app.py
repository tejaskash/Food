from flask import Flask, redirect, url_for, session,render_template,request
from register import reg
from config import LOGGED_IN_USER_EMAIL
from pymongo import MongoClient
import json
import os

client = MongoClient('localhost',27017)

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
app.secret_key = SECRET_KEY
app.config["GOOGLE_OAUTH_CLIENT_ID"] = GOOGLE_CLIENT_ID
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = GOOGLE_CLIENT_SECRET
google_bp = make_google_blueprint(scope=["email"])
app.register_blueprint(google_bp, url_prefix="/login")
app.register_blueprint(reg)
oauth = OAuth()


@app.errorhandler(405)
def error405(code):
    print(code)
    return "<h1>Ooops!!, How did you get here??"
@app.route("/")
def mainPage():
    return render_template("hello.html")
@app.route("/loginPage" ,methods=['GET','POST'])
def loginPage():
    return render_template("login.html")
@app.route("/login")
def login():
    callback = url_for('authorized', _external = True)
    return google.authorize(callback=callback)
@app.route("/ouath2callback")
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token,''
    return redirect(url_for('index'))

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
    app.run("localhost",port=5000,ssl_context=('cert.pem','key.pem'),threaded=True)
