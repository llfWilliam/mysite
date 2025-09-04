from flask import Blueprint, jsonify, request, session, redirect, url_for
from functools import wraps
from config import cursor, db

# 创建认证蓝图
auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查session中是否有用户信息
        if 'user_id' not in session:
            # 如果是API请求，返回JSON错误
            if request.path.startswith('/api/'):
                return jsonify({'success': False, 'message': '请先登录'}), 401
            # 否则重定向到登录页面
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

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
        # 设置session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['is_admin'] = user.get("is_admin", 0) == 1
        
        response = jsonify({"success": True, "message": "登录成功", "is_admin": user.get("is_admin", 0) == 1})
        
        # 检查是否是管理员用户
        is_admin = user.get("is_admin", 0) == 1
        if is_admin:
            response.set_cookie('admin_auth', 'true', httponly=True, secure=True)
            
        return response
    else:
        return jsonify({"success": False, "message": "账号或密码错误"})

@auth_bp.route("/logout", methods=["POST"])
def logout():
    """登出接口"""
    session.clear()
    response = jsonify({"success": True, "message": "登出成功"})
    response.set_cookie('admin_auth', '', expires=0)
    return response