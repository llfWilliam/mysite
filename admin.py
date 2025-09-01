from flask import Blueprint, jsonify, request, send_from_directory
from config import cursor, db, SITE_DIR

# 创建管理员蓝图
admin_bp = Blueprint('admin', __name__)

def check_admin_auth():
    """检查管理员权限"""
    return request.cookies.get('admin_auth') == 'true'

@admin_bp.route("/admin")
def admin_index():
    """管理员页面"""
    if not check_admin_auth():
        return jsonify({"error": "无权限访问管理页面"}), 403
    return send_from_directory(SITE_DIR, "admin.html")

@admin_bp.route("/admin/grant", methods=["POST"])
def grant_admin():
    """授予管理员权限接口"""
    if not check_admin_auth():
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

@admin_bp.route("/admin/revoke", methods=["POST"])
def revoke_admin():
    """撤销管理员权限接口"""
    if not check_admin_auth():
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

@admin_bp.route("/admin/list", methods=["GET"])
def list_users():
    """列出所有用户及其管理员状态"""
    if not check_admin_auth():
        return jsonify({"error": "无权限执行此操作"}), 403
    
    try:
        cursor.execute("SELECT username, is_admin FROM users")
        users = cursor.fetchall()
        return jsonify({"success": True, "users": users})
    except Exception as e:
        return jsonify({"success": False, "message": f"获取用户列表失败: {str(e)}"})