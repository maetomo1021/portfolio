from flask import Blueprint, render_template
from flask_login import login_required

header_bp = Blueprint("header", __name__, template_folder="templates")

@header_bp.route("/")
@login_required
def top():
    return render_template("index.html")
