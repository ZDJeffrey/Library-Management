import click

from library_management import app, db
from library_management.models import Admin, Staff, Reader, ReaderType

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

    reader_types = [
        {'type_name':'新人','available_number':5,'days':30},
        {'type_name':'熟人','available_number':10,'days':60},
    ]

    readers = [
        {'reader_id':1,'type_name':'新人','name':'王五','id_card':'123456789012345678','account':'reader1','password':'123456','credit':100},
        {'reader_id':2,'type_name':'熟人','name':'赵六','id_card':'123456789012345678','account':'reader2','password':'123456','credit':100}
    ]

    for s in staffs:
        staff = Staff(staff_id=s['staff_id'],name=s['name'],age=s['age'],id_card=s['id_card'],phone_number=s['phone_number'],address=s['address'],account=s['account'])
        staff.set_password(s['password'])
        db.session.add(staff)

    for r in reader_types:
        reader_type = ReaderType(type_name=r['type_name'],available_number=r['available_number'],days=r['days'])
        db.session.add(reader_type)
    
    for r in readers:
        reader = Reader(reader_id=r['reader_id'],type_name=r['type_name'],name=r['name'],id_card=r['id_card'],account=r['account'],credit=r['credit'])
        reader.set_password(r['password'])
        db.session.add(reader)
    
    db.session.commit()
    click.echo('Done.')

