from flask import Blueprint
footer_bp = Blueprint('footer', __name__, template_folder='templates')
from . import routes
