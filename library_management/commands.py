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
        {'staff_id': 1,'name': '张三', 'age': 29, 'id_card': '441523199406220640', 'phone_number': '13558888101', 'address': '北京市朝阳区', 'account': 'staff1', 'password': '123456'},
        {'staff_id': 2,'name': '李四', 'age': 71, 'id_card': '510181195201137000', 'phone_number': '13743274295', 'address': '上海市浦东新区', 'account': 'staff2', 'password': '123456'},
        {'staff_id': 3,'name': '王五', 'age': 47, 'id_card': '130526197602079329', 'phone_number': '15293954106', 'address': '广州市天河区', 'account': 'staff3', 'password': '123456'},
        {'staff_id': 4,'name': '赵四', 'age': 39, 'id_card': '320312198411127720', 'phone_number': '15279318772', 'address': '天津市和平区', 'account': 'staff4', 'password': '123456'},
        {'staff_id': 5,'name': '刘七', 'age': 55, 'id_card': '210381196803096925', 'phone_number': '15530146898', 'address': '杭州市西湖区', 'account': 'staff5', 'password': '123456'},
        {'staff_id': 6,'name': '陈八', 'age': 54, 'id_card': '430821196906047423', 'phone_number': '15695845331', 'address': '成都市武侯区', 'account': 'staff6', 'password': '123456'},
        {'staff_id': 7,'name': '杨九', 'age': 40, 'id_card': '34122519460923847X', 'phone_number': '15234854630', 'address': '沈阳市沈河区', 'account': 'staff7', 'password': '123456'},
        {'staff_id': 8,'name': '黄十', 'age': 33, 'id_card': '610828202206254639', 'phone_number': '13673843100', 'address': '南京市鼓楼区', 'account': 'staff8', 'password': '123456'},
        {'staff_id': 9,'name': '许翰', 'age': 29, 'id_card': '410622202202054019', 'phone_number': '17676442882', 'address': '石家庄市长安区', 'account': 'staff9', 'password': '123456'},
        {'staff_id': 10,'name': '郭离', 'age': 36, 'id_card': '540302196403073872', 'phone_number': '18144286738', 'address': '福州市鼓楼区', 'account': 'staff10', 'password': '123456'},
    ]


    for s in staffs:
        staff = Staff(staff_id=s['staff_id'],name=s['name'],age=s['age'],id_card=s['id_card'],phone_number=s['phone_number'],address=s['address'],account=s['account'])
        staff.set_password(s['password'])
        db.session.add(staff)

    reader_types = [
        {'type_name':'初级','available_number':2,'days':30},
        {'type_name':'中级','available_number':4,'days':45},
        {'type_name':'高级','available_number':8,'days':60}
    ]

    for r in reader_types:
        reader_type = ReaderType(type_name=r['type_name'],available_number=r['available_number'],days=r['days'])
        db.session.add(reader_type)

    readers = [
        {'reader_id':1,'type_name':'初级','name':'常开翊','id_card':'654324195506141578','account':'reader1','password':'123456','credit':50},
        {'reader_id':2,'type_name':'中级','name':'韶洋玉','id_card':'610425198910019237','account':'reader2','password':'123456','credit':70},
        {'reader_id':3,'type_name':'中级','name':'虞蓬岗','id_card':'411627201503074628','account':'reader3','password':'123456','credit':70},
        {'reader_id':4,'type_name':'高级','name':'钱苏晶','id_card':'130203196904307512','account':'reader4','password':'123456','credit':90},
        {'reader_id':5,'type_name':'中级','name':'嵇漫蕾','id_card':'130535195503194441','account':'reader5','password':'123456','credit':70},
        {'reader_id':6,'type_name':'初级','name':'牧东严','id_card':'445281202207014540','account':'reader6','password':'123456','credit':50},
        {'reader_id':7,'type_name':'中级','name':'邴颢恩','id_card':'371302198905014192','account':'reader7','password':'123456','credit':70},
        {'reader_id':8,'type_name':'初级','name':'武烁来','id_card':'520327199111203599','account':'reader8','password':'123456','credit':50},
        {'reader_id':9,'type_name':'初级','name':'昌兵众','id_card':'540123201110032932','account':'reader9','password':'123456','credit':50},
        {'reader_id':10,'type_name':'中级','name':'颜希卿','id_card':'540302196403073872','account':'reader10','password':'123456','credit':70},
        {'reader_id':11,'type_name':'高级','name':'鲁泽霞','id_card':'410622202202054019','account':'reader11','password':'123456','credit':90},
        {'reader_id':12,'type_name':'初级','name':'郑柏飙','id_card':'532926202203202731','account':'reader12','password':'123456','credit':50},
        {'reader_id':13,'type_name':'高级','name':'武源柏','id_card':'610828202206254639','account':'reader13','password':'123456','credit':90},
        {'reader_id':14,'type_name':'中级','name':'牧翊朴','id_card':'34122519460923847X','account':'reader14','password':'123456','credit':70},
        {'reader_id':15,'type_name':'初级','name':'柳萱义','id_card':'430821196906047423','account':'reader15','password':'123456','credit':50}
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
        {'stack_id':1,'stack_name':'西书库','location':'北京市','opening':'9:00'},
        {'stack_id':2,'stack_name':'东书库','location':'北京市','opening':'9:00'}
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

