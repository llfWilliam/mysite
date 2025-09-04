from flask import Flask, send_from_directory, request, g
import time
import json
from config import SITE_DIR, audit_logger, admin_logger, VERSION, print_version
from auth import auth_bp
from admin import admin_bp
from logs import logs_bp
from modules.academic.routes import academic_bp

# 创建Flask应用
app = Flask(__name__, static_folder="static", static_url_path="", template_folder="templates")

# 配置session密钥
app.secret_key = 'your-secret-key-here-change-in-production'

# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(academic_bp)

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
    admin_logger.info(f"[{entry['time']}] {entry['method']} {entry['path']} -> {entry['status']} ({entry['duration_ms']}ms)")
    return resp

@app.route("/")
def get_index():
    return send_from_directory(SITE_DIR, "login.html")

@app.route("/index.html")
def get_home():
    return send_from_directory(SITE_DIR, "index.html")

if __name__ == "__main__":
    # 打印版本信息
    print_version()
    print(f"启动 MySite v{VERSION}...")
    app.run(host="127.0.0.1", port=8000, debug=False)