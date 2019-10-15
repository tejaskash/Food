from flask import Blueprint

reg = Blueprint('register',__name__,template_folder='templates')

@reg.route("/register",methods=['POST'])
def regr():
    return "<h1>Registration Page</h1>"