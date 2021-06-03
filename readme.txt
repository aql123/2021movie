
项目介绍：
本推荐系统采用的是分层模型设计思想，第一层为前端页面模型设计，注重为实现页面的展示效果，主用的编程语言为JavaScript,和前端主流框架bootstrap。
第二层为后端模型设计，编程语言选了简单易懂的python，用Django作为后端框架进行开发，此框架是python web系统开发的首选框架，简单易用。
第三层为算法的设计与实现的逻辑，用协同过滤算法来实现，第四层为数据库表的设计，用SQLite数据库。
本系统web端的功能模块，主要实现影片显示、影片分类显示、热门影片排序显示、收藏影片排序显示、时间排序显示、评分排序显示、算法推荐、影片搜索、影片信息管理等功能，并进行数据库的详细设计，完成设计阶段的各项功能，并对此系统进行功能测试，最后，系统进行相关的实际应用操作，通过系统的使用，用户进入电影推荐系统，此系统可以根据用户对电影所打的标签行为，给用户推荐用户所感兴趣的电影，准确率在百分之75左右，用户可以查看信息，观看影片，给影片评分等操作，本系统基本上完成了预期的基本功能。

电影推荐系统运行说明书
安装运行方法
1.解压项目，解压的文件夹目录下有movie，用pycharm打开movie目录。
2.在pycharm配置python解释器，3.7及以下都可以。可以通过conda或者其他的虚拟环境来安装。
3.打开终端 输入pip install -r requirements.txt 若提示无pip。去下载get-pip.py 运行python get-pip.py
4.安装成功后， 使用pip list 查看已经安装好的package，和requirements.txt中的进行对比，确认安装无误。
有两种运行方法:
1.通过命令行/cmd运行: python manage.py runserver
2.通过Pycharm专业版配置运行，右上角选中movie，一键运行，第一次运行时间可能比较长，因为需要将item_recommend的相似矩阵计算出来。将模型保存到本地。
技术介绍：
前端: bootstrap3 + js+ jquery
后端: django 2.2.1 +  django--rest-framework  (MVC框架)
数据库: sqlite3
算法:协同过滤推荐算法
豆瓣数据集
通过爬虫去抓取豆瓣电影网站的电影信息，带有图片
id,title ,image-link ,country ,years ,director-description,leader,star ,
description,alltags,imdb,language,time-length
电影数量: 2250
功能介绍：
电影展示，标签分类，详情介绍，电影搜索
用户的登录，注册，修改信息
用户对电影的打分，收藏，评论
基于user和Item的协同过滤推荐算法
后台管理系统

算法简介
冷启动问题解决
推荐值: 相似度*评分 根据用户点赞过得商品来寻找相似度推荐。计算每个点赞过的物品和所有未点赞物品之间的得分。得分=相似度*打分值分越高表示越相似。 然后返回结果。
项目文件介绍
media/ 静态文件存放处，图片
movie/ Django的默认app，负责设置的配置还有url路由,部署等功能
static/ css文件和js文件的存放处
user/ 主app，程序的所有代码基本都在这下面 user/migrations为自动生成的数据库迁移文件 user/templates为前端页面模板文件， user/admins.py 为管理员后台代码 user/forms.py为前端表单代码 user/models.py为数据库orm模型 user/serializers.py为restful文件，不用管。 user/urls为路由注册文件。 user/views为负责处理前端请求和与后端数据库交互的模块，也就是controller模块。
cache_keys.py为缓存的key值名称存放文件，不用管。
db.sqlite3数据库文件
douban_crawler.py 豆瓣爬虫文件
manage.py 运行的主程序，从这里启动
Populate movies script.py 填充电影数据到数据库中
Populate user rate.py 随机生成用户评分
recommend_movies.py为推荐算法的部分
model: recommend模型存放的位置
后台管理
通过创建管理员进入后台，已经自带管理员用户名和密码均为admins。
同时可以通过 python manage.py createsuperuser 在终端交互输入用户名和密码即可
创建超级管理员, (密码输入时终端暂时显示)
进入后台: 127.0.0.1:8000/admin

三、各功能代码位置介绍：
标签分类: 数据库设计Movie通过外键关联Tags表，
电影搜索: 在views.py search方法中。通过电影名，导演名，介绍去进行关键字搜索。
后台管理: 通过django自带的admin后台加插件 在admins.py中注册数据库模型
两种推荐算法: 都在recommend_movies.py文件中。
推荐显示的代码:
前端: items.html
后端: views.py中 388行 user_recommend 传递数据到前端template
算法：recommend_movies.py。
依赖包和框架版本
(venv) E:\2021movie>pip list
Package             Version
aiohttp             3.7.4.
asgiref             3.3.4
async-timeout       3.0.1
attrs               21.2.0
beautifulsoup4      4.9.3
bs4                 0.0.1
certifi             2020.12.5
chardet             4.0.0
crawler             0.0.2
Django              2.2.10
django-simpleui     2.1
djangorestframework 3.9.1
greenlet            1.1.0
idna                2.10
idna-ssl            1.1.0
importlib-metadata  4.0.1
lxml                4.6.3
multidict           5.1.0
