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
        {'reader_id':1,'type_name':'初级','name':'常开翊','id_card':'654324195506141578','account':'reader1','password':'123456','credit':51},
        {'reader_id':2,'type_name':'中级','name':'韶洋玉','id_card':'610425198910019237','account':'reader2','password':'123456','credit':72},
        {'reader_id':3,'type_name':'中级','name':'虞蓬岗','id_card':'411627201503074628','account':'reader3','password':'123456','credit':70},
        {'reader_id':4,'type_name':'高级','name':'钱苏晶','id_card':'130203196904307512','account':'reader4','password':'123456','credit':91},
        {'reader_id':5,'type_name':'中级','name':'嵇漫蕾','id_card':'130535195503194441','account':'reader5','password':'123456','credit':71},
        {'reader_id':6,'type_name':'初级','name':'牧东严','id_card':'445281202207014540','account':'reader6','password':'123456','credit':57},
        {'reader_id':7,'type_name':'中级','name':'邴颢恩','id_card':'371302198905014192','account':'reader7','password':'123456','credit':78},
        {'reader_id':8,'type_name':'初级','name':'武烁来','id_card':'520327199111203599','account':'reader8','password':'123456','credit':54},
        {'reader_id':9,'type_name':'初级','name':'昌兵众','id_card':'540123201110032932','account':'reader9','password':'123456','credit':50},
        {'reader_id':10,'type_name':'中级','name':'颜希卿','id_card':'540302196403073872','account':'reader10','password':'123456','credit':70},
        {'reader_id':11,'type_name':'高级','name':'鲁泽霞','id_card':'410622202202054019','account':'reader11','password':'123456','credit':95},
        {'reader_id':12,'type_name':'初级','name':'郑柏飙','id_card':'532926201303202731','account':'reader12','password':'123456','credit':59},
        {'reader_id':13,'type_name':'高级','name':'武源柏','id_card':'610828201306254639','account':'reader13','password':'123456','credit':93},
        {'reader_id':14,'type_name':'中级','name':'牧翊朴','id_card':'34122519460923847X','account':'reader14','password':'123456','credit':75},
        {'reader_id':15,'type_name':'初级','name':'柳萱义','id_card':'430821196906047423','account':'reader15','password':'123456','credit':55}
    ]

    for r in readers:
        reader = Reader(reader_id=r['reader_id'],type_name=r['type_name'],name=r['name'],id_card=r['id_card'],account=r['account'],credit=r['credit'])
        reader.set_password(r['password'])
        db.session.add(reader)

    publishers = [
        {'publisher_id':1,'publisher_name':'人民出版社','address':'中华人民共和国北京市东城区隆福寺街99号金隆基大厦'},
        {'publisher_id':2,'publisher_name':'人民文学出版社','address':'北京市东城区朝阳门内大街166号'},
        {'publisher_id':3,'publisher_name':'科学出版社','address':'北京东城区东黄城根北街16号'},
        {'publisher_id':4,'publisher_name':'高等教育出版社','address':'北京市西城区德胜门外大街4号'},
        {'publisher_id':5,'publisher_name':'人民教育出版社','address':'北京市海淀区中关村南大街17号院'},
        {'publisher_id':6,'publisher_name':'机械工业出版社','address':'北京西城区百万庄大街22号'},
        {'publisher_id':7,'publisher_name':'北京大学出版社','address':'北京市海淀区成府路205号'},
        {'publisher_id':8,'publisher_name':'清华大学出版社','address':'北京市海淀区清华园街道双清路30号学研大厦'},
        {'publisher_id':9,'publisher_name':'中山大学出版社','address':'广州市新港西路135号校内东北区343栋'}
    ]

    for p in publishers:
        publisher = Publisher(publisher_id=p['publisher_id'],publisher_name=p['publisher_name'],address=p['address'])
        db.session.add(publisher)

    stacks = [
        {'stack_id':1,'stack_name':'南图书馆','location':'广东省广州市番禺区外环东路132号中山大学东校区','opening':'7:00'},
        {'stack_id':2,'stack_name':'东图书馆','location':'广东省广州市海珠区新港西路135号中山大学南校区','opening':'8:00'},
        {'stack_id':3,'stack_name':'北图书馆','location':'广东省广州市越秀区中山二路74号中山大学北校区','opening':'8:00'}
    ]

    for s in stacks:
        stack = Stack(stack_id=s['stack_id'],stack_name=s['stack_name'],location=s['location'],opening=s['opening'])
        db.session.add(stack)

    books = [
        {'book_id':1,'title':'纯粹理性批判','type':"哲学",'author':'康德','publisher_id':1,'stack_id':1,'availability':True,'ISBN':'9787010040592','place':'A1','state':False},
        {'book_id':2,'title':'资本论','type':"哲学",'author':'马克思','publisher_id':1,'stack_id':2,'availability':True,'ISBN':'9787010191652','place':'A2','state':True},
        {'book_id':3,'title':'家庭、私有制和国家的起源','type':"哲学",'author':'恩格斯','publisher_id':1,'stack_id':3,'availability':True,'ISBN':'9787010029726','place':'A3','state':False},
        {'book_id':4,'title':'碎片','type':"散文",'author':'埃莱娜·费兰特','publisher_id':2,'stack_id':1,'availability':False,'ISBN':'9787020159178','place':'A4','state':False},
        {'book_id':5,'title':'昆虫记','type':"自然",'author':'法布尔','publisher_id':2,'stack_id':2,'availability':True,'ISBN':'9787020137909','place':'A5','state':True},
        {'book_id':6,'title':'朝花夕拾','type':"散文",'author':'鲁迅','publisher_id':2,'stack_id':3,'availability':True,'ISBN':'9787020137701','place':'A6','state':True},
        {'book_id':7,'title':'进化','type':"生物",'author':'巴顿','publisher_id':3,'stack_id':1,'availability':True,'ISBN':'9787030271754','place':'A7','state':True},
        {'book_id':8,'title':'赛博朋克科幻文化研究','type':"思想",'author':'余泽梅','publisher_id':3,'stack_id':2,'availability':True,'ISBN':'9787030651679','place':'A8','state':False},
        {'book_id':9,'title':'人工智能原理（高等教育出版社）','type':"计算机科学与技术",'author':'王文敏','publisher_id':4,'stack_id':3,'availability':True,'ISBN':'9787040521887','place':'A9','state':False},
        {'book_id':10,'title':'图书馆学基础','type':"图书馆学",'author':'吴慰慈','publisher_id':4,'stack_id':1,'availability':True,'ISBN':'9787040153378','place':'A10','state':True},
        {'book_id':11,'title':'叔本华的治疗','type':"心理",'author':'Irvin D. Yalom','publisher_id':6,'stack_id':2,'availability':True,'ISBN':'9787111659280','place':'A11','state':False},
        {'book_id':12,'title':'组合数学(原书第5版)','type':"计算机科学与技术",'author':'Richard A. Brualdi','publisher_id':6,'stack_id':3,'availability':True,'ISBN':'9787111377870','place':'A12','state':True},
        {'book_id':13,'title':'西方哲学十五讲','type':"哲学",'author':'张志伟','publisher_id':7,'stack_id':1,'availability':True,'ISBN':'9787301068687','place':'A13','state':True},
        {'book_id':14,'title':'雾中风景','type':"电影",'author':'戴锦华','publisher_id':7,'stack_id':2,'availability':True,'ISBN':'9787301271674','place':'A14','state':True},
        {'book_id':15,'title':'深度强化学习图解','type':"计算机科学与技术",'author':'Miguel Morales','publisher_id':8,'stack_id':3,'availability':True,'ISBN':'9787302605461','place':'A15','state':True},
        {'book_id':16,'title':'吾心可鉴','type':"哲学",'author':'彭凯平','publisher_id':8,'stack_id':1,'availability':False,'ISBN':'9787302437352','place':'A16','state':False},
        {'book_id':17,'title':'白发魔女传','type':"小说",'author':'梁羽生','publisher_id':9,'stack_id':2,'availability':True,'ISBN':'9787306042095','place':'A17','state':True},
        {'book_id':18,'title':'小说写作十日谈','type':"写作",'author':'汤达','publisher_id':9,'stack_id':3,'availability':False,'ISBN':'9787306075789','place':'A18','state':False}
    ]

    for b in books:
        book = Book(book_id=b['book_id'],title=b['title'],type=b['type'],author=b['author'],publisher_id=b['publisher_id'],stack_id=b['stack_id'],availability=b['availability'],ISBN=b['ISBN'],place=b['place'],state=b['state'])
        db.session.add(book)

    bookouts = [
        {'book_id':4,'staff_id':9,'date':date(2023,12,16),'reason':'图书损坏'},
        {'book_id':18,'staff_id':1,'date':date(2023,12,25),'reason':'图书丢失'},
        {'book_id':16,'staff_id':2,'date':date(2023,10,1),'reason':'图书捐赠'}
    ]

    for b in bookouts:
        bookout = BookOut(book_id=b['book_id'],staff_id=b['staff_id'],date=b['date'],reason=b['reason'])
        db.session.add(bookout)

    bookenterings = [
        {'book_id':1,'staff_id':1,'date':date(2020,1,1),'reason':'图书购入'},
        {'book_id':2,'staff_id':2,'date':date(2021,11,12),'reason':'图书购入'},
        {'book_id':3,'staff_id':3,'date':date(2019,10,12),'reason':'图书购入'},
        {'book_id':4,'staff_id':4,'date':date(2018,5,12),'reason':'图书购入'},
        {'book_id':5,'staff_id':5,'date':date(2017,9,12),'reason':'图书购入'},
        {'book_id':6,'staff_id':6,'date':date(2016,3,12),'reason':'图书购入'},
        {'book_id':7,'staff_id':7,'date':date(2015,2,5),'reason':'图书购入'},
        {'book_id':8,'staff_id':8,'date':date(2014,7,12),'reason':'图书购入'},
        {'book_id':9,'staff_id':9,'date':date(2013,11,5),'reason':'图书购入'},
        {'book_id':10,'staff_id':10,'date':date(2012,11,12),'reason':'图书购入'},
        {'book_id':11,'staff_id':1,'date':date(2022,9,8),'reason':'图书购入'},
        {'book_id':12,'staff_id':2,'date':date(2021,5,12),'reason':'图书购入'},
        {'book_id':13,'staff_id':3,'date':date(2020,5,4),'reason':'图书购入'},
        {'book_id':14,'staff_id':4,'date':date(2019,1,12),'reason':'图书购入'},
        {'book_id':15,'staff_id':5,'date':date(2018,7,5),'reason':'图书购入'},
        {'book_id':16,'staff_id':6,'date':date(2017,7,1),'reason':'图书购入'},
        {'book_id':17,'staff_id':7,'date':date(2016,6,12),'reason':'图书购入'},
        {'book_id':18,'staff_id':8,'date':date(2015,5,7),'reason':'图书购入'}
    ]

    for b in bookenterings:
        bookentering = BookEntering(book_id=b['book_id'],staff_id=b['staff_id'],date=b['date'],reason=b['reason'])
        db.session.add(bookentering)

    borrows = [
        {'book_id':1,'reader_id':1,'date':date(2023,1,1),'is_return':True},
        {'book_id':1,'reader_id':5,'date':date(2023,4,5),'is_return':True},
        {'book_id':1,'reader_id':7,'date':date(2023,12,15),'is_return':False},
        {'book_id':2,'reader_id':2,'date':date(2023,2,18),'is_return':True},
        {'book_id':2,'reader_id':4,'date':date(2023,4,9),'is_return':True},
        {'book_id':2,'reader_id':8,'date':date(2023,8,5),'is_return':True},
        {'book_id':2,'reader_id':6,'date':date(2023,6,1),'is_return':True},
        {'book_id':3,'reader_id':3,'date':date(2023,3,1),'is_return':True},
        {'book_id':3,'reader_id':10,'date':date(2023,3,15),'is_return':True},
        {'book_id':3,'reader_id':15,'date':date(2023,6,18),'is_return':True},
        {'book_id':3,'reader_id':11,'date':date(2023,11,16),'is_return':False},
        {'book_id':4,'reader_id':12,'date':date(2023,11,16),'is_return':True},
        {'book_id':5,'reader_id':9,'date':date(2023,9,16),'is_return':True},
        {'book_id':5,'reader_id':6,'date':date(2023,7,16),'is_return':True},
        {'book_id':7,'reader_id':7,'date':date(2023,4,15),'is_return':True},
        {'book_id':8,'reader_id':14,'date':date(2023,1,16),'is_return':True},
        {'book_id':8,'reader_id':11,'date':date(2023,6,17),'is_return':True},
        {'book_id':8,'reader_id':1,'date':date(2023,11,15),'is_return':False},
        {'book_id':9,'reader_id':12,'date':date(2023,1,7),'is_return':True},
        {'book_id':9,'reader_id':6,'date':date(2023,4,6),'is_return':True},
        {'book_id':9,'reader_id':4,'date':date(2023,11,19),'is_return':False},
        {'book_id':10,'reader_id':3,'date':date(2023,1,16),'is_return':True},
        {'book_id':10,'reader_id':1,'date':date(2023,3,9),'is_return':True},
        {'book_id':10,'reader_id':5,'date':date(2023,7,7),'is_return':True},
        {'book_id':11,'reader_id':1,'date':date(2023,12,6),'is_return':False},
        {'book_id':12,'reader_id':15,'date':date(2023,12,16),'is_return':True},
        {'book_id':13,'reader_id':13,'date':date(2023,1,4),'is_return':True},
        {'book_id':14,'reader_id':15,'date':date(2023,4,4),'is_return':True},
        {'book_id':15,'reader_id':2,'date':date(2023,2,25),'is_return':True},
        {'book_id':17,'reader_id':3,'date':date(2023,1,25),'is_return':True},
        {'book_id':18,'reader_id':6,'date':date(2023,10,25),'is_return':True},
    ]
    
    for b in borrows:
        borrow = Borrow(book_id=b['book_id'],reader_id=b['reader_id'],date=b['date'],is_return=b['is_return'])
        db.session.add(borrow)
    
    db.session.commit()
    click.echo('Done.')

