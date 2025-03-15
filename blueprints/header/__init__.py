from flask import Blueprint
header_bp = Blueprint('header', __name__, template_folder='templates')
from . import routes  # ルートを読み込む
