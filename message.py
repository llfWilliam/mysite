#这个文件专门用于存放各类定义的json文件
import json
from datetime import datetime
import threading
LOG_LOCK = threading.Lock()                #多线程加锁，基本功

#now_time 用来获得当前时间
#

def now_time() ->str:
     return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")    
     #通过这个函数可以直接得到当前时间,datetime.now()这个会返回一个datetime对象
     #这个strftime意思是string format time 把datetime对象转成指定格式的字符串
     #T是用来分隔日期和时间的
def mymessage(category: str, event: str, number:int, detail:str, more_detail:str)->str:
    message={
        "category": category,
        "event":event,
        "time":now_time(),
        "number":number,
        "detail":detail,
        "more_detail":more_detail,
    }
    return json.dumps(message,ensure_ascii=False)                  
    #务必注意加s，dumps这样才能返回字符串