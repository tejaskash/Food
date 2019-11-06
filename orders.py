from flask import Blueprint,render_template
from pymongo import MongoClient
order = Blueprint("order","order")
client = MongoClient("mongodb://localhost:27017")
@order.route('/order/<name>')
def displayPage(name):
    db = client.restdb
    res = db.rest.find_one({"name":name})
    print(res)
    return render_template("restaurant.html",name=name,data=res)
