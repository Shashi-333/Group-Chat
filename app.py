from flask import Flask
from flask import render_template,request


app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def initial():
    return render_template("index.html")

@app.route("/login", methods = ['POST'])
def login():
    if request.method == "POST":
        name = request.form.get('username')
        form = {
            "name": name
        }
        return render_template("chat.html",context = form)


if __name__ == "__main__":
    app.run(debug=True, host= "0.0.0.0", port = "5000" )