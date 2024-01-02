# 需求建模

>  组员：张雄、郑圳毅、刘思迪

## 系统功能性需求

​	本网站的基本目标是提供一个存储图书馆的书籍用户信息的平台，记录图书基本信息以及借阅情况，同时满足图书馆职员的管理需求和读者的查询借阅需求，方便更好的管理图书馆和在图书馆借阅书籍。

​	网站主要的三类实体为读者、图书馆职员（管理员）和书籍，其中读者和职员为用户，书籍只需要储存信息。对于这三类角色，他们所需的主要功能如下：

- **图书馆职员**：记录书籍的入库和出库信息，管理图书馆库藏，增加/删减图书资源，管理读者的借阅权限；
- **读者**：查询图书信息，借出和归还书籍；
- **书籍**：记录书籍的基本信息、借阅情况以及在馆内所处的位置。

​	对于职员和读者这两种用户，用户组织架构图如下所示：

![用户组织架构图0](./assets/%E7%94%A8%E6%88%B7%E7%BB%84%E7%BB%87%E6%9E%B6%E6%9E%84%E5%9B%BE0.png)

## 系统用例

​	根据上述用户的基本功能性需求，以下列出可能的系统需求用例：

**读者：**

- 查询书籍信息
- 借出书籍
- 归还书籍
- 查询借阅记录
- 申请提升权限

**职员：**

- 管理读者权限
  - 提升读者权限
  - 降低读者权限
- 新增书籍入库
- 已有书籍出库
- 修改书籍信息
- 管理出版商信息
  - 增加出版商
  - 删除出版商

## 系统核心用例

### 读者借出书籍

**主要参与者：**读者

**涉众及关注点：**

1. 读者：希望能够快速完成借阅过程，
2. 职员：希望书籍已借出、归还时间等信息被准确录入

**前置条件：**系统中已经添加了读者的账号

**主成功场景：**

- 读者使用账号密码登录网站（在终端使用读者证录入信息）
- 读者选择批量或单独借出书籍
- 读者录入书籍信息
- 读者成功借出书籍，系统更新数据库信息

**扩展失败场景：**

- 读者的账号不存在或密码错误
- 书籍信息录入错误
- 读者的可借书籍数量不足
- 书籍状态为不可借阅

**发生频率：**经常发生

**特殊需求：**无

### 职员提升读者权限

**主要参与者：**职员

**涉众及关注点：**

1. 职员：希望精确快速的修改读者权限，满足读者的请求
2. 读者：希望被更快提升权限

**前置条件：**读者提交升级申请

**主成功场景：**

- 职工通过账号密码登录网站
- 职工例行检视提交申请的读者表格
- 职工查看具体读者信息
- 职工提升符合条件的读者等级

**扩展失败场景：**无

**发生频率：**较少发生

**特殊需求：**无

### 读者查询书籍信息

**主要参与者：**读者

**涉众及关注点：**

1. 读者：希望能够快速准确获取书籍信息

**前置条件：**系统中已经添加了读者的账号

**主成功场景：**

- 读者使用账号密码登录网站（在终端使用读者证录入信息）
- 读者输入需要查询的书籍名/作者等信息
- 系统给出符合条件的书籍列表，包括书籍的详细信息和是否在馆等状态信息
- 读者完成查询，自行选择继续查询或退出系统

**扩展失败场景：**

- 读者的账号不存在或密码错误
- 没有与输入信息相匹配的书籍信息

**发生频率：**经常发生

**特殊需求：**无

## 领域模型

​	在这个系统中共具有6个角色，分别为读者、职员、书籍、读者类型（等级）、图书馆区域（书库）和出版社，他们之间存在如下关系：

- 一个职员可以管理多个读者、书籍和出版社的信息，即职员和读者、书籍和出版社之间都是一对多关系
- 一个读者可以借阅多本书籍，读者和书籍之间也是一对多关系
- 每个读者类型都可能有多个读者，而每个读者只可能处于一种类型中，读者类型和读者之间是一对多关系
- 图书馆每个区域会有若干本书籍，图书馆区域和书籍是一对多关系
- 每个出版社可以出版多本图书，出版社和书籍之间是一对多关系

据此，画出系统的领域模型：
<img src="./assets/library_management.drawio.png" alt="library_management.drawio" style="zoom: 50%;" />

# 架构设计

## 系统架构及原理（根据实现要更改）

本系统采用MVC的设计模式，为了更加清晰地显示其架构图，将model层再细分为两层：Domain层和Foundation层。Domain层主要表示系统的数据模型，Foundation层主要表示系统所使用的数据库类型支持和框架支持。下面是本系统的架构图：

视图层，即View层，是最顶层。负责界面的显示，以及与用户的交互功能，例如表单、网页等，是用户直接接触的一层。使用了XXX框架，为用户提供了简约美观的界面，使用户能够更加方便地使用系统。

控制层，即Controller层，是中间层。负责接收用户的请求，调用模型层处理用户的请求，然后将处理结果返回给用户。可以理解为一个分发器，用来决定对于视图发来的请求，需要用哪一个模型来处理，以及处理完后需要跳回到哪一个视图。即用来连接视图和模型。

领域层，即Domain层，是第三层。存放系统的各个模型数据，

基础层，即Foundation层，是最底层。存放系统所使用的数据库类型支持和框架支持，例如数据库连接、数据库操作等。

## 业务用例的实现

下面我们将介绍本系统涉及的重要业务用例，分别是：图书查询、图书借阅、图书入库、读者管理。

### 图书查询

### 图书借阅

### 图书入库

### 读者管理

## 数据库设计

### ER图

本系统的ER图如下所示：
<img src="./assets/E-R_diagram.png" alt="E-R_diagram" style="zoom:67%;" />

### 数据库关系模式

本系统共有9张数据库表，分别是staff、book_out、book_entering、book、publisher、stack、borrow、reader、reader_type。下面分别对这些表进行介绍。

|     表名      |                说明                |
| :-----------: | :--------------------------------: |
|     staff     |     员工表，用于存储员工的信息     |
|   book_out    |   出库表，用于存储图书出库的信息   |
| book_entering |   入库表，用于存储图书入库的信息   |
|     book      |     图书表，用于存储图书的信息     |
|   publisher   |   出版社表，用于存储出版社的信息   |
|     stack     |     书库表，用于存储书库的信息     |
|    borrow     |     借阅表，用于存储借阅的信息     |
|    reader     |     读者表，用于存储读者的信息     |
|  reader_type  | 读者类型表，用于存储读者类型的信息 |


下面对这些表的字段进行介绍。

<center>职工表</center>

|     字段     |  数据类型   | 主键/外键 |     说明     |
| :----------: | :---------: | :-------: | :----------: |
|   staff_id   |     int     |   主键    |   职工编号   |
|     name     | varchar(40) |           |   职工姓名   |
|     age      |     int     |           |   职工年龄   |
|   id_card    | varchar(18) |           | 职工身份证号 |
| phone_number | varchar(11) |           | 职工电话号码 |
|   address    | varchar(80) |           |   职工住址   |
|   account    | varchar(8)  |           |   职工账号   |
|   password   | varchar(128) |           |   职工密码   |

<center>图书出库表</center>

|   字段   |  数据类型   | 主键/外键 |     说明     |
| :------: | :---------: | :-------: | :----------: |
| book_id  |     int     |   主键    | 出库图书编号 |
| staff_id |     int     |   主键    | 经手职工编号 |
|   date   |    date     |           |   出库日期   |
|  reason  | varchar(20) |           |   出库原因   |

<center>图书入库表</center>

|   字段   |  数据类型   | 主键/外键 |           说明           |
| :------: | :---------: | :-------: | :----------------------: |
| book_id  |     int     |   主键    |       入库图书编号       |
| staff_id |     int     |   主键    |       经手职工编号       |
|   date   |    date     |           |         入库日期         |
|  reason  | varchar(20) |           | 入库原因，也就是书籍来源 |

<center>图书表</center>

|     字段     |  数据类型   | 主键/外键 |                  说明                  |
| :----------: | :---------: | :-------: | :------------------------------------: |
|   book_id    |     int     |   主键    |                图书编号                |
|   stack_id   |     int     |   外键    |            图书所处书库编号            |
| publisherid  |     int     |   外键    |             图书出版社编号             |
|    title     | varchar(40) |           |                图书名称                |
|     type     | varchar(25) |           |                图书类型                |
|    author    | varchar(40) |           |                图书作者                |
| availability |   Boolean   |           |             图书是否被收录             |
|     ISBN     | varchar(13) |           |                图书ISBN                |
|    place     | varchar(40) |           |              图书存放位置              |
|    state     |   Byte(1)   |           | 图书状态，有在馆、借出和流通中三个状态 |

<center>出版社表</center>

|    字段     |  数据类型   | 主键/外键 |    说明    |
| :---------: | :---------: | :-------: | :--------: |
| publisherid |     int     |   主键    | 出版社编号 |
|    name     | varchar(40) |           | 出版社名称 |
|   address   | varchar(80) |           | 出版社地址 |

<center>书库表</center>

|    字段    |  数据类型   | 主键/外键 |     说明     |
| :--------: | :---------: | :-------: | :----------: |
|  stack_id  |     int     |   主键    |   书库编号   |
| stack_name | varchar(25) |           |   书库名称   |
|  location  | varchar(80) |           |   书库位置   |
|  opening   | varchar(40) |           | 书库开放时间 |

<center>借阅表</center>

|   字段    | 数据类型 | 主键/外键 |      说明      |
| :-------: | :------: | :-------: | :------------: |
|  book_id  |   int    |   主键    | 被借阅图书编号 |
| reader_id |   int    |   主键    |  借阅读者编号  |
|   date    |   date   |           |    借阅日期    |
| is_return |   bool   |           |    是否归还    |

<center>读者表</center>

|   字段    |   数据类型   | 主键/外键 |     说明     |
| :-------: | :----------: | :-------: | :----------: |
| reader_id |     int      |   主键    |   读者编号   |
| type_name | varchar(10)  |   外键    |   读者类型   |
|   name    | varchar(40)  |           |   读者姓名   |
|  id_card  | varchar(18)  |           | 读者身份证号 |
|  account  |  varchar(8)  |           |   读者账号   |
| password  | varchar(128) |           |   读者密码   |
|  credit   |     int      |           |  读者信誉值  |

<center>读者类型表</center>

|      字段       |  数据类型   | 主键/外键 |       说明       |
| :-------------: | :---------: | :-------: | :--------------: |
|    type_name    | varchar(10) |   主键    |   读者类型名称   |
| avaibook_number |     int     |           | 同时可借图书数量 |
|      days       |     int     |           |   最长借阅天数   |


## 部署与应用
### 系统部署架构
该图书管理系统采用了B/S架构，即浏览器/服务器架构，用户通过浏览器访问服务器，服务器处理用户的请求并返回结果给用户。本系统基于Flask框架，通过SQLAlchemy进行数据库操作，使用Bootstrap框架进行前端页面设计，使用Jinja2模板引擎进行页面渲染。
### 环境配置
图书管理系统主要依赖库如下：
- flask（网站框架）
- flask-login（用户登录）
- flask-sqlalchemy（数据库交互）
- python-dotenv（环境变量配置）

本系统依赖于Python(>=3.7)，安装Python后，通过pip指令安装依赖。
```shell
pip install -r requirements.txt
```
### 运行
以下操作均在项目根目录下进行。
- 环境变量
    创建`.env`文件，配置环境变量。`SECRET_KEY`为密钥，需要通过随机生成字符串`uuid.uuid4().hex`进行修改，如下所示：
    ```
    SECRET_KEY=dev              # Flask的密钥
    DATABASE_FILE=library.db    # 数据库文件名
    ```
    若需要将项目于生产环境运行，需要将`.flaskenv`文件进行修改
    ```
    FLASK_APP=library_management
    FLASK_ENV=production
    FLASK_DEBUG=0
    ```
- 数据库初始化
    ```shell
    flask init --drop
    ```
    初始化数据库，`-drop`参数表示删除原有数据库，重新创建。
- 初始数据
    ```shell
    flask forge
    ```
    导入初始数据用于测试。
- 管理员注册
    ```shell
    flask admin
    ```
    输入管理员账号密码，即可注册管理员账号。
- 运行
    ```shell
    flask run
    ```
    运行网站，通过访问端口5000即可访问网站，本地可以通过`http://127.0.0.1:5000`访问。
### 部分功能截图
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



