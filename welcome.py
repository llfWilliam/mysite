import json
from datetime import datetime
from message import mymessage

def show_welcome(port: int):
    today_str = datetime.now().strftime("%Y年%m月%d日")
    weekday_str = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"][datetime.now().weekday()]
    welcome_json = mymessage(
        category="system",
        event="server_start",
        number=port,
        detail=f"管理员，欢迎你！今天是 {today_str} {weekday_str}",
        more_detail=f"服务器已启动，端口号为 {port}"
    )
    msg = json.loads(welcome_json)
    print(msg["detail"])
    print(msg["more_detail"])
    print(f"访问地址: http://127.0.0.1:{port}")