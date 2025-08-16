from flask import Flask, jsonify, send_from_directory
from handler import ADMIN_LOG, DEBUG_LOG
import os
import time
from flask_cors import CORS

app = Flask(__name__, static_folder="site", static_url_path="")

BASE_DIR = os.path.dirname(__file__)
SITE_DIR = os.path.join(BASE_DIR, "site")

START_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

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
    # 本地开发用；上线请换 WSGI 服务器（如 waitress-serve）
    app.run(host="127.0.0.1", port=8000, debug=False)