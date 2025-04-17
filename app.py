from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required
from portfolio.models import db, bcrypt, User
from portfolio.blueprints.auth import auth_bp
from portfolio.blueprints.header import header_bp
from portfolio.blueprints.footer import footer_bp
from dotenv import load_dotenv
import os

###APIキー読み込み###
from pathlib import Path
# env_path = Path()

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'maetomo1021'  # セッション用の秘密キー


# すでに定義済みの db と bcrypt を初期化
db.init_app(app)
bcrypt.init_app(app)

# Flask-Login のセットアップ
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"  # ログインが必要なページでリダイレクトする先

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Blueprint を登録
app.register_blueprint(auth_bp, url_prefix='/auth') 
app.register_blueprint(header_bp, url_prefix='/')
app.register_blueprint(footer_bp, url_prefix='/')


# app = Flask(__name__)
@app.route("/")
@login_required
def index():
    age = 29
    name = "Taro"
    return render_template("index.html", age=age, name=name)

@app.route("/search_root")
@login_required
def search_root():
    return render_template("search_root.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4940, debug=True)
