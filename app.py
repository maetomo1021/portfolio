from flask import Flask,render_template
from flask_login import LoginManager
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

@app.route("/")
def index():
    return render_template("index.html")


