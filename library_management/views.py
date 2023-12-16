from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from library_management import app, db
from library_management.models import Admin, Staff, Reader, ReaderType

# 主页
@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')

# 登录界面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 获取表单数据
        account = request.form['account']
        password = request.form['password']
        user_type = request.form['user_type']
        # 验证数据
        if not account or not password or not user_type:
            flash('Invalid input.')
            return redirect(url_for('login'))
        if user_type == 'admin':
            user = Admin.query.filter_by(account=account).first()
        elif user_type == 'staff':
            user = Staff.query.filter_by(account=account).first()
        elif user_type == 'reader':
            user = Reader.query.filter_by(account=account).first()
        else:
            flash('Invalid user type.')
            return redirect(url_for('login'))
        if not user:
            flash('Invalid account.')
            return redirect(url_for('login'))
        if not user.validate_password(password):
            flash('Invalid password.')
            return redirect(url_for('login'))
        # 登录用户
        if user_type == 'admin':
            login_user(user)
        elif user_type == 'staff':
            login_user(user)
        elif user_type == 'reader':
            login_user(user)
        flash('Login success.')
        return redirect(url_for('index'))
    return render_template('login.html')

# 登出
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))

    