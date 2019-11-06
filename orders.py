from flask import Blueprint,render_template,request
from datetime import datetime
from pymongo import MongoClient
order = Blueprint("order","order")
client = MongoClient("mongodb://localhost:27017")
@order.route('/order/<name>')
def displayPage(name):
    db = client.restdb
    res = db.rest.find_one({"name":name})
    print(res)
    menuid=res["menuid"]
    db = client.menudb
    menu=db.menus.find_one({"menuid":menuid})
    itemList = menu["Items"]
    print(itemList)
    return render_template("restaurant.html",name=name,data=res,menu=itemList)
@order.route("/order/confirm/<name>")
def placeOrder(name):
    req = dict(request.args)
    keys = req.keys()
    order = dict()
    for k in keys:
        if k.split(".")[0] == "Item":
            order[k.split(".")[1]]=req["Qty."+k.split(".")[1]]
    print(order)
    db = client.logindb
    email = db.loggedin.find_one()["user"]
    db = client.orderdb
    db.orders.insert_one({"email":email,"OrderItems":order,"timestamp":datetime.now()})
    return render_template("payment.html",order=order,email=email)