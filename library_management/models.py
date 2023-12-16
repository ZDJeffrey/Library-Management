from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from library_management import db

# 管理员
class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True) # 管理者编号
    account = db.Column(db.String(20), unique=True) # 账号
    password_hash = db.Column(db.String(128)) # 密码散列值

    def get_id(self):
        '''身份验证'''
        return self.admin_id
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 职工
class Staff(db.Model, UserMixin):
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
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 读者
class Reader(db.Model, UserMixin):
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
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 读者类型
class ReaderType(db.Model):
    __tablename__ = 'reader_type'
    type_name = db.Column(db.String(10), primary_key=True) # 读者类型
    available_number = db.Column(db.Integer) # 可借数量
    days = db.Column(db.Integer) # 可借天数


# # 出库
# class BookOut(db.Model):
#     __tablename__ = 'book_out'


# # 入库
# class BookEntering(db.Model):
#     __tablename__ = 'book_entering'


# # 书籍
# class Book(db.Model):
#     __tablename__ = 'book'


# # 出版社
# class Publisher(db.Model):
#     __tablename__ = 'publisher'


# # 书库
# class Stack(db.Model):
#     __tablename__ = 'stack'


# # 借阅
# class Borrow(db.Model):
#     __tablename__ = 'borrow'




