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
    if db.session.commit():
        return True
    else:
        return False
    pass

def book_join_publisher():
    '''
    书籍和出版社表外连接结果,返回字典列表,字典属性值为变量名,其中出版社属性只需要出版社名字
    '''
    ret = Book.query.all().join(Publisher, Book.publisher_id == Publisher.publisher_id).add_column(
        Publisher.publisher_name).order_by(Book.title).all()
    return ret
    # return []

def book_join_publisher_search_by(search_type, search_text):
    '''
    书籍和出版社表外连接结果,返回字典列表,字典属性值为变量名,其中出版社属性只需要出版社名字publisher_name
    search_type为搜索类型(id,title,author,ISBN,publisher),search_text为搜索内容
    '''
    if search_type == 'id':
        ret = Book.query.filter(Book.book_id == search_text).join(
            Publisher, Book.publisher_id == Publisher.publisher_id).add_column(
            Publisher.publisher_name).order_by(Book.title).all()
    elif search_type == 'title':
        ret = Book.query.filter(Book.title == search_text).join(
            Publisher, Book.publisher_id == Publisher.publisher_id).add_column(
            Publisher.publisher_name).order_by(Book.title).all()
    elif search_type == 'author':
        ret = Book.query.filter(Book.author == search_text).join(
            Publisher, Book.publisher_id == Publisher.publisher_id).add_column(
            Publisher.publisher_name).order_by(Book.title).all()
    elif search_type == 'ISBN':
        ret = Book.query.filter(Book.ISBN == search_text).join(
            Publisher, Book.publisher_id == Publisher.publisher_id).add_column(
            Publisher.publisher_name).order_by(Book.title).all()
    elif search_type == 'publisher':
        ret = Book.query.filter(Publisher.publisher_name == search_text).join(
            Publisher,Book.publisher_id == Publisher.publisher_id).add_column(
            Publisher.publisher_name).order_by(Book.title).all()
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
    if db.session.commit():
        return True
    else:
        return False
    pass

def books_to_return(reader_id):
    '''
    读者借阅的书籍,返回书籍列表(书籍ID、书名、借阅时间、剩余时间)
    [{book_id, title, date, day_left}]
    '''
    books = Borrow.query.filter(Borrow.reader_id == reader_id).filter().all()
    return []

def return_book_by_id(book_id)->bool:
    '''
    读者还书,返回是否还书成功
    '''
    pass

def borrow_book(book_id, reader_id)->bool:
    '''
    读者借书,返回是否借书成功
    '''
    pass

def user_borrow_history(reader_id):
    '''
    读者借书历史,返回书籍列表(书籍ID、书名、借阅时间、是否归还)
    [{book_id, title, date, is_return}]
    '''
    return []

def add_publisher(publisher_name, publisher_address)->bool:
    '''
    添加出版社,返回是否添加成功
    '''
    pass

def add_stack(stack_name, stack_address, stack_open_time)->bool:
    '''
    添加书库,返回是否添加成功
    '''
    pass

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