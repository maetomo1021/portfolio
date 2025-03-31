from flask import Blueprint, render_template, redirect, url_for, request, flash
from portfolio.models import db, User, bcrypt
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint("auth", __name__)  # Blueprint の名前を指定

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("そのメールアドレスは既に使用されています", "danger")
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("登録完了！ログインしてください", "success")
            return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # ユーザー情報をデータベースから取得
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):  # パスワードが正しいか確認
            login_user(user)
            flash('ログイン成功', 'success')
            return redirect(url_for('index'))  # ホーム画面へ
        else:
            flash('メールアドレスまたはパスワードが間違っています', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました', 'info')
    return redirect(url_for('auth.login'))  # ログインページへ戻る
