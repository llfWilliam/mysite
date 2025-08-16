from http.server import SimpleHTTPRequestHandler
from message import mymessage
import os
import json
HANDLER_PATH = os.path.abspath(__file__)
# 项目根目录 (mysite)
BASE_DIR = os.path.dirname(HANDLER_PATH)
# logs 目录
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
# 绝对路径日志文件
ADMIN_LOG = os.path.join(LOG_DIR, "admin.log")
DEBUG_LOG = os.path.join(LOG_DIR, "server.log")
class MyHandler(SimpleHTTPRequestHandler):                 #继承了他的类
    def log_message(self, format, *args):
        # 生成结构化日志
        log_json = mymessage(
            category="访问日志",            # 日志类型
            event="http请求",             # 事件类型
            number=self.server.server_port,   # 端口
            detail=f"{self.client_address[0]} 请求 {self.path}",  # 访问详情
            more_detail=f"状态: {args[1]}, 消息: {args[0]}"        # 状态和请求行
        )
        msg = json.loads(log_json)
        # 管理端日志（简短）
        short_log = f"[{msg['time']}] {msg['detail']} - {msg['more_detail']}"
        with open(ADMIN_LOG, "a", encoding="utf-8") as f:
            f.write(short_log + "\n")
        # 追加写入日志文件
        with open(DEBUG_LOG, "a", encoding="utf-8") as f:
            f.write(log_json + "\n")
    def handle(self):
        try:
            super().handle()
        except ConnectionAbortedError:
            # 忽略 WinError 10053
            pass