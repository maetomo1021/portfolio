from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from portfolio.models import User, db  # SQLAlchemyのUserモデルとdb
from portfolio.models import bcrypt  # ハッシュ化用

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # 既存ユーザー確認
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("そのユーザー名またはメールアドレスはすでに使われています")
            return render_template('register.html')

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("登録完了！ログインしてね")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("ログイン成功！")
            return redirect(url_for('header.top'))  # 任意のページに飛ばしてOK
        else:
            flash("ユーザー名またはパスワードが間違っています")

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash("ログアウトしました")
    return redirect(url_for('auth.login'))
