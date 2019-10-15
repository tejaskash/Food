from flask import Flask, redirect, url_for, session,render_template,request
from flask_dance.contrib.google import make_google_blueprint, google
from register import reg
from config import GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET,SECRET_KEY,DEBUG,jsondata,LOGGED_IN_USER_EMAIL
from pymongo import MongoClient
from flask_oauth import OAuth
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import URLError
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

google = oauth.remote_app('google',
                           base_url='https://www.google.com/accounts/',
                           authorize_url='https://accounts.google.com/o/oauth2/auth',
                           request_token_url=None,
                           request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email','response_type': 'code'},
                           access_token_url='https://accounts.google.com/o/oauth2/token',
                           access_token_method='POST',
                           access_token_params={'grant_type': 'authorization_code'},
                           consumer_key=GOOGLE_CLIENT_ID,
                           consumer_secret=GOOGLE_CLIENT_SECRET)
@app.route("/")
def mainPage():
    return render_template("hello.html")
@app.route("/loginPage" ,methods=['GET','POST'])
def loginPage():
    return render_template("login.html")
@app.route("/login/google",methods=['GET','POST'])
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))
    access_token = access_token[0]
    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',None, headers)
    try:
        res = urlopen(req)
    except URLError as e:
        if e.code == 401:
            session.pop('access_token',None)
            return redirect(url_for('login'))
        return res.read()
    data = res.read()
    data = data.decode('utf8')
    jsondata = json.loads(data)
    LOGGED_IN_USER_EMAIL = jsondata["email"]
    #TODO: ADD Code to Check if user in DB, if yes then redirect to Main Page, else redirect to register page
    return redirect(url_for("mainPage"))
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
    app.run("localhost",port=5000)