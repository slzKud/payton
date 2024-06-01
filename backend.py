'''
Date: 2022-01-17 10:52:11
LastEditors: 苏林正
LastEditTime: 2022-06-06 09:55:38
FilePath: \OAM-Kernel\backend.py
'''
import web,os,sys
from WebLog import Log
from webapi import api
class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0',port))
urls = (
    '/hello/(.*)', 'hello',
    '/Api/(.*)/(.*)', 'api',
    '/','index',
    '(.*\..{1,4})','staticFile'

)
app = MyApplication(urls, globals())

class hello:
    def GET(self, name):
        if not name:
            name = 'World'
        return 'Hello, ' + name + '!'
class index:
    def GET(self):
        web.seeother('/index.html'); #重定向
class apifake:
    def GET(self,d,a):
        return "It isn't OAM!"
    def POST(self,d,a):
        return "It isn't OAM!"
class staticFile:
    def GET(self, file):
        try:
            f = open(os.path.dirname(os.path.realpath(sys.argv[0]))+'/static'+file,'rb')
            return f.read()
        except:
            web.ctx.status='404 Not Found'
            return 'File Not Found' # you can send an 404 error here if you want
def stopServer():
    global app
    app.stop()
def startServer():
    print('HTTP SERVER START\n')
    global app
    app.run(80,Log)
if __name__ == "__main__":
    app.run(80,Log)