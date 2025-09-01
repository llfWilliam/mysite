import os
import time
import logging
import mysql.connector

# 文件路径配置
BASE_DIR = os.path.dirname(__file__)
SITE_DIR = os.path.join(BASE_DIR, "static")
START_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 日志文件配置
ADMIN_LOG = "admin.log"
DEBUG_LOG = "audit.log"

# 数据库连接配置
def get_db_connection():
    """获取数据库连接"""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3307")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "mysite")
    )

# 初始化数据库连接和游标
db = get_db_connection()
cursor = db.cursor(dictionary=True)

# 日志配置函数
def setup_logging():
    """设置日志配置"""
    # 每次启动都清空管理员日志
    open(ADMIN_LOG, "w").close()
    
    # 配置普通日志
    logging.basicConfig(
        filename=DEBUG_LOG,
        level=logging.INFO,
        format="%(message)s"
    )
    
    # 创建审计日志记录器
    audit_logger = logging.getLogger("audit")
    
    # 创建管理员日志记录器
    admin_logger = logging.getLogger("admin")
    admin_handler = logging.FileHandler(ADMIN_LOG, encoding="utf-8")
    admin_logger.addHandler(admin_handler)
    admin_logger.setLevel(logging.INFO)
    
    return audit_logger, admin_logger

# 初始化日志记录器
audit_logger, admin_logger = setup_logging()