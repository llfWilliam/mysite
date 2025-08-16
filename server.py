import os
from manage_api import app  # 你现有的 Flask 应用

def ask_port(default=8000) -> int:
    try:
        s = input(f"请输入要使用的端口号（默认{default}）：").strip()
        return int(s) if s else default
    except Exception:
        return default

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", str(ask_port())))
    print(f"\n=> Flask 开发服务器启动： http://{host}:{port}/  （管理端：/admin）\n")
    # 注意：Flask 开发服务器仅用于本地开发，正式环境请换 WSGI（如 waitress、gunicorn）
    app.run(host=host, port=port, debug=False)