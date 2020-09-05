# 个人博客系统（personal-blog）

## 目录

- [配置中心](#配置中心)
- [本地运行](#本地运行)
  - [系统环境](#系统环境)
  - [本地安装](#本地安装)
  - [本地启动](#本地启动)
  - [单元测试](#单元测试)
- [Docker部署](#Docker部署)


## 本地运行

### 系统环境

* SQLite 或者 MySQL 5.6或以上版本 
* Python 3.7 以上版本

### 本地安装

#### Linux环境

* virtualenv安装并创建虚拟环境
```sh
$ pip install virtualenv
$ virtualenv -p /usr/bin/python3.7 .env
```

* blog服务依赖库安装
```sh
* 激活虚拟环境
$ source .env/bin/activate
* 安装依赖库
$ pip install -r build/requirements.txt
```

* 设置服务依赖变量
```sh

$ export DEBUG=true
```

* 配置数据库
```sh
修改目录 blog/setting.py 文件的以下内容:
DATABASES = {
    
    'default': {

        'ENGINE': 'django.db.backends.mysql',

        'NAME': 'blog',         #你的数据库名称

        'USER': 'root',         #你的数据库用户名

        'PASSWORD': '123456',   #你的数据库密码

        'HOST': '',             #你的数据库主机，留空默认为localhost

        'PORT': '3306',         #你的数据库端口

    }
}
```

* 初始化数据库并导入数据
```sh
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py loaddata build/blog_db.json
```

* 创建超级用户
```sh
$ python manage.py createsuperuser
```

#### Windows环境

* virtualenv安装并创建虚拟环境
```sh
pip install virtualenv
virtualenv -p python3.7 .env 或 virtualenv -p 你的安装路径/python3.7 .env
```

* blog服务依赖库安装
```sh
* 激活虚拟环境
 .env/Scripts/activate 或 cd .env/Scripts/ 下输入activate
* 安装依赖库
 pip install -r build/requirements.txt
```

* 设置服务依赖变量
```sh
set DEBUG=true
```

* 配置数据库
```sh
修改目录 blog/setting.py 文件的以下内容:
DATABASES = {
    
    'default': {

        'ENGINE': 'django.db.backends.mysql',

        'NAME': 'blog',         #你的数据库名称

        'USER': 'root',         #你的数据库用户名

        'PASSWORD': '123456',   #你的数据库密码

        'HOST': '',             #你的数据库主机，留空默认为localhost

        'PORT': '3306',         #你的数据库端口

    }
}
```

* 初始化数据库并导入数据
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata build/blog_db.json
```

* 创建超级用户
```sh
python manage.py createsuperuser
```

### 本地启动

* Linux 80端口本地启动服务

```sh
$ source .env/bin/activate
$ python manage.py runserver 0:80
```

* Windows 80端口本地启动服务

```sh
cd .env/Scripts/ 下输入activate
python manage.py runserver 0:80
```

详细接口说明和调试请查看[Editor Swagger](/docs/editor_v1.yaml)或[智能语音应用服务详细设计说明书](/docs/智能语音应用服务详细设计说明书.docx)

## 单元测试

```sh
$ python manage.py test 
```

## Docker部署

* 镜像构建

```sh
# 按照版本替换tag_version
$ docker build -t personal-blog:tag_version .
```

* docker-compose.yaml

```yaml
version: '3'
services:
  Blog:
    image: personal-blog:tag_version
    restart: 'no'
    ports:
      - 80:80
    environment:
      - DEBUG: True
    # 如果使用sqlite，需要挂在数据目录
    volumes:
      - ./data:/app/data
```

* 服务启动
```bash
$ docker-compose up -d
```

* 导入配置
```bash
# 进入容器
$ docker-compose exec Blog bash
# 容器内执行
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py loaddata build/blog_db.json
$ python manage.py createsuperuser
$ python manage.py runserver 0:80
```