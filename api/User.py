import json,web
from mods import db
class CheckToken:
    def doSomething(self,data):
        if 'token' not in data:
            c=web.ctx.env.get('HTTP_OAMAUTH')
            if not c:
                return json.dumps({"result":-999,"r":"没有登录"})
        else:
            c=data['token']
        if not '{' in c or not '}' in c:
            return json.dumps({"result":-999,"r":"无效C"})
        cj=json.loads(c)
        ret=db.checkToken(db.fastOpenDb(),cj['username'],cj['token'],cj['seed'],1)
        print(ret)
        if ret[0]==0:
            return json.dumps({"result":0,"r":"校验成功","authowner":"admin","authpar":ret[1]})
        else:
            return json.dumps({"result":-999,"r":"token无效"})
class LoginUser:
    def postSomething(self,data):
        if 'username' not in data or 'password' not in data:
            return json.dumps({"result":-999,"r":"没有用户名或密码"})
        c1=db.fastOpenDb()
        c=db.login(c1,data['username'],data['password'])
        if c==0:
            c1=db.fastOpenDb()
            token,seed=db.makeToken(c1,data['username'])
            web.setcookie('oam_auth',json.dumps({"username":data['username'],"seed":seed,"token":token}),60*60*30)
            return json.dumps({"result":0,"r":"登录成功","username":data['username'],"seed":seed,"token":token})
        else:
            return json.dumps({"result":c,"r":"登录失败"})
class UserChangePassword:
    def postSomething(self,data):
        from webapi import getUserName
        username=getUserName()
        if username=="Any":
            return json.dumps({"result":-999,"r":"未知错误"})
        c1=db.fastOpenDb()
        g=db.getPermission(c1,username)
        if g=="*":
            if 'username' not in data or 'password' not in data:
                return json.dumps({"result":-999,"r":"没有用户名或密码"})
            db.insertUser(db.fastOpenDb(),data['username'],data['password'])
            return json.dumps({"result":0,"r":"修改成功"})
        if 'username' not in data or 'oldpassword' not in data or 'newpassword' not in data:
            return json.dumps({"result":-999,"r":"没有用户名或密码"})
        c=db.login(c1,data['username'],data['oldpassword'])
        if c==0:
            db.insertUser(db.fastOpenDb(),data['username'],data['newpassword'])
            if g[0]=="#":
                db.setPermission(c1,data['username'],g[1:])
            return json.dumps({"result":0,"r":"修改成功"})
        else:
            return json.dumps({"result":c,"r":"修改失败"})
class AddUser:
    def postSomething(self,data):
        if 'username' not in data or 'password' not in data:
            return json.dumps({"result":-999,"r":"没有用户名或密码"})
        c1=db.fastOpenDb()
        db.insertUser(c1,data['username'],data['password'])
        return json.dumps({"result":0,"r":"修改成功"})
class SetUserPermission:
    def postSomething(self,data):
        from webapi import getUserName
        username=getUserName()
        if username=="Any":
            return json.dumps({"result":-999,"r":"未知错误"})
        c1=db.fastOpenDb()
        g=db.getPermission(c1,username)
        if "username" not in data:
            db.setPermission(c1,username,data['par'])
            return json.dumps({"result":0,"r":"修改成功"})
        else:
            if data['username']==username:
                db.setPermission(c1,username,data['par'])
                return json.dumps({"result":0,"r":"修改成功"})
            else:
                if g=="*":
                    db.setPermission(c1,data['username'],data['par'])
                    return json.dumps({"result":0,"r":"修改成功"})
                else:
                    return json.dumps({"result":-1,"r":"权限不够"})
class GetUserPermission:
    def doSomething(self,data):
        if "username" not in data:
            json.dumps({"result":-1,"r":"没有用户名"})
        c1=db.fastOpenDb()
        g=db.getPermission(c1,data['username'])
        return json.dumps({"result":0,"r":"ok","username":data['username'],"userPermission":g})
class UserList:
    def doSomething(self,data):
        c1=db.fastOpenDb()
        userList=db.getUserList(c1)
        return json.dumps({"result":0,"r":"ok","userlist":userList})