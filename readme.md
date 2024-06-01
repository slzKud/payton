# Payton
一个基于Web.py的轻量化Web框架。支持后台Worker,自定义路由和API。有一个基于SQLite3的用户认证系统。

***这里只是存档，个人开发使用，很多东西都没统一在一起。***

暂时没有完整开发说明（咕咕咕）

命名来自***Liella***的成员Payton尚未。

## 需要的依赖
* web.py
* requests

## 如何运行
* 直接执行start.py即可，然后访问http://127.0.0.1即可。（默认端口在backend.py里面）

## 如何添加API

* 参照api内User.py的写法，执行的URL为/Api/文件名/所添加的类名
### GET
~~~
class Hello:
    def doSomething(self,data):
        return "Hello, Payton."
~~~

### POST
~~~
class Hello:
    def postSomething(self,data):
        return "Hello, Payton."
~~~

## 如何添加Worker
* 参照worker文件夹W.py的写法即可
~~~
class Worker:
    def __init__(self,data=""):
        pass
    def Background(self):
        while 1:
            print("Hello, Payton from worker.")
            time.sleep(1)
~~~

## 用户认证系统
* 参照User.py的代码，用对应的API操作即可。
* 除了User.py的一小部分API以外，所有API都需要登录内执行。白名单在webapi.py内。
* 框架第一次运行的时候会自动生成数据库，默认用户是**admin**/**admin**