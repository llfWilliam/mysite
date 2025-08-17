from flask import Flask, jsonify, send_from_directory
import os
import time
from flask import request, g
import logging
import json

app = Flask(__name__, static_folder="site", static_url_path="")
BASE_DIR = os.path.dirname(__file__)
SITE_DIR = os.path.join(BASE_DIR, "site")
START_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

logging.basicConfig(
    filename="audit.log",  # 日志文件
    level=logging.INFO,
    format="%(message)s"
)
audit_logger = logging.getLogger("audit")

@app.before_request
def start_timer():
    g.start_time = time.time()

@app.after_request
def log_request(resp):
    duration_ms = int((time.time() - g.start_time) * 1000)
    entry = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "ip": request.remote_addr,
        "method": request.method,
        "path": request.path,
        "status": resp.status_code,
        "duration_ms": duration_ms,
        "user_agent": request.headers.get("User-Agent", "")[:200],
    }
    audit_logger.info(json.dumps(entry, ensure_ascii=False))
    return resp

@app.route("/")
def get_index():
    return send_from_directory(SITE_DIR, "index.html")

@app.route("/logs/admin")
def get_admin_logs():
    """返回管理端日志（简短）"""
    if os.path.exists(ADMIN_LOG):
        with open(ADMIN_LOG, encoding="utf-8") as f:
            lines = f.read().splitlines()                      
            #splitline的意思是按换行符分割成多行
        return jsonify(lines)
    return jsonify([])

@app.route("/logs/debug")
def get_debug_logs():
    """返回完整调试日志（JSON格式字符串数组）"""
    if os.path.exists(DEBUG_LOG):
        with open(DEBUG_LOG, encoding="utf-8") as f:
            lines = f.read().splitlines()
        return jsonify(lines)
    return jsonify([])

@app.route("/admin")
def admin_index():
    return send_from_directory(SITE_DIR, "manage.html")

@app.route("/status")
def get_status():
    """返回服务器状态信息"""
    status_info = {
        "server": "mysite",
        "status": "running",
        "start_time": START_TIME,
        "uptime_seconds": int(time.time() - time.mktime(time.strptime(START_TIME, "%Y-%m-%d %H:%M:%S")))
    }
    return jsonify(status_info)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)