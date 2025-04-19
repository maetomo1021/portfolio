from flask import Flask,render_template,redirect,url_for
from flask_login import LoginManager,login_required,current_user
from portfolio.models import db, bcrypt, User
from portfolio.blueprints.auth import auth_bp
from portfolio.blueprints.header.routes import header_bp
from portfolio.blueprints.footer.routes import footer_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"

# DBやbcryptの初期化
db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(header_bp)
app.register_blueprint(footer_bp)

@app.route("/", methods=["GET"])
def start_page():
    if current_user.is_authenticated:
        return redirect(url_for('header.index'))  # ✅ 正しいendpoint名
    else:
        return redirect(url_for('auth.login'))  # 未ログインならログインページへ

@app.route("/search_root")
def search_root():
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    return render_template("search_root.html", api_key=api_key)



@login_required
@login_manager.unauthorized_handler
def index():
    return render_template("index.html")