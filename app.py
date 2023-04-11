
from flask import Flask
from flask import render_template,request
from loginForm import *
from flask_sqlalchemy import SQLAlchemy,session
from passlib.hash import pbkdf2_sha256
from flask_socketio import SocketIO, send


app = Flask(__name__)

#Config
app.secret_key = "sjjfdjg&jnsf#sndf"

#Db congfig
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin1234567@localhost:3306/groupchat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

#initialize Flask_socket.io
socket = SocketIO(app)

users_list=['Sasikala','Jana']

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique =True, nullable = False)
    password = db.Column(db.String(25), unique =True, nullable = False)
    email = db.Column(db.String(25), unique =True, nullable = False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

class user(db.Model):
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
        ad = admin.query.all()
        us = user.query.all()
        f = request.form
        l=[]
        for a in ad:
            l.append(a.username)
        for u in us:
            continue
        if f['username'] == "Sasikala":
            if f['username'] == a.username and f['password'] == a.password :
                return render_template("admin.html")
            else:
                return "Invalid Password"
        
        elif request.form['username'] not in l:
            if f['username'] == u.username and f['password'] == u.password :
                return render_template("chatroom.html")
            else:
                return "Invalid Password"
            #uobj = user.query.filter_by(username == f['username'])
            # uobj.password =  f['password']
            # uobj.email = f['email']
            # db.session.commit(uobj)
    return render_template("login.html",form = log)

@app.route("/addusers", methods = ['POST'])
def addusers():
    if request.method == "POST":
        us = request.form['addusers']
        print(users_list)
        users_list.append(us)
        print(users_list)
    return render_template("admin.html")
@app.route("/delusers", methods = ['POST'])
def delusers():
    if request.method == "POST":
        if request.form['delusers'] in users_list:
            users_list.remove(request.form['delusers'])
            # u = user.query.filter_by(username = request.form['delusers']).delete()
            # u.commit()

    return render_template("admin.html")

@app.route("/chatroom", methods = ['GET', 'POST'])
def chatroom():
    return render_template('chatroom.html')

@socket.on('message')
def message(data):
    #print(data)

    send(data)


if __name__ == "__main__":
    socket.run(app, debug=True)