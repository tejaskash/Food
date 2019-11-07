from flask import Blueprint,request,render_template
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
adm = Blueprint("adm","adm",template_folder="./templatesadmin")

@adm.route("/admin/login")
def adminLogin():
    return render_template("adminlogin.html")

@adm.route("/admin/auth",methods=["GET","POST"])
def adminAuth():
    user = request.form['email']
    print(user)
    password = request.form['psw']
    print(password)
    db = client.admlogindb
    res = db.loginAuth.find_one({"user":user,"passw":password})
    print(res)
    if res["passw"] == password:
        db=client.admlogindb
        db.loggedin.insert_one({"user":user})
        return render_template("adminDashboard.html",email=user)
    else:
        return "<h1>Invalid Password</h1>"
    return "<h1>Hello</h1>"
@adm.route("/admin/add",methods=["POST"])
def adminAdd():
    email=request.form["email"]
    db = client.restdb
    res = db.rest.find({"email":email})
    return render_template("addRestaurant.html",email=email,data=res)
@adm.route("/admin/update",methods=["POST"])
def adminUpdate():
    email = request.form['email']
    name = request.form['name']
    desc = request.form['desc']
    address=request.form['address']
    itemCost = dict()
    for i in range(1,6):
        item = request.form["item"+str(i)]
        cost = request.form["cost"+str(i)]
        itemCost[item] = cost
    db = client.restdb
    db.rest.insert_one({"email":email,"name":name,"address":address,"desc":desc,"menuid":name})
    db = client.menudb
    db.menus.insert_one({"menuid":name,"Items":itemCost})
    return "<h1>Success</h1>"