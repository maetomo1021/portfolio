from flask import render_template
from . import footer_bp

@footer_bp.route('/footer')
def footer():
    return render_template('footer.html')
