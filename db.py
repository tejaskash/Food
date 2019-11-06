# Defining Constants
from datetime import datetime
conn_str=""
client = MongoClient(conn_str)
my_db=client.UserDB

#End of constants

#Code For Order

Ord_Date=datetime.now()

RID=0

UID=0

Order_Items[]={}

OID=my_db.Orders.find().sort({OID:-1}).limit(1)+1

my_db.Orders.insert_one({"OID":OID, "RID":RID, "UID":UID,"Date":Ord_Date})

for i in Order_Items:
    total=i.quantity*i.cost
    my_db.Order_Items.insert_one({"OID":OID,"IID":i.iid,"Quantity":i.quantity,"Cost_Per_Item":i.cost,"Total":total})

client.close()



# Code for Menu

#insert

IID=my_db.Menu.find().sort({IID:-1}).limit(1)+1
RID=0
Item_Name=str(request.form['item_name'])
Category[]=request.form.getlist('category')
Price=int(request.form['price'])

my_db.Menu.insert_one({"IID":IID,"RID":RID, "Item_Name":Item_Name, "Category":Category, "Price":Price})

#update
IID=0
Item_Name=str(request.form['item_name'])
Category[]=request.form.getlist('category')
Price=int(request.form['price'])

my_db.Menu.update({"IID":IID},{$set:{"Item_Name":Item_Name, "Category":Category, "Price":Price}})


#delete
IID=0
 my_db.Menu.deleteOne({"IID":IID})























