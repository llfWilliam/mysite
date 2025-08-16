import os
from http.server import ThreadingHTTPServer
from handler import MyHandler, ADMIN_LOG, DEBUG_LOG
from welcome import show_welcome

BASE_DIR = os.path.dirname(__file__)
WEBROOT = os.path.join(BASE_DIR, "site")
os.chdir(WEBROOT)

port_input = input("请输入要使用的端口号（默认8000）：").strip()
port = int(port_input) if port_input else 8000
addr = ("127.0.0.1", port)

open(ADMIN_LOG, "w", encoding="utf-8").close()
httpd = ThreadingHTTPServer(addr, MyHandler)

show_welcome(port)


try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n服务器已手动停止")
    httpd.server_close()