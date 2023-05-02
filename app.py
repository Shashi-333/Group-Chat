
from datetime import datetime
from flask import Flask, jsonify
from flask import render_template,request,flash,redirect,session
from sqlalchemy import and_
from loginForm import *
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from flask_socketio import SocketIO,emit,send
from flask_migrate import Migrate

app = Flask(__name__)

#Config
app.secret_key = "sjjfdjg&jnsf#sndf"

#Db congfig
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin1234567@localhost:3306/groupchat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)
migrate= Migrate(app, db)



#initialize Flask_socket.io
socketio = SocketIO(app, cors_allowed_origins="*")

users_list=['Sasikala','Jana']

groups={"group1":["Sasikala"]}

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique =True, nullable = False)
    password = db.Column(db.String(25), unique =True, nullable = False)
    email = db.Column(db.String(25), unique =True, nullable = False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, default=False)
    username = db.Column(db.String(25), unique =True, nullable = False)
    password = db.Column(db.String(25), unique =True, nullable = False)
    email = db.Column(db.String(25), unique =True, nullable = False)

    # def __init__(self, username, password, email):
    #     self.username = username
    #     self.password = password
    #     self.email = email
    def to_dict(self):
        return {'id': self.id, 'username': self.username,'password':self.password, 'email': self.email}

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(50), nullable=False)
    groupname = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'user': self.username,'groupname':self.groupname, 'message': self.message, 'timestamp': self.timestamp}

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupname = db.Column(db.String(50), unique =True, nullable=False)

    def __init__(self, groupname):
        self.groupname = groupname

class Groupmember(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(25), nullable = False)

    
    def __init__(self, groupname, username):
        self.groupname = groupname
        self.username = username

with app.app_context():
    db.create_all()

@app.route("/", methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        ad = admin.query.all()
        f = request.form
        form.username=f['username']
        form.password=f['password']
        form.email=f['email']
        session['username'] = f['username']
        l=[]
        for a in ad:
            l.append(a.username)
        if f['username'] == "Sasikala":
            if f['username'] == a.username and f['password'] == a.password :
                return render_template("admin.html")
            else:
                return "Invalid Password"
        
        else:
            us = db.session.query(user).filter(user.username == f['username']).first()
            if f['username'] == us.username and f['password'] == us.password :
                return redirect("/chatroom")
            else:
                return "Invalid Password"
    return render_template("login.html",form = form)

@app.route("/register",methods=['GET','POST'])
def register():
    # rform = RegisterForm()
    # if rform.validate_on_submit():
    if request.method == "POST":
        f=request.form
        new_user = f['username']
        users_list.append(new_user)
        us = user(username=f['username'], password=f['password'], email=f['email'])
        db.session.add(us)
        db.session.commit()
    return render_template('admin.html')

@app.route("/delusers", methods = ['POST'])
def delusers():
    if request.method == "POST":
        u=db.session.query(user).filter(user.username == request.form['username'] ).first()
        # u = user.query.filter_by(username = request.form['username'])
        if u:
            db.session.delete(u)
        db.session.commit()
    return render_template("admin.html")

@app.route("/chatroom", methods = ['GET', 'POST'])
def chatroom():
    return render_template('chatroom.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/create_group',methods = ['GET', 'POST'])
def create_group():
    grp = Group(groupname = request.args.get('groupname'))
    db.session.add(grp)
    db.session.commit()
    return render_template('chatroom.html')

@app.route('/addmember',methods = ['GET', 'POST'])
def addmember():
    data = db.session.query(Groupmember).filter(Groupmember.username == session['username']).all()
    u=[]
    for d in data:
        u.append(d.groupname)
    return render_template('addmember.html',groups=u)

@app.route('/addmembersgrp/<groupname>',methods = ['GET', 'POST'])
def addmember_add(groupname):
    grp=groupname
    userlist = db.session.query(Groupmember).filter(Groupmember.groupname == grp ).all()
    u=[]
    for use in userlist:
        u.append(use.username)
    data = db.session.query(user).filter(user.username.notin_(u)).all()
    l=[]
    for d in data:
        l.append(d.username)
    data={'list':l}
    print(jsonify(data))
    return jsonify(data)


@socketio.on('message')
def message(data):
    userlist = db.session.query(Groupmember).filter(Groupmember.groupname == session['groupname'] ).all()
    u=[]
    for user in userlist:
        u.append(user.username)
    if (session['username'] in u):
        message = Message(user=session['username'],groupname=session['groupname'], message=data['message'])
        db.session.add(message)
        db.session.commit()
        messages = Message.query.order_by(Message.timestamp.desc()).all()
        messages.reverse()
        for message in messages:
            emit('message', {'username': message.user, 'message': message.message})
    else:
        flash("Not allowed to message")

@socketio.on('grp_button')
def grp_message(data):
    session['groupname']=data['btn']
    userlist = db.session.query(Groupmember).filter(Groupmember.groupname == data['btn'] ).all()
    u=[]
    for user in userlist:
        u.append(user.username)
    messages = db.session.query(Message).order_by(Message.timestamp.desc()).filter(and_(Message.user.in_(u),Message.groupname == data['btn'])).limit(10).all()
    messages.reverse()
    for message in messages:
        emit('message', {'username': message.user, 'message': message.message, 'groupname': message.groupname, 'userlist':u})
    

@socketio.on('connect')
def handle_connect():
    grplst = db.session.query(Groupmember).filter(Groupmember.username == session['username']).all()
    for grp in grplst:
        socketio.emit('grp_button',{'grp':grp.groupname})



if __name__ == "__main__":
    socketio.run(app, debug=True)