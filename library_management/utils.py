from library_management.models import *
from sqlalchemy import and_
import datetime


def user_register(name, id_card, account, password) -> bool:
    """
    读者注册,返回是否注册成功
    """
    # 验证身份证是否已经注册
    if Reader.query.filter(Reader.id_card == id_card).first():
        return False
    # 验证账号是否已经注册
    if Reader.query.filter(Reader.account == account).first():
        return False
    # 读者类型默认为新人,信誉值默认为100
    next_id = Reader.query.order_by(Reader.reader_id.desc()).first().reader_id + 1
    reader = Reader(
        reader_id=next_id,
        type_name="初级",
        name=name,
        id_card=id_card,
        account=account,
        credit=100,
    )
    reader.set_password(password)
    db.session.add(reader)
    db.session.commit()
    return True
    pass


def book_join_publisher():
    """
    书籍和出版社表外连接结果,返回字典列表,字典属性值为变量名,其中出版社属性只需要出版社名字
    """
    # todo: 还要按变量名排序吗
    ret = (
        db.session.query(
            Book.book_id.label("book_id"),
            Book.title.label("title"),
            Book.author.label("author"),
            Book.ISBN.label("ISBN"),
            Book.place.label("place"),
            Book.state.label("state"),
        )
        .join(Publisher)
        .add_column(Publisher.publisher_name)
        .order_by(Book.book_id)
        .all()
    )
    return ret
    # return []


def book_join_publisher_search_by(search_type, search_text):
    """
    书籍和出版社表外连接结果,返回字典列表,字典属性值为变量名,其中出版社属性只需要出版社名字publisher_name
    search_type为搜索类型(id,title,author,ISBN,publisher),search_text为搜索内容
    """
    if search_type == "id":
        ret = (
            db.session.query(
                Book.book_id.label("book_id"),
                Book.title.label("title"),
                Book.author.label("author"),
                Book.ISBN.label("ISBN"),
                Book.place.label("place"),
                Book.state.label("state"),
            )
            .join(Publisher)
            .add_column(Publisher.publisher_name)
            .filter(Book.book_id == search_text)
            .order_by(Book.book_id)
            .all()
        )
    elif search_type == "title":
        ret = (
            db.session.query(
                Book.book_id.label("book_id"),
                Book.title.label("title"),
                Book.author.label("author"),
                Book.ISBN.label("ISBN"),
                Book.place.label("place"),
                Book.state.label("state"),
            )
            .join(Publisher)
            .add_column(Publisher.publisher_name)
            .filter(Book.title == search_text)
            .order_by(Book.book_id)
            .all()
        )
    elif search_type == "author":
        ret = (
            db.session.query(
                Book.book_id.label("book_id"),
                Book.title.label("title"),
                Book.author.label("author"),
                Book.ISBN.label("ISBN"),
                Book.place.label("place"),
                Book.state.label("state"),
            )
            .join(Publisher)
            .add_column(Publisher.publisher_name)
            .filter(Book.author == search_text)
            .order_by(Book.book_id)
            .all()
        )
    elif search_type == "ISBN":
        ret = (
            db.session.query(
                Book.book_id.label("book_id"),
                Book.title.label("title"),
                Book.author.label("author"),
                Book.ISBN.label("ISBN"),
                Book.place.label("place"),
                Book.state.label("state"),
            )
            .join(Publisher)
            .add_column(Publisher.publisher_name)
            .filter(Book.ISBN == search_text)
            .order_by(Book.book_id)
            .all()
        )
    elif search_type == "publisher":
        ret = (
            db.session.query(
                Book.book_id.label("book_id"),
                Book.title.label("title"),
                Book.author.label("author"),
                Book.ISBN.label("ISBN"),
                Book.place.label("place"),
                Book.state.label("state"),
            )
            .join(Publisher)
            .add_column(Publisher.publisher_name)
            .filter(Publisher.publisher_name == search_text)
            .order_by(Book.book_id)
            .all()
        )
    else:
        ret = []
    return ret
    # return []


def edit_book(book_id, place) -> bool:
    """
    修改书籍信息,place为书籍所在书架位置,返回是否修改成功
    """
    book = Book.query.filter(Book.book_id == book_id).first()
    book.place = place
    db.session.add(book)
    db.session.commit()
    return True


def books_to_return(reader_id):
    """
    读者借阅的书籍,返回书籍列表(书籍ID、书名、借阅时间、剩余时间)
    [{book_id, title, date, day_left}]
    """
    # books = Borrow.query(Book.book_id, Book.title, Borrow.date).filter(Borrow.reader_id == reader_id).all()
    reader_type = Reader.query.filter(Reader.reader_id == reader_id).first().type_name
    available_number = (
        ReaderType.query.filter(ReaderType.type_name == reader_type)
        .first()
        .available_number
    )
    # todo: 查询已借阅书籍
    books = (
        db.session.query(
            Borrow.book_id.label("book_id"),
            Borrow.date.label("date"),
            (Borrow.date + available_number - datetime.date.today()).label("day_left"),
        )
        .join(Book)
        .add_column(Book.title.label("title"))
        .filter(Borrow.reader_id == reader_id, Borrow.is_return == False)
    )
    return books


def return_book_by_id(book_id) -> bool:
    """
    读者还书,返回是否还书成功
    """
    # todo：逾期
    # 查找书籍和借阅记录
    book = Book.query.filter(Book.book_id == book_id).first()
    borrow = (
        Borrow.query.filter(Borrow.book_id == book_id)
        .order_by(Borrow.borrow_id.desc())
        .first()
    )

    # 检验是否超期
    # reader = Reader.query.filter(Reader.reader_id == borrow.reader_id).first()
    # reader_type = ReaderType.query.filter(ReaderType.type_name == reader.type_name).first()
    # if (datetime.date.today() - borrow.date).days > reader_type.day_limit:
    #     # 超期
    #     print('已逾期，请找管理员当面核销')
    #     # reader.credit -= 5
    #     return False

    # 修改书籍和借阅记录并提交
    book.state = True
    borrow.is_return = True
    db.session.add(book)
    db.session.add(borrow)
    db.session.commit()
    return True


def borrow_book(book_id, reader_id) -> bool:
    """
    读者借书,返回是否借书成功
    """
    # todo：讨论具体信誉值
    # 检验读者是否有借书资格
    reader = Reader.query.filter(Reader.reader_id == reader_id).first()
    reader_type = ReaderType.query.filter(
        ReaderType.type_name == reader.type_name
    ).first()
    # print(reader)
    # print(reader_type)
    # if reader.credit < 60: # 信誉值小于60则不能借书
    # return False

    # 检验读者是否超过借书数量限制
    borrow_count = Borrow.query.filter(
        and_(Borrow.reader_id == reader_id, Borrow.is_return == False)
    ).count()
    if borrow_count >= reader_type.available_number:
        print("借书数量超过限制")
        return False

    # 检验书籍是否可借
    book = Book.query.filter(Book.book_id == book_id).first()
    if book.state == False:  # 书籍已被借阅
        print("书籍已被借阅")
        return False

    # 修改书籍和借阅记录并提交
    book.state = False
    new_id = Borrow.query.order_by(Borrow.borrow_id.desc()).first().borrow_id + 1
    if not new_id:
        new_id = 1
    borrow = Borrow(
        borrow_id=new_id,
        book_id=book_id,
        reader_id=reader_id,
        date=datetime.date.today(),
        is_return=False,
    )
    db.session.add(book)
    db.session.add(borrow)
    db.session.commit()
    return True


def user_borrow_history(reader_id):
    """
    读者借书历史,返回书籍列表(书籍ID、书名、借阅时间、是否归还)
    [{book_id, title, date, is_return}]
    """
    books = (
        db.session.query(Book.book_id, Book.title, Borrow.date, Borrow.is_return)
        .filter(Borrow.reader_id == reader_id)
        .filter(Book.book_id == Borrow.book_id)
        .order_by(Borrow.date.desc())
        .all()
    )
    return books


def add_publisher(publisher_name, publisher_address) -> bool:
    """
    添加出版社,返回是否添加成功
    """
    publisher_id = (
        Publisher.query.order_by(Publisher.publisher_id.desc()).first().publisher_id + 1
    )
    publisher = Publisher(
        publisher_id=publisher_id,
        publisher_name=publisher_name,
        address=publisher_address,
    )
    db.session.add(publisher)
    db.session.commit()
    return True


def add_stack(stack_name, stack_address, stack_open_time) -> bool:
    """
    添加书库,返回是否添加成功
    """
    stack_id = Stack.query.order_by(Stack.stack_id.desc()).first().stack_id + 1
    stack = Stack(
        stack_id=stack_id,
        stack_name=stack_name,
        location=stack_address,
        opening=stack_open_time,
    )
    db.session.add(stack)
    db.session.commit()
    return True


def modify_reader(reader_id, type_name) -> bool:
    """
    修改读者类型,返回是否修改成功
    """
    reader = Reader.query.filter(Reader.reader_id == reader_id).first()
    if reader == None:
        return False
    reader.type_name = type_name
    db.session.add(reader)
    db.session.commit()
    return True


def add_entering(
    title,
    book_id,
    ISBN,
    type_name,
    author,
    publisher_id,
    stack_id,
    place,
    reason,
    staff_id,
) -> bool:
    """
    添加入库书籍,返回是否添加成功
    book的外键publisher_id和stack_id需要先查询出对应的id，如果没有则需要先添加
    """
    if Publisher.query.filter(Publisher.publisher_id == publisher_id).first() == None:
        return False
    if Stack.query.filter(Stack.stack_id == stack_id).first() == None:
        return False
    book = Book(
        book_id=book_id,
        ISBN=ISBN,
        type=type_name,
        title=title,
        author=author,
        publisher_id=publisher_id,
        availability=True,
        state=True,
        place=place,
        stack_id=stack_id,
    )
    entering = BookEntering(
        book_id=book_id, staff_id=staff_id, reason=reason, date=datetime.date.today()
    )
    db.session.add(book)
    db.session.add(entering)
    db.session.commit()
    return True


def add_out(book_id, reason, staff_id) -> bool:
    """
    添加出库书籍,返回是否添加成功
    出库后不再被收录
    出库时需要确定书籍是否被借出,若被借出则需要先还书，先还书的操作在借书时已经完成
    """
    book = Book.query.get(book_id)
    print(book.availability, book.state)
    if book.availability == False or book.state == False:
        return False
    bookout = BookOut(
        book_id=book_id, date=datetime.date.today(), reason=reason, staff_id=staff_id
    )
    book.availability = False
    book.state = False
    db.session.add(bookout)
    db.session.commit()
    return True


def admin_modify_info(admin_id, account, password) -> bool:
    """
    修改管理员信息,返回是否修改成功
    id不修改
    password若为空则不修改
    检查account是否重复
    """
    admin = Admin.query.get(admin_id)
    if (
        account != admin.account
        and Admin.query.filter(Admin.account == account).first() != None
    ):
        return False
    admin.account = account
    if password:
        admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    return True


def staff_modify_info(
    staff_id, name, age, id_card, phone_number, address, account, password
) -> bool:
    """
    修改员工信息,返回是否修改成功
    id不修改
    password若为空则不修改
    检查account是否重复
    """
    staff = Staff.query.get(staff_id)
    if (
        account != staff.account
        and Staff.query.filter(Staff.account == account).first() != None
    ):
        return False
    staff.name = name
    staff.age = age
    staff.id_card = id_card
    staff.phone_number = phone_number
    staff.address = address
    staff.account = account
    if password:
        staff.set_password(password)
    db.session.add(staff)
    db.session.commit()
    return True


def reader_modify_info(reader_id, name, id_card, account, password) -> bool:
    """
    修改读者信息,返回是否修改成功
    id不修改
    password若为空则不修改
    检查account是否重复
    """
    reader = Reader.query.get(reader_id)
    if (
        account != reader.account
        and Reader.query.filter(Reader.account == account).first() != None
    ):
        return False
    reader.name = name
    reader.id_card = id_card
    reader.account = account
    if password:
        reader.set_password(password)
    db.session.add(reader)
    db.session.commit()
    return True


def add_new_staff(account, password) -> bool:
    """
    添加新员工,返回是否添加成功
    检查account是否重复
    """
    if Staff.query.filter(Staff.account == account).first() != None:
        return False
    staff = Staff(account=account)
    staff.set_password(password)
    db.session.add(staff)
    db.session.commit()
    return True
