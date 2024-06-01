import sqlite3,os,random,hashlib,json,sys,time
def printEx(s,f,l):
    s="["+":"+ os.path.basename(f) +":"+ str(l)+"]"+str(s)
    print(s)
    # if not os.path.exists("{0}/log".format(os.path.dirname(os.path.realpath(sys.argv[0])))):
    #     os.mkdir("{0}/log".format(os.path.dirname(os.path.realpath(sys.argv[0]))))
    # fiobj=open("{0}/log/oam_{1}.log".format(os.path.dirname(os.path.realpath(sys.argv[0])),time.strftime("%Y%m%d", time.localtime())),"a+",encoding="utf-8")
    # fiobj.write(s+'\n')
    # fiobj.close
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
def createDb(path):
    if os.path.exists(path):
        os.remove(path)
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('''CREATE TABLE "login" (
  "username" TEXT NOT NULL,
  "phar" TEXT NOT NULL,
  "salt" TEXT NOT NULL
);''')
    c.execute('''CREATE TABLE "var" (
  "var_name" TEXT NOT NULL,
  "var_value" TEXT
);''')
    conn.commit()
    insertUser(conn,"admin","admin")
    conn.close()
def openDb(path):
    if not os.path.exists(path):
        printEx("正在创建数据库...",__file__,"{0}:{1}".format(sys._getframe().f_code.co_name,sys._getframe().f_lineno))
        createDb(path)
        printEx("创建数据库完成...",__file__,"{0}:{1}".format(sys._getframe().f_code.co_name,sys._getframe().f_lineno))
    conn = sqlite3.connect(path)
    return conn
def getVar(conn,varName):
    printEx("获取数据%s..."%(varName),__file__,"{0}:{1}".format(sys._getframe().f_code.co_name,sys._getframe().f_lineno))
    c = conn.cursor()  
    cursor = c.execute('''SELECT "var_name", "var_value"  from "main"."var" where "var_name"='%s' ''' %(varName))
    return cursor.fetchall()
def insertVar(conn,varName,varValue):
    printEx("插入/更改数据%s:%s..."%(varName,varValue),__file__,"{0}:{1}".format(sys._getframe().f_code.co_name,sys._getframe().f_lineno))
    c = conn.cursor()
    c1=getVar(conn,varName)
    if len(c1)>0:
        sql='''UPDATE "main"."var" SET  "var_value" = '{1}' WHERE "var_name" = '{0}';'''.format(varName,varValue)
    else:
        sql='''INSERT INTO "main"."var"("var_name", "var_value") VALUES ('%s', '%s');'''%(varName,varValue)
    #print(sql)
    c.execute(sql)
    conn.commit()
#TODO SALT算法
def salt(username,password):
    salt=''.join(random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/*-+!@#$%^&*()~ ",16))
    phar_ori="!OMA%s%s%sAMO!"%(username,password,salt)
    phar_md5_b=hashlib.sha1(phar_ori.encode('utf-8'))
    phar_md5=phar_md5_b.hexdigest()
    return (phar_md5,salt)
def insertUser(conn,userName,password):
    printEx("插入用户%s..."%(userName),__file__,"{0}:{1}".format(sys._getframe().f_code.co_name,sys._getframe().f_lineno))
    c = conn.cursor()
    phar,salt1=salt(userName,password)
    if len(getSalt(conn,userName))==0:
        c.execute('''INSERT INTO "main"."login"("username", "phar","salt") VALUES ('%s', '%s','%s');'''%(userName,phar,salt1))
    else:
        c.execute('''UPDATE "main"."login" SET  "phar" = '%s' WHERE "username" = '%s';'''%(phar,userName))
        c.execute('''UPDATE "main"."login" SET  "salt" = '%s' WHERE "username" = '%s';'''%(salt1,userName))
    conn.commit()
def getSalt(conn,username):
    c = conn.cursor()  
    cursor = c.execute('''SELECT "salt"  from "main"."login" where "username"='%s' ''' %(username))
    return(cursor.fetchall())
def login(conn,username,password):
    printEx("登入用户%s..."%(username),__file__,"{0}:{1}".format(sys._getframe().f_code.co_name,sys._getframe().f_lineno))
    c = conn.cursor()
    s=getSalt(conn,username)
    if len(s)>0:
        salt=s[0][0]
        phar_ori="!OMA%s%s%sAMO!"%(username,password,salt)
        phar_md5_b=hashlib.sha1(phar_ori.encode('utf-8'))
        phar_md5=phar_md5_b.hexdigest()
        cursor = c.execute('''SELECT "salt"  from "main"."login" where "username"='%s' and "phar"='%s' ''' %(username,phar_md5))
        printEx('''SELECT "salt"  from "main"."login" where "username"='%s' and "phar"='%s' ''' %(username,phar_md5),__file__,"{0}:{1}".format(sys._getframe().f_code.co_name,sys._getframe().f_lineno))
        c2=cursor.fetchall()
        if len(c2)>0:
            printEx("用户存在%s..."%(username),__file__,"{0}:{1}".format(sys._getframe().f_code.co_name,sys._getframe().f_lineno))
            if c2[0][0]==salt:
                printEx("登入确认%s..."%(username),__file__,"{0}:{1}".format(sys._getframe().f_code.co_name,sys._getframe().f_lineno))
                return 0
            else:
                printEx("登入失败%s：SALT值不正确..."%(username),__file__,"{0}:{1}".format(sys._getframe().f_code.co_name,sys._getframe().f_lineno))
                return -1
        else:
            printEx("登入失败%s：用户名或密码错误..."%(username),__file__,"{0}:{1}".format(sys._getframe().f_code.co_name,sys._getframe().f_lineno))
            return -1
    else:
        printEx("登入失败%s：用户不存在..."%(username),__file__,"{0}:{1}".format(sys._getframe().f_code.co_name,sys._getframe().f_lineno))
        return -2
def makeToken(conn,username):
    c = conn.cursor()
    s=getSalt(conn,username)
    seed=''.join(random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",16))
    if len(s)>0:
        salt=s[0][0]
        cursor = c.execute('''SELECT "phar"  from "main"."login" where "username"='%s' ''' %(username))
        phar=cursor.fetchall()[0][0]
        phar_ori="%s!OMA%s%s%sAMO!%s"%(seed,username,phar,salt,seed)
        phar_md5_b=hashlib.sha1(phar_ori.encode('utf-8'))
        phar_md5=phar_md5_b.hexdigest()
        return phar_md5,seed
    else:
        return '',''
def checkToken(conn,username,token,seed,showpar=0):
    c = conn.cursor()
    s=getSalt(conn,username)
    if len(s)>0:
        salt=s[0][0]
        if showpar!=1:
            cursor = c.execute('''SELECT "phar"  from "main"."login" where "username"='%s' ''' %(username))
        else:
            cursor = c.execute('''SELECT "phar","per"  from "main"."login" where "username"='%s' ''' %(username))
        c1=cursor.fetchall()
        phar=c1[0][0]
        print(c1)
        phar_ori="%s!OMA%s%s%sAMO!%s"%(seed,username,phar,salt,seed)
        phar_md5_b=hashlib.sha1(phar_ori.encode('utf-8'))
        phar_md5=phar_md5_b.hexdigest()
        if phar_md5==token:
            if showpar==1:
                return 0,c1[0][1]
            return 0
        else:
            return -1
    else:
        return -1
def changePassword(conn,username,oripassword,newpassword):
    c = conn.cursor()
    s=getSalt(conn,username)
    if len(s)>0:
        salt=s[0][0]
        phar_ori="!OMA%s%s%sAMO!"%(username,oripassword,salt)
        phar_md5_b=hashlib.sha1(phar_ori.encode('utf-8'))
        phar_md5=phar_md5_b.hexdigest()
        cursor = c.execute('''SELECT "salt"  from "main"."login" where "username"='%s' and "phar"='%s' ''' %(username,phar_md5))
        printEx('''SELECT "salt"  from "main"."login" where "username"='%s' and "phar"='%s' ''' %(username,phar_md5),__file__,"{0}:{1}".format(sys._getframe().f_code.co_name,sys._getframe().f_lineno))
        c2=cursor.fetchall()
        if len(c2)<0:
            return -2
        insertUser(conn,username,newpassword)
        return 0
    else:
        return -1
def setPermission(conn,username,permission):
    c = conn.cursor()  
    cursor = c.execute('''SELECT "salt"  from "main"."login" where "username"='%s' ''' %(username))
    c1=cursor.fetchall()
    if(len(c1)>0):
        c.execute('''UPDATE "main"."login" SET  "per" = '%s' WHERE "username" = '%s';'''%(permission,username))
        return 0
    return -1
def getPermission(conn,username):
    c = conn.cursor()  
    cursor = c.execute('''SELECT "salt"  from "main"."login" where "username"='%s' ''' %(username))
    c1=cursor.fetchall()
    if(len(c1)>0):
        cursor = c.execute('''SELECT "per"  from "main"."login" where "username"='%s' ''' %(username))
        c2=cursor.fetchall()
        if(len(c2)>0):
            return c2[0][0]
        else:
            return ""
    return ""
def getUserList(conn):
    c = conn.cursor()  
    cursor = c.execute('''SELECT "username"  from "main"."login" ''')
    c1=cursor.fetchall()
    r=[]
    for cc1 in c1:
        r.append(cc1[0])
    return r
def configJson2dbVar():
    conn=fastOpenDb()
    if os.path.exists('{0}/settings.json'.format(os.path.dirname(os.path.realpath(sys.argv[0])))):
        f=open('{0}/settings.json'.format(os.path.dirname(os.path.realpath(sys.argv[0]))),'r',encoding="utf-8")
        j=f.read()
        j_l=json.loads(j)
        for x in j_l.keys():
            print(x)
            insertVar(conn,x,json.dumps(j_l[x]))
        return True
    else:
        return False
def dbVar2ConfigObj():
    conn=fastOpenDb()
    c = conn.cursor()  
    cursor = c.execute('''SELECT "var_name", "var_value"  from "main"."var" ''')
    r=cursor.fetchall()
    c1={}
    for x in r:
        #print("%s:%s\n"%(x[0],x[1]))
        if x[0]=="docker":
            continue
        if "{" not in x[1] or "}" not in x[1] :
            if not is_number(x[1]):
                c1[x[0]]=x[1]
            else:
                c1[x[0]]=eval(x[1])
        else:
            c1[x[0]]=json.loads(x[1])
    printEx("读取设置完成！",__file__,"{0}:{1}".format(sys._getframe().f_code.co_name,sys._getframe().f_lineno))
    #升级heart->kitty
    if 'kitty' not in c1 and 'heart' in c1:
        c1['kitty']=c1['heart']#转移
        insertVar(conn,'kitty',json.dumps(c1['kitty']))#写入
    return c1
def fastOpenDb():
    return openDb('{0}/settings.db'.format(os.path.dirname(os.path.realpath(sys.argv[0]))))
if __name__ == "__main__":
    openDb('{0}/settings.db'.format(os.path.dirname(os.path.realpath(sys.argv[0]))))
    print("数据库初始化完成")