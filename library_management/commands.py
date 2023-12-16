import click

from library_management import app, db
from library_management.models import *
from datetime import date

@app.cli.command()
@click.option('--drop',is_flag=True,help='Create after drop.') # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop: # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') # 输出提示信息


@app.cli.command()
@click.option('--account',prompt=True,help='The account used to login.')
@click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True,help='The password used to login.')
def admin(account,password):
    """Create admin."""
    db.create_all()
    admins = Admin.query.filter_by(account=account).all()
    if admins:
        click.echo('The account already exist.')
        return
    else:
        click.echo('Creating admin...')
        admin = Admin(account=account)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        click.echo('Done.')


@app.cli.command()
def forge():
    '''Generate fake data.'''
    db.create_all()
    staffs = [
        {'staff_id':1,'name':'张三','age':20,'id_card':'123456789012345678','phone_number':'12345678901','address':'北京市','account':'staff1','password':'123456'},
        {'staff_id':2,'name':'李四','age':21,'id_card':'123456789012345678','phone_number':'12345678901','address':'北京市','account':'staff2','password':'123456'}
    ]

    for s in staffs:
        staff = Staff(staff_id=s['staff_id'],name=s['name'],age=s['age'],id_card=s['id_card'],phone_number=s['phone_number'],address=s['address'],account=s['account'])
        staff.set_password(s['password'])
        db.session.add(staff)

    reader_types = [
        {'type_name':'新人','available_number':5,'days':30},
        {'type_name':'熟人','available_number':10,'days':60},
    ]

    for r in reader_types:
        reader_type = ReaderType(type_name=r['type_name'],available_number=r['available_number'],days=r['days'])
        db.session.add(reader_type)

    readers = [
        {'reader_id':1,'type_name':'新人','name':'王五','id_card':'123456789012345678','account':'reader1','password':'123456','credit':100},
        {'reader_id':2,'type_name':'熟人','name':'赵六','id_card':'123456789012345678','account':'reader2','password':'123456','credit':100}
    ]

    for r in readers:
        reader = Reader(reader_id=r['reader_id'],type_name=r['type_name'],name=r['name'],id_card=r['id_card'],account=r['account'],credit=r['credit'])
        reader.set_password(r['password'])
        db.session.add(reader)

    publishers = [
        {'publisher_id':1,'publisher_name':'出版社1','address':'北京市'},
        {'publisher_id':2,'publisher_name':'出版社2','address':'北京市'}
    ]

    for p in publishers:
        publisher = Publisher(publisher_id=p['publisher_id'],publisher_name=p['publisher_name'],address=p['address'])
        db.session.add(publisher)

    stacks = [
        {'stack_id':1,'stack_name':'A','location':'北京市','opening':'9:00'},
        {'stack_id':2,'stack_name':'B','location':'北京市','opening':'9:00'}
    ]

    for s in stacks:
        stack = Stack(stack_id=s['stack_id'],stack_name=s['stack_name'],location=s['location'],opening=s['opening'])
        db.session.add(stack)

    books = [
        {'book_id':1,'title':'书1','type':"类型1",'author':'作者1','publisher_id':1,'stack_id':1,'availability':False,'ISBN':'1234567890123','place':'A1','state':1},
        {'book_id':2,'title':'书2','type':"类型2",'author':'作者2','publisher_id':2,'stack_id':2,'availability':True,'ISBN':'1234567890124','place':'A2','state':0}
    ]

    for b in books:
        book = Book(book_id=b['book_id'],title=b['title'],type=b['type'],author=b['author'],publisher_id=b['publisher_id'],stack_id=b['stack_id'],availability=b['availability'],ISBN=b['ISBN'],place=b['place'],state=b['state'])
        db.session.add(book)

    bookouts = [
        {'book_id':1,'staff_id':1,'date':date(2022,11,1),'reason':'原因1'}
    ]

    for b in bookouts:
        bookout = BookOut(book_id=b['book_id'],staff_id=b['staff_id'],date=b['date'],reason=b['reason'])
        db.session.add(bookout)

    bookenterings = [
        {'book_id':1,'staff_id':1,'date':date(2020,1,1),'reason':'原因1'},
        {'book_id':2,'staff_id':2,'date':date(2021,11,12),'reason':'原因1'}
    ]

    for b in bookenterings:
        bookentering = BookEntering(book_id=b['book_id'],staff_id=b['staff_id'],date=b['date'],reason=b['reason'])
        db.session.add(bookentering)

    borrows = [
        {'book_id':1,'reader_id':1,'date':date(2021,1,1),'is_return':True},
        {'book_id':2,'reader_id':2,'date':date(2022,11,15),'is_return':False}
    ]
    
    for b in borrows:
        borrow = Borrow(book_id=b['book_id'],reader_id=b['reader_id'],date=b['date'],is_return=b['is_return'])
        db.session.add(borrow)
    
    db.session.commit()
    click.echo('Done.')

