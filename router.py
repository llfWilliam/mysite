import os, json
from urllib.parse import urlparse
from api import get_status, get_admin_logs, get_debug_logs

#整理一下一般路径和管理端路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.join(BASE_DIR, "site")
MANAGE_DIR = os.path.join(BASE_DIR, "manage_site")

def handle_request(handler):
    parsed = urlparse(handler.path)
    #解析当前请求的 URL，将其拆分成各个组成部分，方便后续对 URL 中的路径、查询参数等进行处理。
    
    
    
    