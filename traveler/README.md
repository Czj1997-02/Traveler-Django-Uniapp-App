# 项目搭建
```
pip install -r copy\requirements.txt
pip install copy\mysqlclient-1.4.6-cp37-cp37m-win32.whl
traveler utf8mb4 utf8mb4_general_ci
python manage.py makemigrations
python manage.py migrate
```
## 创建账号
```
python manage.py createsuperuser
```
### 或者使用接口创建账号，指令创建的要补全电话和姓名等信息，不然会因为unique报错
#### 运行
```
python manage.py runserver
```
#### 传入手机号获取注册验证码
```
http://127.0.0.1:8000/rc/
```
#### 使用postman创建用户,顺便测试一下接口
```
http://127.0.0.1:8000/register/
```

```
post请求 form-data
{
    'telephone':'',
    'code':'',
    'username':'',
    'password':'',
    'realname':'',
    'desc':'',
    'first_name':'',
    'last_name':'',
}
{
    "code": 201,
    "msg": "创建成功！",
    "data": {
        "id": 1
    }
}
```
因为为了安全没写权限传值，可以写了一起传，或者去数据库里改

### 配置setting
修改对应数据库

### 基础数据
创建管理员账号后，一定要先执行数据库脚本，不然缺数据无法登陆
copy文件夹内的sql文件