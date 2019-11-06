from flask import Blueprint,render_template

order = Blueprint("order","order")

@order.route('/order/<name>')
def displayPage(name):
    return "<h3>"+name+"<h3>"