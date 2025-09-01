# MySite

一个基于Flask的用户管理系统，支持用户注册、登录、管理员权限管理和系统日志查看功能。

## 功能特性

### 用户功能
- 用户注册和登录
- 响应式Web界面
- 主题切换（白天/黑夜模式）
- 缓存清除功能

### 管理员功能
- 管理员权限授予和撤销
- 用户列表查看
- 系统日志查看（管理员日志和调试日志）
- 服务器状态监控
- 手动日志刷新

### 系统特性
- 模块化架构设计
- MySQL数据库支持
- 请求日志记录
- 权限验证机制
- 安全的Cookie认证

## 项目结构

```
mysite/
├── config.py          # 配置模块（数据库、日志配置）
├── auth.py            # 用户认证模块
├── admin.py           # 管理员功能模块
├── logs.py            # 日志功能模块
├── routes.py          # 主路由文件
├── server.py          # 服务器启动文件
├── create_admin.py    # 创建管理员用户脚本
├── static/            # 静态文件目录
│   ├── login.html     # 登录页面
│   ├── admin.html     # 管理员页面
│   ├── login.js       # 登录页面脚本
│   ├── admin.js       # 管理员页面脚本
│   ├── theme.js       # 主题切换脚本
│   ├── light.css      # 白天模式样式
│   └── dark.css       # 黑夜模式样式
├── admin.log          # 管理员日志文件
├── audit.log          # 审计日志文件
└── README.md          # 项目说明文档
```

## 环境要求

- Python 3.7+
- MySQL 5.7+
- Flask
- mysql-connector-python

## 安装配置

### 1. 克隆项目
```bash
git clone <repository-url>
cd mysite
```

### 2. 安装依赖
```bash
pip install flask mysql-connector-python
```

### 3. 数据库配置

创建MySQL数据库和用户表：

```sql
CREATE DATABASE mysite;
USE mysite;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. 环境变量配置

设置以下环境变量（可选，有默认值）：

```bash
set DB_HOST=127.0.0.1
set DB_PORT=3307
set DB_USER=root
set DB_PASSWORD=your_password
set DB_NAME=mysite
```

### 5. 创建管理员用户

```bash
python create_admin.py
```

## 使用说明

### 启动服务器

```bash
python routes.py
```

或使用专用启动脚本：

```bash
python server.py
```

服务器将在 `http://127.0.0.1:8000` 启动。

### 访问系统

1. **用户登录页面**：`http://127.0.0.1:8000`
2. **管理员页面**：`http://127.0.0.1:8000/admin`（需要管理员权限）

### 主要功能使用

#### 用户注册和登录
- 在登录页面可以注册新用户或登录现有用户
- 支持主题切换和缓存清除功能

#### 管理员功能
- 登录后的管理员用户可以访问管理页面
- 查看和管理用户列表
- 授予或撤销用户的管理员权限
- 查看系统日志和服务器状态
- 手动刷新日志内容

## API接口

### 用户认证
- `POST /register` - 用户注册
- `POST /login` - 用户登录

### 管理员功能
- `GET /admin` - 管理员页面
- `POST /admin/grant` - 授予管理员权限
- `POST /admin/revoke` - 撤销管理员权限
- `GET /admin/list` - 获取用户列表

### 日志和状态
- `GET /logs/admin` - 获取管理员日志
- `GET /logs/debug` - 获取调试日志
- `GET /status` - 获取服务器状态

## 开发说明

### 模块化架构

项目采用模块化设计，主要模块包括：

- **config.py**：统一管理数据库连接、日志配置和全局变量
- **auth.py**：处理用户注册、登录等认证功能
- **admin.py**：管理员权限管理和用户管理功能
- **logs.py**：日志查看和服务器状态监控功能
- **routes.py**：主应用文件，注册各功能模块的蓝图

### 日志系统

系统包含两套日志机制：

1. **管理员日志**（admin.log）：记录简化的请求信息，每次启动时清空
2. **审计日志**（audit.log）：记录详细的JSON格式请求信息，持久保存

### 权限验证

管理员权限通过安全的HttpOnly Cookie进行验证，确保权限控制的安全性。

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交Issue和Pull Request来改进项目。

## 更新日志

### v1.1.0
- 重构代码为模块化架构
- 优化主题切换功能
- 修复黑夜模式显示问题
- 移除自动日志刷新，改为手动刷新
- 添加缓存清除功能

### v1.0.0
- 初始版本发布
- 基础用户管理功能
- 管理员权限系统
- 日志记录功能
