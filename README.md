# 图书管理系统
这是一个使用Flask实现的简单的图书管理系统，Flask是一个轻量级的Python Web应用框架。
    <div style="display: flex; justify-content: center;">
        <img src="img/flask.png" style="max-height: 400px;">
    </div>
## 需求
- flask（网站）
- flask-login（用户登录）
- flask-sqlalchemy（数据库交互）
- python-dotenv（环境变量配置）
- colorama（命令行着色，flask依赖）

## 文件结构
```
.
├── library_management  # 应用包
│   ├── static          # 静态文件
│   ├── templates       # 模板文件
│   ├── __init__.py     # 应用实例
│   ├── commands.py     # 自定义命令
│   ├── models.py       # 模型
│   └── views.py        # 视图
├── wsgi.py             # 环境变量加载器
├── .flaskenv           # Flask环境变量
```
## 功能
- 登录
    在登录界面，可以选择登录的用户类型，包括读者、职工和管理员。
    <div style="display: flex; justify-content: center;">
        <img src="img/login.png" style="max-height: 400px;">
    </div>
- 修改/查看个人信息
    用户可以该该界面修改个人信息并申请保存，若修改有效，则会提示修改成功。
    <div style="display: flex; justify-content: center;">
        <img src="img/info.png" style="max-height: 400px;">
    </div>
- 图书查询
    图书查询作为图书管理系统的主页，可以通过ID、书名、作者、ISBN等信息查询书籍，并且可以根据每个条目后的按钮查看书籍的详细信息。
    <div style="display: flex; justify-content: center;">
        <img src="img/index.png" style="max-height: 400px;">
    </div>
- 书库查询
    书库查询可以查看所有书库的相关信息，其中职工可以新增书库。
    <div style="display: flex; justify-content: center;">
        <img src="img/stack.png" style="max-height: 400px;">
    </div>
- 出版社查询
    出版社查询可以查看所有出版社的相关信息，其中职工可以新增出版社。
    <div style="display: flex; justify-content: center;">
        <img src="img/publisher.png" style="max-height: 400px;">
    </div>
- 读者
  - 注册
        读者可以通过该界面注册账号，注册成功后会跳转到登录界面。
        <div style="display: flex; justify-content: center;">
            <img src="img/register.png" style="max-height: 400px;">
        </div>
  - 借书
        在图书的详情界面，读者可以进行借书，若图书可以结果，则会提供借阅图书的按钮，点击后会根据读者的信息判断是否可以借阅，若可以借阅，则会提示借阅成功，否则会提示借阅失败。
        <div style="display: flex; justify-content: center;">
            <img src="img/borrow.png" style="max-height: 400px;">
        </div>
  - 还书
        读者可以在归还书籍界面查看正在借阅的书籍及相关信息，并且可以进行归还书籍。
        <div style="display: flex; justify-content: center;">
            <img src="img/return.png" style="max-height: 400px;">
        </div>
- 职工
  - 图书信息修改
        在图书的详情界面，职工可以查看该书籍的历史借阅记录、入库记录以及出库记录，并且可以修改图书的信息。
        <div style="display: flex; justify-content: center;">
            <img src="img/book_modify.png" style="max-height: 400px;">
        </div>
  - 图书入库
        职工可以查看所有入库记录，并且可以新增入库记录。
        <div style="display: flex; justify-content: center;">
            <img src="img/book_enter.png" style="max-height: 200px;">
            <img src="img/book_enter_add.png" style="max-height: 200px;">
        </div>
  - 图书出库
        职工可以查看所有出库记录，并且可以新增出库记录。
        <div style="display: flex; justify-content: center;">
            <img src="img/book_out.png" style="max-height: 200px;">
            <img src="img/book_out_add.png" style="max-height: 200px;">
        </div>
  - 读者管理
        职工可以查看所有读者，并通过详情按钮查看读者的详细信息，并允许对读者类型进行修改。
        <div style="display: flex; justify-content: center;">
            <img src="img/reader_management.png" style="max-height: 400px;">
        </div>
- 管理员
  - 职工管理
        管理员的主页显示所有职工的信息。
        <div style="display: flex; justify-content: center;">
            <img src="img/staff_management.png" style="max-height: 400px;">
        </div>
  - 新建职工
        管理员可以新建职工账号。
        <div style="display: flex; justify-content: center;">
            <img src="img/add_staff.png" style="max-height: 400px;">
        </div>
## 安装
- 克隆仓库
- 安装依赖
- 初始化数据库
    ```shell
    flask initdb --drop
    ```
    若修改了数据库关系模式，则需要重新初始化数据库
- 创建测试数据
    ```shell
    flask forge
    ```
    导入测试数据，以便测试应用
- 创建管理员账户
    ```shell
    flask admin
    ```
    创建管理员账户，以便登录管理网站
- 运行应用
    ```shell
    flask run
    ```
    运行网站，访问`http://127.0.0.1:5000/`，其余路由参见views.py文件
    ```shell
    flask initdb --drop; flask forge; flask run
    ```


# Library-Management
This is a simple Book Management System implemented using Flask, a lightweight web application framework for Python.

## Requirements
- flask
- flask-login
- flask-sqlalchemy
- python-dotenv
- colorama

## File Structure
```
.
├── library_management  # Application package
│   ├── static          # Static files
│   ├── templates       # Templates
|   |   ├── base.html   # Base template
|   |   ├── index.html  # Index template
|   |   ├── login.html  # login template
│   ├── __init__.py     # Application factory
│   ├── commands.py     # Custom commands
│   ├── models.py       # Models
│   └── views.py        # Views
├── wsgi.py             # Environment variables loader
├── .flaskenv           # Flask Environment variables
```

## Installation
- Clone the repository
- Install the requirements
- Initialize the database
    ```shell
    flask initdb --drop
    ```
- Create fake data to test the application
    ```shell
    flask forge
    ```
- Create an administrator account
    ```shell
    flask admin
    ```
- Run the application
    ```shell
    flask run
    ```



