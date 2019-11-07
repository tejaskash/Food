from flask import render_template,request,Blueprint
from pymongo import MongoClient
pay = Blueprint("pay","pay")
client = MongoClient("mongodb://localhost:27017")

@pay.route("/pay",methods=["POST"])
def makePayment():
    email = request.form["email"]
    order = request.form["ord"]
    ccnum = request.form["ccnum"]
    ccname= request.form["ccname"]
    cccvv = request.form["cccvv"]
    exp = request.form["exp"]
    totCost = request.form["totCost"]
    db = client.paymentdb
    db.payments.insert_one({"email":email,"ccnum":ccnum,"ccname":ccname,"cccvv":cccvv,"exp":exp,"amount":totCost})
    return render_template("orderconf.html",email=email,order=eval(order),name=request.form["name"])