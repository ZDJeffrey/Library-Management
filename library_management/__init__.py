import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

# 配置信息
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # 数据库实例
login_manager = LoginManager(app) # 登录管理实例

@login_manager.user_loader
def load_admin(admin_id):
    from library_management.models import Admin
    admin = Admin.query.get(int(admin_id))
    return admin

@login_manager.user_loader
def load_staff(staff_id):
    from library_management.models import Staff
    staff = Staff.query.get(int(staff_id))
    return staff

@login_manager.user_loader
def load_reader(reader_id):
    from library_management.models import Reader
    reader = Reader.query.get(int(reader_id))
    return reader

from library_management import views, commands

