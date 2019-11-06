from flask import Blueprint,render_template
from pymongo import MongoClient
prof = Blueprint('prof','prof')
client = MongoClient("mongodb://localhost:27017")
@prof.route("/profile")
def profilePage():
    db = client.logindb
    res = db.loggedin.find_one()
    email = res['user']
    db = client.userdb
    res = db.userDetails.find_one({"email":email})
    fname=res["fname"]
    lname=res["lname"]
    db=client.addressdb
    res=db.userAddress
    return render_template("profile.html",fname=fname,lname=lname,email=email)