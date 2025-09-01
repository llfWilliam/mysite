from flask import Flask, jsonify, send_from_directory
import os
import time
from flask import request, g
import logging
import json
import mysql.connector

app = Flask(__name__, static_folder="static", static_url_path="")       #把flask服务拉起来

#开始定义文件路径
BASE_DIR = os.path.dirname(__file__)
SITE_DIR = os.path.join(BASE_DIR, "static")
START_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 从环境变量里读取数据库配置
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "3307")),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),                      #getenv的意思就是取系统环境变量，在高级系统设置里面改就行，这样安全一点
    database=os.getenv("DB_NAME", "mysite")
)
cursor = db.cursor(dictionary=True)             
#建立一个“游标”对象，用来执行 SQL，
#dictionary=True 表示查询结果会变成字典形式（键=字段名），比元组好用。


#写下管理员日志和普通日志的变量方便管理
ADMIN_LOG = "admin.log"
DEBUG_LOG = "audit.log"

#每次打开都会清空管理员日志，方便前端管理
open("admin.log", "w").close()          #每次启动服务器都要清空管理员日志

#利用标准日志函数来处理普通日志，注意，标准日志函数全局只能调用一次
logging.basicConfig(
    filename=DEBUG_LOG,  # 默认所有日志写到 audit.log 文件里。
    level=logging.INFO,     #设置日志等级，只有 INFO 及以上的日志会被写进去
    format="%(message)s"    #日志的格式，这里只写消息本身，不加时间、等级等前缀。
)
audit_logger = logging.getLogger("audit")
#logging.getLogger(name) 可以拿到一个“命名 logger”。
#如果名字一样，拿到的是同一个 logger；名字不一样，就相当于新建。
admin_logger = logging.getLogger("admin")
admin_handler = logging.FileHandler(ADMIN_LOG, encoding="utf-8")  
admin_logger.addHandler(admin_handler)
admin_logger.setLevel(logging.INFO)

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

@app.route("/logs/admin")
def get_admin_logs():
    """返回管理端日志（简短）"""
    # 检查是否有管理员权限
    if request.cookies.get('admin_auth') != 'true':
        return jsonify({"error": "无权限访问管理日志"}), 403
        
    if os.path.exists(ADMIN_LOG):
        with open(ADMIN_LOG, encoding="utf-8") as f:
            lines = f.read().splitlines()                      
            #splitline的意思是按换行符分割成多行
        return jsonify(lines)
    return jsonify([])

@app.route("/logs/debug")
def get_debug_logs():
    """返回完整调试日志（JSON格式字符串数组）"""
    # 检查是否有管理员权限
    if request.cookies.get('admin_auth') != 'true':
        return jsonify({"error": "无权限访问调试日志"}), 403
        
    if os.path.exists(DEBUG_LOG):
        with open(DEBUG_LOG, encoding="utf-8") as f:
            lines = f.read().splitlines()
        return jsonify(lines)
    return jsonify([])

@app.route("/admin")
def admin_index():
    # 检查是否有管理员权限
    if request.cookies.get('admin_auth') != 'true':
        return jsonify({"error": "无权限访问管理页面"}), 403
    return send_from_directory(SITE_DIR, "admin.html")

@app.route("/status")
def get_status():
    """返回服务器状态信息"""
    # 检查是否有管理员权限
    if request.cookies.get('admin_auth') != 'true':
        return jsonify({"error": "无权限访问服务器状态"}), 403
        
    status_info = {
        "server": "mysite",
        "status": "running",
        "start_time": START_TIME,
        "uptime_seconds": int(time.time() - time.mktime(time.strptime(START_TIME, "%Y-%m-%d %H:%M:%S")))
    }
    return jsonify(status_info)

@app.route("/register", methods=["POST"])
def register():
    """注册接口"""
    data = request.json                     #解析前端发过来的json数据
    username = data.get("username")
    password = data.get("password")

    # 判断是否已存在
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():                   #如果有结果被取出
        return jsonify({"success": False, "message": "账号已存在"})

    # 插入数据库
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    db.commit()
    return jsonify({"success": True, "message": "注册成功"})

    # 登录接口
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:                                #如果有结果被取出
        response = jsonify({"success": True, "message": "登录成功", "is_admin": user.get("is_admin", 0) == 1})
        
        # 检查是否是管理员用户
        is_admin = user.get("is_admin", 0) == 1
        if is_admin:
            response.set_cookie('admin_auth', 'true', httponly=True, secure=True)
            
        return response
    else:
        return jsonify({"success": False, "message": "账号或密码错误"})

@app.route("/admin/grant", methods=["POST"])
def grant_admin():
    """授予管理员权限接口"""
    # 检查当前用户是否有管理员权限
    if request.cookies.get('admin_auth') != 'true':
        return jsonify({"error": "无权限执行此操作"}), 403
        
    data = request.json
    username = data.get("username")
    
    if not username:
        return jsonify({"success": False, "message": "用户名不能为空"})
    
    # 检查用户是否存在
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"success": False, "message": "用户不存在"})
    
    # 更新用户为管理员
    try:
        cursor.execute("UPDATE users SET is_admin = 1 WHERE username = %s", (username,))
        db.commit()
        return jsonify({"success": True, "message": f"已成功将 {username} 设置为管理员"})
    except Exception as e:
        db.rollback()
        return jsonify({"success": False, "message": f"设置管理员失败: {str(e)}"})

@app.route("/admin/revoke", methods=["POST"])
def revoke_admin():
    """撤销管理员权限接口"""
    # 检查当前用户是否有管理员权限
    if request.cookies.get('admin_auth') != 'true':
        return jsonify({"error": "无权限执行此操作"}), 403
        
    data = request.json
    username = data.get("username")
    
    if not username:
        return jsonify({"success": False, "message": "用户名不能为空"})
    
    # 检查用户是否存在
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"success": False, "message": "用户不存在"})
    
    # 撤销用户的管理员权限
    try:
        cursor.execute("UPDATE users SET is_admin = 0 WHERE username = %s", (username,))
        db.commit()
        return jsonify({"success": True, "message": f"已成功撤销 {username} 的管理员权限"})
    except Exception as e:
        db.rollback()
        return jsonify({"success": False, "message": f"撤销管理员权限失败: {str(e)}"})

@app.route("/admin/list", methods=["GET"])
def list_users():
    """列出所有用户及其管理员状态"""
    # 检查当前用户是否有管理员权限
    if request.cookies.get('admin_auth') != 'true':
        return jsonify({"error": "无权限执行此操作"}), 403
    
    try:
        cursor.execute("SELECT username, is_admin FROM users")
        users = cursor.fetchall()
        return jsonify({"success": True, "users": users})
    except Exception as e:
        return jsonify({"success": False, "message": f"获取用户列表失败: {str(e)}"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)