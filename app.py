from flask import Flask,render_template
import os

app = Flask(__name__)

@app.route("/")
def helloworld():
    age = 29
    name = "Taro"
    return render_template("index.html",age = age,name =name)

@app.route("/login")
def login():
    return render_template("login.html")







if __name__ == "__main__":
    app.run()
