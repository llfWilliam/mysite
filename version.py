# MySite 版本管理
# 严格的版本控制文件

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)
__author__ = "MySite Team"
__description__ = "基于Flask的用户管理系统"
__build_date__ = "2024-01-22"

# 版本历史
VERSION_HISTORY = {
    "1.0.0": {
        "release_date": "2024-01-22",
        "features": [
            "模块化架构设计",
            "用户注册和登录功能",
            "管理员权限管理系统",
            "系统日志记录和查看功能",
            "响应式Web界面",
            "主题切换功能（白天/黑夜模式）",
            "缓存清除功能",
            "手动日志刷新机制",
            "MySQL数据库支持",
            "安全的Cookie认证机制"
        ],
        "bug_fixes": [],
        "breaking_changes": []
    }
}

def get_version():
    """获取当前版本号"""
    return __version__

def get_version_info():
    """获取版本信息元组"""
    return __version_info__

def get_full_version_info():
    """获取完整版本信息"""
    return {
        "version": __version__,
        "version_info": __version_info__,
        "author": __author__,
        "description": __description__,
        "build_date": __build_date__
    }

def print_version():
    """打印版本信息"""
    print(f"MySite v{__version__}")
    print(f"构建日期: {__build_date__}")
    print(f"描述: {__description__}")