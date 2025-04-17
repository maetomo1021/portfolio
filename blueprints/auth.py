from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

auth = Blueprint('auth', __name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            flash('ログイン成功')
            return redirect(url_for('views1.home'))  # 例：homeにリダイレクト
        else:
            flash('ログイン失敗')

    return render_template('login.html')
