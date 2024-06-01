'''
Date: 2022-03-25 10:10:56
LastEditors: 苏林正
LastEditTime: 2022-03-25 10:12:17
FilePath: \kittyscan-customer/api\VarConfig.py
'''
import json
from mods import db
class InsertVar:
    def postSomething(self,data):
        if 'varname' not in data:
            return json.dumps({"result":-1,"r":"var is invild"})
        if 'vardata' not in data:
            return json.dumps({"result":-1,"r":"var is invild"})
        c1=data['varname']
        c2=data['vardata']
        if c1=="":
            return json.dumps({"result":-1,"r":"var is invild"})
        db.insertVar(db.fastOpenDb(),c1,c2)
        return json.dumps({"result":0,"r":"ok"})
class GetVar:
    def doSomething(self,data):
        if 'varname' not in data:
            return json.dumps({"result":-1,"r":"var is invild"})
        if data['varname']=="":
            return json.dumps({"result":-1,"r":"var is invild"})
        c=db.getVar(db.fastOpenDb(),data['varname'])
        if len(c)==0:
            return json.dumps({"result":-1,"r":"var is invild","varname":data['varname']})
        if c[0][1]=="":
            return json.dumps({"result":-2,"r":"var is empty","varname":data['varname'],"vardata":""})
        else:
            return json.dumps({"result":0,"r":"ok","varname":data['varname'],"vardata":c[0][1]})