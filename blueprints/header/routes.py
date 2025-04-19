from flask import Blueprint, render_template
from flask_login import login_required
import os

header_bp = Blueprint('header', __name__, template_folder='templates')

@header_bp.route('/index')
@login_required
def index():
    return render_template('index.html')

@header_bp.route('/searchroot')
@login_required
def search_root():
    return render_template('searchroot.html')  # ファイル名に合わせて！
