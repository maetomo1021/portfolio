from flask import Flask,render_template,Blueprint
from portfolio.blueprints.header import header_bp
from portfolio.blueprints.footer import footer_bp
from flask_login import login_required

app = Flask(__name__)
# Blueprint を登録
app.register_blueprint(header_bp, url_prefix='/header')
app.register_blueprint(footer_bp, url_prefix='/footer')

@app.route("/")
def index():
    age = 29
    name = "Taro"
    return render_template("index.html",age = age,name =name)

@app.route("/login")
def login():
    return render_template("login.html")







if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 4940,debug=True)
