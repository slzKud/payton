'''
Date: 2022-03-24 10:22:08
LastEditors: 苏林正
LastEditTime: 2022-11-22 22:22:40
FilePath: \payton-cn\webapi.py
'''
import importlib,web,json
import traceback
from mods import db
class api:
    def __init__(self) -> None:
        self.apiWhiteList=["User/CheckToken","User/LoginUser","fsdCert/UserList"]
        self.apiPremissionList={"User/AddUser":"5",
                                "User/SetUserPermission":"5",
                                "User/GetUserPermission":"5",
                                "User/UserList":"5",
                                "VarConfig/InsertVar":"6"
                                }
    def GET(self, d,a):
        web.header('Access-Control-Allow-Origin','*')
        print("%s/%s\n" %(d,a))
        data=web.input()
        if "%s/%s" %(d,a) not in self.apiWhiteList:
            if web.ctx.env.get('HTTP_OAMAUTH')!=None:
                print(web.ctx.env.get('HTTP_OAMAUTH'))
                auth=web.ctx.env.get('HTTP_OAMAUTH')
                if "{" not in auth or "}" not in auth:
                    web.ctx.status='500 Internal Server Error'
                    return 'OAM_AUTH invild'
                auth_j=json.loads(auth)
                c=db.checkToken(db.fastOpenDb(),auth_j['username'],auth_j['token'],auth_j['seed'],1)
                if c[0]!=0:
                    web.ctx.status='401 Unauthorized'
                    return json.dumps({"result":-9999,"r":"没有认证，请登录"})
                if c[1]!="*":
                    if "%s/%s" %(d,a) in self.apiPremissionList:
                        if "%s,"%(self.apiPremissionList["%s/%s" %(d,a)]) not in c[1]:
                            web.ctx.status='401 Unauthorized'
                            return json.dumps({"result":-9999,"r":"没有对应的权限，请联系管理员或更换用户"})
            else:
                web.ctx.status='401 Unauthorized'
                return json.dumps({"result":-9999,"r":"没有认证，请登录"})
        if not d:
            web.ctx.status='500 Internal Server Error'
            return 'doType Not Found'
        if not a:
            web.ctx.status='500 Internal Server Error'
            return 'actionName Not Found'
        try:
            model = importlib.import_module("api.%s" % d)
            api_class = getattr(model, a)
            api_instance = api_class()
            return api_instance.doSomething(data)
        except Exception as e:
            web.ctx.status='500 Internal Server Error'
            return "Get!Error Not Found:%s/%s:%s\n%s"%(d,a,str(e),traceback.format_exc())
    def POST(self,d,a):
        web.header('Access-Control-Allow-Origin','*')
        print("%s/%s\n" %(d,a))
        data=web.input()
        if "%s/%s" %(d,a) not in self.apiWhiteList:
            if web.ctx.env.get('HTTP_OAMAUTH')!=None:
                print(web.ctx.env.get('HTTP_OAMAUTH'))
                auth=web.ctx.env.get('HTTP_OAMAUTH')
                if "{" not in auth or "}" not in auth:
                    web.ctx.status='500 Internal Server Error'
                    return 'OAM_AUTH invild'
                auth_j=json.loads(auth)
                c=db.checkToken(db.fastOpenDb(),auth_j['username'],auth_j['token'],auth_j['seed'],1)
                if c[0]!=0:
                    web.ctx.status='401 Unauthorized'
                    return json.dumps({"result":-9999,"r":"没有认证，请登录"})
                if c[1]!="*":
                    if "%s/%s" %(d,a) in self.apiPremissionList:
                        if "%s,"%(self.apiPremissionList["%s/%s" %(d,a)]) not in c[1]:
                            web.ctx.status='401 Unauthorized'
                            return json.dumps({"result":-9999,"r":"没有对应的权限，请联系管理员或更换用户"})
            else:
                web.ctx.status='401 Unauthorized'
                return json.dumps({"result":-9999,"r":"没有认证，请登录"})
        if not d:
            web.ctx.status='500 Internal Server Error'
            return 'doType Not Found'
        if not a:
            web.ctx.status='500 Internal Server Error'
            return 'actionName Not Found'
        try:
            model = importlib.import_module("api.%s" % d)
            api_class = getattr(model, a)
            api_instance = api_class()
            return api_instance.postSomething(data)
        except Exception as e:
            web.ctx.status='500 Internal Server Error'
            return "Get!Error Not Found:%s/%s:%s\n%s"%(d,a,str(e),traceback.format_exc())
    def OPTIONS(self,d,a):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Headers',  'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods,OAMAuth')
        web.header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
class index:
    def GET(self):
        web.seeother('/index.html'); #重定向
def getUserName():
    try:
        if web.ctx.env.get('HTTP_OAMAUTH')!=None:
            auth=web.ctx.env.get('HTTP_OAMAUTH')
            if "{" not in auth or "}" not in auth:
                return "Any"
            auth_j=json.loads(auth)
            return auth_j['username']
        else:
            return "Any"
    except:
        return "Any"