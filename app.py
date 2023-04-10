
from flask import Flask
from flask import render_template,request
from loginForm import *
from flask_sqlalchemy import SQLAlchemy,session
app = Flask(__name__)

#Config
app.secret_key = "sjjfdjg&jnsf#sndf"

#Db congfig
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Sasijana@333333@127.0.0.1:3306/groupchat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique =True, nullable = False)
    password = db.Column(db.String(25), unique =True, nullable = False)
    email = db.Column(db.String(25), unique =True, nullable = False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique =True, nullable = False)
    password = db.Column(db.String(25), unique =True, nullable = False)
    email = db.Column(db.String(25), unique =True, nullable = False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

@app.route("/", methods = ['GET','POST'])
def login():
    log = Loginvalidator()
    if log.validate_on_submit():
        return "Created"
    return render_template("index.html",form = log)

@app.route("/adduser", methods = ['POST'])
def addusers():
    return render_template("chat.html")


if __name__ == "__main__":
    app.run(debug=True, host= "0.0.0.0", port = "5000" )