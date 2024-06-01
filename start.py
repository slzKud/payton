'''
Date: 2022-06-06 14:22:44
LastEditors: 苏林正
LastEditTime: 2022-06-06 14:23:12
FilePath: \OAM-Kernel\start.py
'''
from mods import g
if __name__ == "__main__":
    import kernel
    g._init()
    #TODO G
    kernel.startServer()