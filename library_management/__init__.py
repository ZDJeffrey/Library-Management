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
login_manager.login_view = 'login'  # 设置登录页面的视图名称

@login_manager.user_loader
def load_user(user_id):
    prefix, id = user_id.split('.')
    if prefix == 'admin':
        from library_management.models import Admin
        return Admin.query.get(int(id))
    elif prefix == 'staff':
        from library_management.models import Staff
        return Staff.query.get(int(id))
    elif prefix == 'reader':
        from library_management.models import Reader
        return Reader.query.get(int(id))
    else:
        return None
    
@app.context_processor
def inject_user_type():
    from library_management.models import Admin, Staff, Reader
    from flask_login import current_user
    if isinstance(current_user, Admin):
        user_type = 'admin'
    elif isinstance(current_user, Staff):
        user_type = 'staff'
    elif isinstance(current_user, Reader):
        user_type = 'reader'
    else:
        user_type = None
    return dict(user_type=user_type)

from library_management import views, commands

