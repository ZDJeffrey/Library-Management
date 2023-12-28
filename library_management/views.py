from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from library_management import app, db
from library_management.models import *
from library_management.utils import *

# 主页：显示所有书籍或根据书名搜索书籍
@app.route('/', methods=['GET', 'POST'])
def index():
    if isinstance(current_user, Admin):
        staffs = Staff.query.all()
        return render_template('index.html', staffs=staffs)
    if request.method=='POST':
        search_type = request.form['search_type']
        search_text = request.form['search_text']
        print(search_type, search_text)
        books = book_join_publisher_search_by(search_type, search_text)
        return render_template('index.html', books=books, search_type=search_type, search_text=search_text)
    books = book_join_publisher()
    return render_template('index.html', books=books)


# 登录界面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 获取表单数据
        account = request.form['account']
        password = request.form['password']
        login_type = request.form['login_type']
        # 验证数据
        if not account or not password or not login_type:
            flash('Invalid input.')
            return redirect(url_for('login'))
        if login_type == 'admin':
            user = Admin.query.filter_by(account=account).first()
        elif login_type == 'staff':
            user = Staff.query.filter_by(account=account).first()
        elif login_type == 'reader':
            user = Reader.query.filter_by(account=account).first()
        else:
            flash('Invalid user type.')
            return render_template('login.html', account=account, password=password)
        if not user:
            flash('Invalid account.')
            return render_template('login.html',login_type=login_type)
        if not user.validate_password(password):
            flash('Invalid password.')
            return render_template('login.html', login_type=login_type, account=account)
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
@app.route('/info', methods=['GET', 'POST'])
@login_required
def account_info():
    if isinstance(current_user, Admin):
        if request.method == 'POST':
            admin_id = current_user.admin_id
            account = request.form['account']
            password = request.form['password']
            if admin_modify_info(admin_id, account, password):
                flash('修改成功')
                logout_user()
                login_user(Admin.query.get(admin_id))
            else:
                flash('修改失败')
                return render_template('info.html', password=password)
    elif isinstance(current_user, Staff):
        if request.method == 'POST':
            name = request.form['name']
            age = request.form['age']
            id_card = request.form['id_card']
            phone_number = request.form['phone_number']
            address = request.form['address']
            account = request.form['account']
            password = request.form['password']
            if staff_modify_info(current_user.staff_id, name, age, id_card, phone_number, address, account, password):
                flash('修改成功')
            else:
                flash('修改失败')
                return render_template('info.html', password=password)
    elif isinstance(current_user, Reader):
        if request.method == 'POST':
            name = request.form['name']
            id_card = request.form['id_card']
            account = request.form['account']
            password = request.form['password']
            if reader_modify_info(current_user.reader_id, name, id_card, account, password):
                flash('修改成功')
            else:
                flash('修改失败')
        reader_type = ReaderType.query.get(current_user.type_name)
        return render_template('info.html', reader_type=reader_type)
    return render_template('info.html')


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
        if user_register(name,id_card,account,password):
            flash('Sign up success.')
            return redirect(url_for('login'))
        else:
            flash('Account already exists.')
            return render_template('register.html', name=name, id_card=id_card, account=account, password=password)
    return render_template('register.html')


# 书籍详情页：读者借书、图书出入库信息
@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book_detail(book_id):
    if request.method == 'POST':
        submit = request.form['submit']
        if submit =='modify' and isinstance(current_user, Staff):
            place = request.form['place']
            if edit_book(book_id, place):
                flash('修改成功')
            else:
                flash('修改失败')
        elif submit == 'borrow' and isinstance(current_user, Reader):
            if borrow_book(book_id, current_user.reader_id):
                flash('借书成功')
            else:
                flash('借书失败')
 
    if isinstance(current_user, Admin):
        return redirect(url_for('index'))
    book = Book.query.get_or_404(book_id)
    stack = Stack.query.get(book.stack_id)
    book.stack_name = stack.stack_name
    if isinstance(current_user, Staff):
        borrows = Borrow.query.filter_by(book_id=book_id).all()
        enters = BookEntering.query.filter_by(book_id=book_id).all()
        outs = BookOut.query.filter_by(book_id=book_id).all()
        return render_template('book_detail.html', book=book, borrows=borrows,enters=enters,outs=outs)
    return render_template('book_detail.html', book=book)


# 读者还书界面
@app.route('/return_book', methods=['GET'])
@login_required
def return_books_list():
    if not isinstance(current_user, Reader):
        return redirect(url_for('index'))
    borrows = books_to_return(current_user.reader_id)
    return render_template('return_book.html', borrows=borrows)


@app.route('/return_book/<int:book_id>', methods=['GET'])
@login_required
def return_book(book_id):
    if not isinstance(current_user, Reader):
        return redirect(url_for('index'))
    if return_book_by_id(book_id):
        flash('还书成功')
    else:
        flash('还书失败')
    return redirect(url_for('return_books_list'))


# 读者历史借阅记录界面
@app.route('/borrow_history', methods=['GET'])
@login_required
def borrow_history():
    if not isinstance(current_user, Reader):
        return redirect(url_for('index'))
    borrows = user_borrow_history(current_user.reader_id)
    return render_template('borrow_history.html', borrows=borrows)


# 职工入库图书界面
@app.route('/enter', methods=['GET'])
@login_required
def book_enter():
    if not isinstance(current_user, Staff):
        return redirect(url_for('index'))
    enters = BookEntering.query.all()
    return render_template('enter.html', enters=enters)

@app.route('/enter/add', methods=['GET', 'POST'])
@login_required
def book_enter_add():
    if not isinstance(current_user, Staff):
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form['title']
        book_id = request.form['book_id']
        ISBN = request.form['ISBN']
        type_name = request.form['type_name']
        author = request.form['author']
        publisher_id = request.form['publisher_id']
        stack_id = request.form['stack_id']
        place = request.form['place']
        reason = request.form['reason']
        if add_entering(title, book_id, ISBN, type_name, author, publisher_id, stack_id, place, reason, staff_id=current_user.staff_id):
            flash('添加成功')
            return redirect(url_for('book_enter'))
        else:
            flash('添加失败')
            publishers = Publisher.query.all()
            stacks = Stack.query.all()
            return render_template('enter_add.html', publishers=publishers, stacks=stacks, title=title, book_id=book_id, ISBN=ISBN, type_name=type_name, author=author, publisher_id=publisher_id, stack_id=stack_id, place=place, reason=reason)
    publishers = Publisher.query.all()
    stacks = Stack.query.all()
    return render_template('enter_add.html', publishers=publishers, stacks=stacks)


# 职工出库图书界面
@app.route('/out', methods=['GET'])
@login_required
def book_out():
    if not isinstance(current_user, Staff):
        return redirect(url_for('index'))
    outs = BookOut.query.all()
    return render_template('out.html', outs=outs)

@app.route('/out/add', methods=['GET', 'POST'])
@login_required
def book_out_add():
    if not isinstance(current_user, Staff):
        return redirect(url_for('index'))
    if request.method == 'POST':
        book_id = request.form['book_id']
        date = request.form['date']
        reason = request.form['reason']
        if add_out(book_id, date, reason, staff_id=current_user.staff_id):
            flash('添加成功')
            return redirect(url_for('book_out'))
        else:
            flash('添加失败')
            return render_template('out_add.html', book_id=book_id, date=date, reason=reason)
    return render_template('out_add.html')


# 出版社信息界面
@app.route('/publisher', methods=['GET', 'POST'])
@login_required
def publisher_msg():
    if isinstance(current_user, Admin):
        return redirect(url_for('index'))
    if request.method == 'POST' and isinstance(current_user, Staff):
        publisher_name = request.form['publisher_name']
        publisher_address = request.form['publisher_address']
        if add_publisher(publisher_name, publisher_address):
            flash('添加成功')
            return redirect(url_for('publisher_msg'))
        else:
            flash('添加失败')
            publishers = Publisher.query.all()
            return render_template('publisher.html', publishers=publishers, publisher_name=publisher_name, publisher_address=publisher_address)
    publishers = Publisher.query.all()
    return render_template('publisher.html', publishers=publishers)


# 书库信息界面
@app.route('/stack', methods=['GET', 'POST'])
@login_required
def book_stack_msg():
    if isinstance(current_user, Admin):
        return redirect(url_for('index'))
    if request.method == 'POST' and isinstance(current_user, Staff):
        stack_name = request.form['stack_name']
        stack_address = request.form['stack_address']
        stack_open_time = request.form['stack_open_time']
        if add_stack(stack_name, stack_address, stack_open_time):
            flash('添加成功')
            return redirect(url_for('book_stack_msg'))
        else:
            flash('添加失败')
            stacks = Stack.query.all()
            return render_template('stack.html', stacks=stacks, stack_name=stack_name, stack_address=stack_address, stack_open_time=stack_open_time)


    stacks = Stack.query.all()
    return render_template('stack.html', stacks=stacks)


# 读者信息管理界面
@app.route('/reader', methods=['GET'])
@login_required
def reader_msg():
    if not isinstance(current_user, Staff):
        return redirect(url_for('index'))
    readers = Reader.query.all()
    return render_template('reader.html', readers=readers)

@app.route('/reader/<int:reader_id>', methods=['GET', 'POST'])
@login_required
def reader_modify(reader_id):
    if not isinstance(current_user, Staff):
        return redirect(url_for('index'))
    reader = Reader.query.get_or_404(reader_id)
    if request.method == 'POST':
        type_name = request.form['type_name']
        if modify_reader(reader_id, type_name):
            flash('修改成功')
        else:
            flash('修改失败')
    borrows = user_borrow_history(reader_id)
    reader_types = ReaderType.query.all()
    return render_template('reader_modify.html', reader=reader, borrows=borrows, reader_types=reader_types)

# 新建职工
@app.route('/add_staff', methods=['GET', 'POST'])
@login_required
def add_staff():
    if not isinstance(current_user, Admin):
        return redirect(url_for('index'))
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        if add_new_staff(account, password):
            flash('添加成功')
            return redirect(url_for('index'))
        else:
            flash('添加失败')
            return render_template('add_staff.html', account=account, password=password)
    return render_template('add_staff.html')



    