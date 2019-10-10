from flask import Flask, redirect, url_for, session,render_template
from flask_oauth import OAuth
GOOGLE_CLIENT_ID = '55535937800-37l6lks9feaueodu64a2svi34ei0ujq7.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '0OpJ3vyFesZ-jtC-TEPiLmbM'
REDIRECT_URI = '/ouath2callback'
SECRET_KEY = 'tejas'
DEBUG = True
import os
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = "55535937800-37l6lks9feaueodu64a2svi34ei0ujq7.apps.googleusercontent.com"
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = "0OpJ3vyFesZ-jtC-TEPiLmbM"
google_bp = make_google_blueprint(scope=["email"])
app.register_blueprint(google_bp, url_prefix="/login")

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
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))
    access_token = access_token[0]
    from urllib.request import Request
    from urllib.request import urlopen
    from urllib.error import URLError
    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',None, headers)
    try:
        res = urlopen(req)
    except URLError as e:
        if e.code == 401:
            session.pop('access_token',None)
            return redirect(url_for('login'))
        return res.read()
    return res.read()
@app.route("/login")
def login():
    callback = url_for('authorized', _external = True)
    return google.authorize(callback=callback)
@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token,''
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run("localhost",port=5000)