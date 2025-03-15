from flask import render_template
from . import header_bp

@header_bp.route('/header')
def header():
    return render_template('header.html')
