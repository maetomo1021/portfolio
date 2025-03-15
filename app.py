from flask import Flask,render_template,Blueprint,url_for,request,flash
from flask_login import LoginManager,login_required
from portfolio.models import db,bcrypt,User
from portfolio.blueprints.auth import auth_bp
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from portfolio.blueprints.header import header_bp
from portfolio.blueprints.footer import footer_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'maetomo1021'  # セッション用の秘密キー

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
app.register_blueprint(header_bp, url_prefix='/header')
app.register_blueprint(footer_bp, url_prefix='/footer')
app.register_blueprint(auth_bp)

# データベース作成
with app.app_context():
    db.create_all()

# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# LoginManager = LoginManager(app)
# LoginManager.login_view = "login"

# ##ユーザーモデル定義
# class User(db.Model,UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), nullable=False, unique=True)
#     password = db.Column(db.String(150), nullable=False)

# # ログインユーザーの読み込み
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

@app.route("/")
@login_required
def index():
    age = 29
    name = "Taro"
    return render_template("index.html",age = age,name =name)

@app.route("/login")
def login():
    return render_template("login.html")







if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 4940,debug=True)
