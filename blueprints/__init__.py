 # Blueprint の初期化
from flask import Blueprint
# header_bp = Blueprint('header', __name__, template_folder='templates')
from .header import header_bp
from .footer import footer_bp
