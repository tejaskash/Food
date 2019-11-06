@app.route("/Menu_Items")
def Menu_Items():
    db = client.Pockets

    rid="2001"

    res= db.Menu.find({"RID":rid}, {"_id":0,"Item Name":1, "Catergory":1, "Price":1})
    print(res)
    return render_template("Menu_Items.html",data=res)