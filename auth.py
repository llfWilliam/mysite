from flask import Blueprint, jsonify, request
from config import cursor, db

# 创建认证蓝图
auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """注册接口"""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # 判断是否已存在
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify({"success": False, "message": "账号已存在"})

    # 插入数据库
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    db.commit()
    return jsonify({"success": True, "message": "注册成功"})

@auth_bp.route("/login", methods=["POST"])
def login():
    """登录接口"""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        response = jsonify({"success": True, "message": "登录成功", "is_admin": user.get("is_admin", 0) == 1})
        
        # 检查是否是管理员用户
        is_admin = user.get("is_admin", 0) == 1
        if is_admin:
            response.set_cookie('admin_auth', 'true', httponly=True, secure=True)
            
        return response
    else:
        return jsonify({"success": False, "message": "账号或密码错误"})