## 开发环境搭建

### 创建开发环境的基本步骤

* 拉代码
```bash
git pull git@gitlab.gizwits.com:goms/client.git goms_client
```
我比较喜欢把目录名字改成 __goms_client__

* 开发机器上安装 Python 3.8 版本（Mac）
```bash
brew install python@3.8
```

* 创建一个项目专用的 Virtual Environment
```bash
cd goms_client

python3.8 -m venv venv_3_8_client
```
__venv_3_8_client__ 这个目录名字的确比较长了，不过当你有多个项目的时候，清楚的判断当前环境避免犯浑很重要。你也可以改名字，不管什么名字，用 __venv__ 开头就好了。

* 激活这一虚拟环境
```bash
source venv_3_8_client/bin/activate
```

* 安装软件包
```bash
pip install -r requirements/dev.txt
```

### 准备测试

* 创建一个测试配置文件
```bash
touch .env_test
```

* 文件里面放入如下环境变量
```bash
export XSY_CLIENT_SECRET=f6e*********************
export XSY_PASSWORD=gpt************
export XSY_HOST=https://api.xiaoshouyi.com
export XSY_REDIRECT_URI=https://cc8b18f2.ngrok.io/authorize/
export XSY_CLIENT_ID=49dd2****************
export XSY_USERNAME=gpt@gizwits.com
export MYSQL_DATABASE_URL=sqlite:///db.sqlite3
```

* 引入上面的环境变量
```bash
source .env_test
```

* 执行数据库更新
```bash
python manage.py makemigrations
python manage.py migrate
```

* 执行测试
```bash
pytest
```

## 部署服务

### 环境变量

| 变量名称           | 类型   | 默认值               | 样例                                | 说明                                                         |
| ------------------ | ------ | -------------------- | ----------------------------------- | ------------------------------------------------------------ |
| DEBUG              | bool   | False                | 'True'                              | 是否以 “调试模式” 运行服务，生产环境必须将其设置为 'False'，默认不配置该变量即可。`QA` 环境，可以配置为 'True' |
| MYSQL_DATABASE_URL | string | sqlite:///db.sqlite3 | mysql://root:root@mysql/goms_client | MySQL 数据库的配置地址。配置该链接方式前，请确保已经创建了 UTF-8 编码的数据库（SQLite 可以忽略）。 |
| XSY_HOST           | string |                      | https://api.xiaoshouyi.com          | 销售易的访问域名                                             |
| XSY_CLIENT_ID      | string |                      | 49ddxxxxxxxxxxxxxxxxxxxxxxxx64e3    | client ID                                                    |
| XSY_CLIENT_SECRET  | string |                      | f6e6xxxxxxxxxxxxxxxxxxxxxxxx8d65    | client secret                                                |
| XSY_REDIRECT_URI   | string |                      | https://xxx.gizwits.com/authorize/  | 回访地址                                                     |
| XSY_USERNAME       | string |                      | xxx@gizwits.com                     | 销售易的账号，需要有访问客户和订单以及订单详细的权限         |
| XSY_PASSWORD       | string |                      | xxx123xxxYpuxxx                     | 格式：密码 + 令牌                                            |

### 部署须知

#### 定时任务
本服务含有定时任务(crontab)，任务定义在 `Dockerfile` 中：
```bash
0 * * * * python /app/manage.py reload_xsy_client >> /data/reload_xsy_client.log
10 * * * * python /app/manage.py reload_xsy_order >> /data/reload_xsy_order.log
30 * * * * python /app/manage.py reload_org_device_amount >> /data/reload_org_device_amount.log
```

执行的主要任务有：
1. 拉取销售易的客户信息（增量）
2. 拉取销售易的订单列表（增量）
3. 读取新增的设备新增数量

需要特别说明第 `3` 个任务：
该任务的实现，由运维从各个生成环境（美东、欧洲、国内）导出设备下的Mac 列表，并传输到指定目录中。
Docker 容器通过 volumes 的方式，将该目录下的文件，连接到 /app/global_data 下
定时任务，会定时读取该目录，导入数据，并删除文件