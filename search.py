from flask import Blueprint,render_template

ser = Blueprint("ser","ser")

@ser.route("/search")
def SearchPage():
    return render_template("search.html")