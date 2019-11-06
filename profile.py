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
    res=db.userAddress.find_one({"email":email})
    return render_template("profile.html",fname=fname,lname=lname,email=email,unum=res["unum"],bname=res["bname"],addr1=res["addr1"],addr2=res["addr2"],city=res["city"],pincode=res["pincode"])
@prof.route("/profile/edit/<email>")
def editProfile(email):
    db = client.logindb
    res = db.loggedin.find_one()
    email = res['user']
    db = client.userdb
    res = db.userDetails.find_one({"email":email})
    fname=res["fname"]
    lname=res["lname"]
    db=client.addressdb
    res=db.userAddress.find_one({"email":email})
    return render_template("EditProfile.html",fname=fname,lname=lname,email=email,unum=res["unum"],bname=res["bname"],addr1=res["addr1"],addr2=res["addr2"],city=res["city"],pincode=res["pincode"])