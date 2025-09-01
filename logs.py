from flask import Blueprint, jsonify, request
import os
import time
from config import ADMIN_LOG, DEBUG_LOG, START_TIME

# 创建日志蓝图
logs_bp = Blueprint('logs', __name__)

def check_admin_auth():
    """检查管理员权限"""
    return request.cookies.get('admin_auth') == 'true'

@logs_bp.route("/logs/admin")
def get_admin_logs():
    """返回管理端日志（简短）"""
    if not check_admin_auth():
        return jsonify({"error": "无权限访问管理日志"}), 403
        
    if os.path.exists(ADMIN_LOG):
        with open(ADMIN_LOG, encoding="utf-8") as f:
            lines = f.read().splitlines()
        return jsonify(lines)
    return jsonify([])

@logs_bp.route("/logs/debug")
def get_debug_logs():
    """返回完整调试日志（JSON格式字符串数组）"""
    if not check_admin_auth():
        return jsonify({"error": "无权限访问调试日志"}), 403
        
    if os.path.exists(DEBUG_LOG):
        with open(DEBUG_LOG, encoding="utf-8") as f:
            lines = f.read().splitlines()
        return jsonify(lines)
    return jsonify([])

@logs_bp.route("/status")
def get_status():
    """返回服务器状态信息"""
    if not check_admin_auth():
        return jsonify({"error": "无权限访问服务器状态"}), 403
        
    status_info = {
        "server": "mysite",
        "status": "running",
        "start_time": START_TIME,
        "uptime_seconds": int(time.time() - time.mktime(time.strptime(START_TIME, "%Y-%m-%d %H:%M:%S")))
    }
    return jsonify(status_info)