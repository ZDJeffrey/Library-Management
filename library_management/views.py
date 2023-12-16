from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from library_management import app, db
from library_management.models import *

# 主页：显示所有书籍或根据书名搜索书籍
@app.route('/', methods=['GET'])
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

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

# 账号信息界面
@app.route('/info', methods=['GET'])
@login_required
def account_info():
    if isinstance(current_user, Admin):
        return 'Admin'
    elif isinstance(current_user, Staff):
        return 'Staff'
    elif isinstance(current_user, Reader):
        return 'Reader'

# 账号信息修改界面



# 读者注册界面
@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        id_card = request.form['id_card']
        account = request.form['account']
        password = request.form['password']
        # 检查account是否存在
        exist_accounts = Reader.query.filter_by(account=account).first()
        if exist_accounts:
            flash('Account already exists.')
            return redirect(url_for('register'))
        type_name = '新人'
        credit = 100
        reader = Reader(name=name,id_card=id_card,account=account,type_name=type_name,credit=credit)
        reader.set_password(password)
        db.session.add(reader)
        db.session.commit()
        flash('Sign up success.')
        return redirect(url_for('login'))
    return render_template('register.html')


# 书籍详情页：读者借书、职工出库、职工入库新图书



# 读者还书界面



# 职工入库图书界面




# 职工管理读者信息界面




    