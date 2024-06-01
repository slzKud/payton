'''
Date: 2022-01-17 10:50:13
LastEditors: 苏林正
LastEditTime: 2022-03-24 10:24:11
FilePath: \kittyscan-customer\WebLog.py
'''

from  web.httpserver import LogMiddleware
class Log(LogMiddleware):
    def log(self, status, environ):
        req = environ.get("PATH_INFO", "_")
        protocol = environ.get("ACTUAL_SERVER_PROTOCOL", "-")
        method = environ.get("REQUEST_METHOD", "-")
        host = "%s:%s" % (
            environ.get("REMOTE_ADDR", "-"),
            environ.get("REMOTE_PORT", "-"),
        )

        time = self.log_date_time_string()

        msg = self.format % (host, time, protocol, method, req, status)
        print(msg)
        #printWeb(msg)
        return 0
