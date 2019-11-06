@app.route("/MyOrders")
def MyOrders():
    db = client.Pockets

    email="isha@pockets.com"

    res=db.Order.find({"email":email},{"_id":0, "OrderItems":1, "Restaurant":1, "timestamp":1,"Total":1})
    return render_template("MyOrders.html",data=res) 

