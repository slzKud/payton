'''
Date: 2022-06-06 14:17:55
LastEditors: 苏林正
LastEditTime: 2022-06-15 10:06:20
FilePath: \OAM-Kernel\kernel.py
'''
import sys,time,os
import threading,queue,json
import backend
from mods import g
class re_Text():
    def __init__(self, queue):
        self.terminal = sys.stdout
        self.queue = queue
    def write(self, content):
        s="["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]"+str(content)
        if content=='\n' or content==' ' or content=='\t':
            s=content
        self.terminal.write(s)
        self.queue.put(s)
        if not os.path.exists("{0}/log".format(os.path.dirname(os.path.realpath(sys.argv[0])))):
            os.mkdir("{0}/log".format(os.path.dirname(os.path.realpath(sys.argv[0]))))
        fiobj=open("{0}/log/kernel_{1}.log".format(os.path.dirname(os.path.realpath(sys.argv[0])),time.strftime("%Y%m%d", time.localtime())),"a+",encoding="utf-8")
        fiobj.write(s)
        fiobj.close
    def flush(self):
        pass
class WorkerLoader():
    def __init__(self):
        import os
        a=[]
        if not os.path.exists("{0}/worker".format(os.path.dirname(os.path.realpath(sys.argv[0])))):
            return False
        dirs=os.listdir("{0}/worker".format(os.path.dirname(os.path.realpath(sys.argv[0]))))
        for file in dirs:
            if ".py" in file:
                a.append(file)
        self.fileList=a
    def LoadTask(self,modelA,data=""):
        import importlib,traceback
        try:
            model = importlib.import_module("worker.%s" % modelA)
            api_class = getattr(model, "Worker")
            api_instance = api_class(data)
            # return api_instance.doSomething(data)
            T=threading.Thread(target=api_instance.Background, args=(),name="Worker_%s"%(modelA))
            T.start()
            return True
        except Exception as e:
            print("\nPOOL!\nTask:%s\nError:%s\nTrace:%s"%(modelA,str(e),traceback.format_exc()))
            return False
    def LoadConfig(self):
        #读取Config
        if os.path.exists('{0}/config.json'.format(os.path.dirname(os.path.realpath(sys.argv[0])))):
            a=open('{0}/config.json'.format(os.path.dirname(os.path.realpath(sys.argv[0]))),"r")
            try:
                b=json.loads(a.read())
                return b
            except:
                return {}
        return {}
    def startLoader(self):
        a=self.LoadConfig()
        for file in self.fileList:
            if self.LoadTask(file.replace('.py',''),a):
                print("Model:%s,OK"%(file))
            else:
                print("Model:%s,FAIL"%(file))
def creatCUI():
    msg_queue = queue.Queue()
    sys.stdout = re_Text(msg_queue)
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExit Server...Wait!Press Ctrl+C again to close force.")
        backend.stopServer()
        g.set_value("g_fsd_restartFlag",0)
        g_fsd_deamon=g.get_value("g_fsd_deamon")
        g_fsd_deamon.kill()
        sys.exit(0)
def startServer():
    T = threading.Thread(target=backend.startServer, args=())
    T.start()
    A=WorkerLoader()
    A.startLoader()
    creatCUI()