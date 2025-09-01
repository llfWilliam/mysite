from flask import Flask
import os
import mysql.connector
import sys

# 检查命令行参数
if len(sys.argv) < 2:
    print("使用方法: python create_admin.py <用户名>")
    sys.exit(1)

username = sys.argv[1]

try:
    # 从环境变量里读取数据库配置
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3307")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "mysite")
    )
    cursor = db.cursor(dictionary=True)
    
    # 检查用户是否存在
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    if not user:
        print(f"错误: 用户 '{username}' 不存在")
        sys.exit(1)
    
    # 检查是否存在is_admin字段
    try:
        cursor.execute("SHOW COLUMNS FROM users LIKE 'is_admin'")
        result = cursor.fetchone()
        
        if not result:
            print("添加is_admin字段...")
            cursor.execute("ALTER TABLE users ADD COLUMN is_admin TINYINT(1) DEFAULT 0")
            db.commit()
            print("已成功添加is_admin字段")
    except Exception as e:
        print(f"检查字段时出错: {str(e)}")
        sys.exit(1)
    
    # 设置用户为管理员
    cursor.execute("UPDATE users SET is_admin = 1 WHERE username = %s", (username,))
    db.commit()
    print(f"已成功将用户 '{username}' 设置为管理员")
    
    # 显示当前管理员列表
    cursor.execute("SELECT username FROM users WHERE is_admin = 1")
    admins = cursor.fetchall()
    print("\n当前管理员列表:")
    for admin in admins:
        print(f"- {admin['username']}")
    
except mysql.connector.Error as e:
    print(f"数据库错误: {str(e)}")
except Exception as e:
    print(f"错误: {str(e)}")
finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()