
from datetime import datetime
from flask import Flask
from flask import render_template,request,flash,redirect,session
from loginForm import *
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from flask_socketio import SocketIO,emit,send


app = Flask(__name__)

#Config
app.secret_key = "sjjfdjg&jnsf#sndf"

#Db congfig
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin1234567@localhost:3306/groupchat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)


#initialize Flask_socket.io
socketio = SocketIO(app, cors_allowed_origins="*")

users_list=['Sasikala','Jana']

groups={"gorup1":["Sasikala"]}

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

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'user': self.username, 'message': self.message, 'timestamp': self.timestamp}

with app.app_context():
    db.create_all()

@app.route("/", methods = ['GET','POST'])
def login():
    log = LoginForm()
    if log.validate_on_submit():
        ad = admin.query.all()
        us = user.query.all()
        f = request.form
        session['username'] = f['username']
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
                return redirect("/chatroom")
            else:
                return "Invalid Password"
    return render_template("login.html",form = log)

@app.route("/register",methods=['GET','POST'])
def register():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        if request.method == "POST":
            new_user = request.form['username']
            if new_user not in users_list:
                users_list.append(new_user)
                us = user(username=request.form['username'],password=request.form['password'],email=request.form['email'])
                db.session.add(us)
                db.session.commit()
            else:
                flash("User Already exist")
        return render_template('admin.html',form = reg_form)

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

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/create_group')
def create_group():
    
    return redirect('/login')

@socketio.on('message')
def message(data):
    print(session['username'])
    print(data)
    message = Message(user=session['username'], message=data['message'])
    db.session.add(message)
    db.session.commit()
    # socketio.emit('message', {'username : session['username'], message=data['message']})
    messages = Message.query.order_by(Message.timestamp.desc()).limit(10).all()
    messages.reverse()
    for message in messages:
        emit('message', {'username': message.user, 'message': message.message})

@socketio.on('connect')
def handle_connect():
    messages = Message.query.order_by(Message.timestamp.desc()).limit(10).all()
    messages.reverse()
    for message in messages:
        emit('message', {'username': message.user, 'message': message.message})

if __name__ == "__main__":
    socketio.run(app, debug=True)