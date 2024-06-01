'''
Date: 2022-06-08 09:35:07
LastEditors: 苏林正
LastEditTime: 2022-06-17 14:03:04
FilePath: \OAM-Kernel\mods\tools.py
'''
def execCmd(cmd):
    import subprocess
    #print('执行命令{0}'.format(cmd))
    '''
    r = os.popen(cmd)
    text = r.read()
    r.close()
    '''
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)  
    out,err = p.communicate()  
    return out.decode()