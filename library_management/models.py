from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from library_management import db

class Admin(db.Model, UserMixin):
    '''管理员'''
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True) # 管理者编号
    account = db.Column(db.String(20), unique=True) # 账号
    password_hash = db.Column(db.String(128)) # 密码散列值

    def get_id(self):
        '''身份验证'''
        return self.admin_id
    
    def set_password(self, password):
        '''设置密码'''
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        '''验证密码'''
        return check_password_hash(self.password_hash, password)


class Staff(db.Model, UserMixin):
    '''职工'''
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True) # 职工编号
    name = db.Column(db.String(40)) # 姓名
    age = db.Column(db.Integer) # 年龄
    id_card = db.Column(db.String(18)) # 身份证号
    phone_number = db.Column(db.String(11)) # 电话号码
    address = db.Column(db.String(80)) # 地址
    account = db.Column(db.String(20), unique=True) # 账号
    password_hash = db.Column(db.String(128)) # 密码散列值

    def get_id(self):
        '''身份验证'''
        return self.staff_id
    
    def set_password(self, password):
        '''设置密码'''
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        '''验证密码'''
        return check_password_hash(self.password_hash, password)


class Reader(db.Model, UserMixin):
    '''读者'''
    __tablename__ = 'reader'
    reader_id = db.Column(db.Integer, primary_key=True) # 读者编号
    type_name = db.Column(db.String(10), db.ForeignKey('reader_type.type_name',ondelete='SET NULL')) # 读者类型
    name = db.Column(db.String(40)) # 姓名
    id_card = db.Column(db.String(18)) # 身份证号
    account = db.Column(db.String(20), unique=True) # 账号
    password_hash = db.Column(db.String(128)) # 密码散列值
    credit = db.Column(db.Integer) # 信誉值

    def get_id(self):
        '''身份验证'''
        return self.reader_id
    
    def set_password(self, password):
        '''设置密码'''
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        '''验证密码'''
        return check_password_hash(self.password_hash, password)

class ReaderType(db.Model):
    '''读者类型'''
    __tablename__ = 'reader_type'
    type_name = db.Column(db.String(10), primary_key=True) # 读者类型
    available_number = db.Column(db.Integer) # 可借数量
    days = db.Column(db.Integer) # 可借天数

class Publisher(db.Model):
    __tablename__ = 'publisher'
    publisher_id = db.Column(db.Integer, primary_key=True) # 出版社编号
    publisher_name = db.Column(db.String(40)) # 出版社名称
    address = db.Column(db.String(80)) # 出版社地址

class Stack(db.Model):
    '''书库'''
    __tablename__ = 'stack'
    stack_id = db.Column(db.Integer, primary_key=True) # 书库编号
    stack_name = db.Column(db.String(25)) # 书库名称
    location = db.Column(db.String(80)) # 书库位置
    opening = db.Column(db.String(40)) # 开放时间
    
class Book(db.Model):
    '''图书'''
    __tablename__ = 'book'
    book_id = db.Column(db.Integer, primary_key=True) # 图书编号
    stack_id = db.Column(db.Integer, db.ForeignKey('stack.stack_id',ondelete='SET NULL')) # 书库编号
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.publisher_id',ondelete='SET NULL')) # 出版社编号
    title = db.Column(db.String(40)) # 图书名称
    type = db.Column(db.String(25)) # 图书类型
    author = db.Column(db.String(40)) # 作者
    availability = db.Column(db.Boolean) # 是否被收录
    ISBN = db.Column(db.String(13)) # ISBN
    place = db.Column(db.String(40)) # 存放位置
    state = db.Column(db.Numeric(precision=1, scale=0)) # 图书状态

# class BookOut(db.Model):
#     '''出库'''
#     __tablename__ = 'book_out'
#     book_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('book')) # 书籍编号

# class BookEntering(db.Model):
#     '''入库'''
#     __tablename__ = 'book_entering'
    

# class Borrow(db.Model):
#     '''借阅'''
#     __tablename__ = 'borrow'




