from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from . import auth_bp
from portfolio.models import db, User

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # ユーザーがすでに存在しないか確認
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('このメールアドレスはすでに登録されています。', 'danger')
            return redirect(url_for('auth.register'))

        # 新しいユーザーを作成
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('登録に成功しました！ログインしてください。', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)  # ここでログイン
            flash('ログイン成功！', 'success')
            return redirect(url_for('index'))  # ホームページへリダイレクト
        else:
            flash('ログイン失敗。メールアドレスまたはパスワードが間違っています。', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()  # ログアウト
    flash('ログアウトしました。', 'info')
    return redirect(url_for('auth.login'))
