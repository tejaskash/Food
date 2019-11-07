from flask import Blueprint,render_template,request
from pymongo import MongoClient
prof = Blueprint('prof','prof')
client = MongoClient("mongodb://localhost:27017")
@prof.route("/profile")
def profilePage():
    db = client.logindb
    res = db.loggedin.find_one()
    email = res['user']
    print(email)
    db = client.userdb
    res = db.userDetails.find_one({"email":email})
    print(res)
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
    db=client.logindb
    res=db.loginAuth.find_one({"user":email})
    passw=res["passw"]
    db=client.addressdb
    res=db.userAddress.find_one({"email":email})
    return render_template("EditProfile.html",fname=fname,lname=lname,email=email,unum=res["unum"],bname=res["bname"],addr1=res["addr1"],addr2=res["addr2"],city=res["city"],pincode=res["pincode"],password=passw)
@prof.route("/update/<email>",methods=['GET','POST'])
def updateProfile(email):
    db = client.addressdb
    db.userAddress.update_one({"email":email},{"$set":{"unum":request.form['unum']}})
    db.userAddress.update_one({"email":email},{"$set":{"bname":request.form['bname']}})
    db.userAddress.update_one({"email":email},{"$set":{"addr1":request.form['addr1']}})
    db.userAddress.update_one({"email":email},{"$set":{"addr2":request.form['addr2']}})
    db.userAddress.update_one({"email":email},{"$set":{"city":request.form['city']}})
    db.userAddress.update_one({"email":email},{"$set":{"pincode":request.form['pincode']}})
    db=client.addressdb
    db.loginAuth.update_one({"user":email},{"$set":{"passw":request.form['password']}})
    return "<h1>Success</h1>"
@prof.route("/profile/orders/<email>",methods=['GET','POST'])
def previousOrders(email):
    db = client.orderdb
    print(email)
    res = db.orders.find({"email":email})
    print("--RESULT--")
    if(res == None):
        return "<h1>No Previous Orders</h1>"
    result = list()
    for r in res:
        a = list()
        a.append(r["rest"])
        a.append(r["OrderItems"])
        a.append(r["timestamp"])
        result.append(a)
    print("--END--")
    return render_template("previous.html",data=result)