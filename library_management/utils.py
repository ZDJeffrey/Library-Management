from library_management.models import *

def user_register(name, id_card, account, password)->bool:
    '''
    读者注册,返回是否注册成功
    '''
    # 读者类型默认为新人,信誉值默认为100
    next_id = Reader.query.order_by(Reader.reader_id.desc()).first().reader_id + 1
    reader = Reader(reader_id=next_id, type_name='新人', name=name, id_card=id_card, account=account, credit=100,
                    password_hash=password)
    db.session.add(reader)
    db.session.commit()
    return True
    pass

def book_join_publisher():
    '''
    书籍和出版社表外连接结果,返回字典列表,字典属性值为变量名,其中出版社属性只需要出版社名字
    '''
    ret = []
    # ret = Book.query.join(Publisher).all()
    ret = db.session.query(Book.book_id, Book.title, Book.author, Book.ISBN, Book.place, Book.state, Book.publisher_id,
                     Publisher.publisher_name).filter(Book.publisher_id == Publisher.publisher_id).order_by(Book.title).all()
    return ret
    # return []

def book_join_publisher_search_by(search_type, search_text):
    '''
    书籍和出版社表外连接结果,返回字典列表,字典属性值为变量名,其中出版社属性只需要出版社名字publisher_name
    search_type为搜索类型(id,title,author,ISBN,publisher),search_text为搜索内容
    '''
    if search_type == 'id':
        # ret = Book.query.filter(Book.book_id == search_text).join(
        #     Publisher, Book.publisher_id == Publisher.publisher_id).add_column(
        #     Publisher.publisher_name).order_by(Book.title).all()
        ret = db.session.query(Book.book_id, Book.title, Book.author, Book.ISBN, Book.place, Book.state, Book.publisher_id,
            Publisher.publisher_name).filter(Book.book_id == search_text).filter(
            Book.publisher_id == Publisher.publisher_id).order_by(Book.title).all()
    elif search_type == 'title':
        ret = db.session.query(Book.book_id, Book.title, Book.author, Book.ISBN, Book.place, Book.state, Book.publisher_id,
            Publisher.publisher_name).filter(Book.title == search_text).filter(
            Book.publisher_id == Publisher.publisher_id).order_by(Book.title).all()
    elif search_type == 'author':
        # ret = Book.query.filter(Book.author == search_text).join(
        #     Publisher, Book.publisher_id == Publisher.publisher_id).add_column(
        #     Publisher.publisher_name).order_by(Book.title).all()
        ret = db.session.query(Book.book_id, Book.title, Book.author, Book.ISBN, Book.place, Book.state, Book.publisher_id,
            Publisher.publisher_name).filter(Book.author == search_text).filter(
            Book.publisher_id == Publisher.publisher_id).order_by(Book.title).all()
    elif search_type == 'ISBN':
        # ret = Book.query.filter(Book.ISBN == search_text).join(
        #     Publisher, Book.publisher_id == Publisher.publisher_id).add_column(
        #     Publisher.publisher_name).order_by(Book.title).all()
        ret = db.session.query(Book.book_id, Book.title, Book.author, Book.ISBN, Book.place, Book.state, Book.publisher_id,
            Publisher.publisher_name).filter(Book.ISBN == search_text).filter(
            Book.publisher_id == Publisher.publisher_id).order_by(Book.title).all()
    elif search_type == 'publisher':
        # ret = Book.query.filter(Publisher.publisher_name == search_text).join(
        #     Publisher,Book.publisher_id == Publisher.publisher_id).add_column(
        #     Publisher.publisher_name).order_by(Book.title).all()
        ret = db.session.query(Book.book_id, Book.title, Book.author, Book.ISBN, Book.place, Book.state, Book.publisher_id,
            Publisher.publisher_name).filter(Publisher.publisher_name == search_text).filter(
            Book.publisher_id == Publisher.publisher_id).order_by(Book.title).all()
    else:
        ret = []
    return ret
    # return []

def edit_book(book_id, place)->bool:
    '''
    修改书籍信息,place为书籍所在书架位置,返回是否修改成功
    '''
    book = Book.query.filter(Book.book_id == book_id).first()
    book.place = place
    db.session.add(book)
    db.session.commit()
    return True


def books_to_return(reader_id):
    '''
    读者借阅的书籍,返回书籍列表(书籍ID、书名、借阅时间、剩余时间)
    [{book_id, title, date, day_left}]
    '''
    books = Borrow.query(Book.book_id, title, date, day_left).filter(Borrow.reader_id == reader_id).all()
    return books
    pass

def return_book_by_id(book_id)->bool:
    '''
    读者还书,返回是否还书成功
    '''
    # TODO：逾期惩罚
    查找书籍和借阅记录
    book = Book.query.filter(Book.book_id == book_id).first()
    borrow = Borrow.query.filter(Borrow.book_id == book_id).first()

    # 检验是否超期
    reader = Reader.query.filter(Reader.reader_id == borrow.reader_id).first()
    reader_type = ReaderType.query.filter(ReaderType.type_name == reader.type_name).first()
    if (datetime.date.today() - borrow.date).days > reader_type.day_limit:
        # 超期
        print('已逾期，请找管理员当面核销')
        # reader.credit -= 5
        return False

    # 修改书籍和借阅记录并提交
    book.state = False
    borrow.is_return = True
    db.session.add(book)
    db.session.add(borrow)
    if db.session.commit():
        return True
    else:
        return False
    pass

def borrow_book(book_id, reader_id)->bool:
    '''
    读者借书,返回是否借书成功
    '''
    # TODO：讨论具体信誉值
    检验读者是否有借书资格
    reader = Reader.query.filter(Reader.reader_id == reader_id).first()
    reader_type = ReaderType.query.filter(ReaderType.type_name == reader.type_name).first()
    # if reader.credit < 60: # 信誉值小于60则不能借书
        # return False

    # 检验读者是否超过借书数量限制
    borrow_count = Borrow.query.filter(Borrow.reader_id == reader_id).count()
    if borrow_count >= reader_type.book_limit:
        print('借书数量超过限制')
        return False

    # 检验书籍是否可借
    book = Book.query.filter(Book.book_id == book_id).first()
    if book.state == True: # 书籍已被借阅
        print('书籍已被借阅')
        return False

    # 修改书籍和借阅记录并提交
    book.state = True
    borrow = Borrow(book_id=book_id, reader_id=reader_id, date=datetime.date.today(), is_return=False)
    db.session.add(book)
    db.session.add(borrow)
    db.session.commit()
    return True


def user_borrow_history(reader_id):
    '''
    读者借书历史,返回书籍列表(书籍ID、书名、借阅时间、是否归还)
    [{book_id, title, date, is_return}]
    '''
    books = Borrow.query(Book.book_id, title, date, is_return).filter(Borrow.reader_id == reader_id).all()
    return books
    # return []

def add_publisher(publisher_name, publisher_address)->bool:
    '''
    添加出版社,返回是否添加成功
    '''
    new_publisher = Publisher(publisher_name=publisher_name, address=publisher_address)
    db.session.add(new_publisher)
    db.session.commit()
    return True


def add_stack(stack_name, stack_address, stack_open_time)->bool:
    '''
    添加书库,返回是否添加成功
    '''
    new_stack = Stack(stack_name=stack_name, location=stack_address, opening=stack_open_time)
    db.session.add(new_stack)
    db.session.commit()
    return True


def modify_reader(reader_id, type_name)->bool:
    '''
    修改读者类型,返回是否修改成功
    '''
    pass

def add_entering(title, book_id, ISBN, type_name, author, publisher_id, stack_id, place, staff_id)->bool:
    '''
    添加入库书籍,返回是否添加成功
    '''
    pass

def add_out(book_id, date, reason, staff_id)->bool:
    '''
    添加出库书籍,返回是否添加成功
    '''
    pass

def admin_modify_info(admin_id, account, password)->bool:
    '''
    修改管理员信息,返回是否修改成功
    id不修改
    password若为空则不修改
    '''
    pass

def staff_modify_info(staff_id, name, age, id_card, phone_number, address, account, password)->bool:
    '''
    修改员工信息,返回是否修改成功
    id不修改
    password若为空则不修改
    '''
    pass

def reader_modify_info(reader_id, name, id_card, account, password)->bool:
    '''
    修改读者信息,返回是否修改成功
    id不修改
    password若为空则不修改
    '''
    pass

def add_new_staff(account, password)->bool:
    '''
    添加新员工,返回是否添加成功
    '''
    pass