from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from . import auth_bp
from portfolio.models import db, User
import re

import re
from flask import request, flash, redirect, url_for, render_template
from portfolio.models import User, db
from flask_login import login_user

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # SQLインジェクション対策はSQLAlchemyが自動で処理してるが、念のためチェック
        if any(sql_keyword in email.upper() for sql_keyword in ["SELECT", "INSERT", "DELETE", "DROP", "--"]):
            flash("不正な文字列が含まれています", "danger")
            return render_template('register.html')

        # メール形式の簡易バリデーション（type=email だけでなくPythonでも検証）
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("有効なメールアドレスを入力してください", "danger")
            return render_template('register.html')

        # 重複チェック
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("すでにそのユーザー名またはメールアドレスは登録されています", "danger")
            return render_template('register.html')

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("登録完了！ログインしてね", "success")
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
