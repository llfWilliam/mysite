import os
from router import app  # 你现有的 Flask 应用
from welcome import show_welcome

def ask_port(default=8000) -> int:
    try:
        s = input(f"请输入要使用的端口号（默认{default}）：").strip()
        return int(s) if s else default
    except Exception:
        return default

if __name__ == "__main__":                              
    #这个函数意思是，只有在这个文件被主动拉起来才会用，单单import的话是不会执行的
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", str(ask_port())))      
    #如果环境变量没设置，就 fallback 用默认 127.0.0.1
    show_welcome(port)
    app.run(host=host, port=port, debug=False)