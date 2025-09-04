# MySite

**版本：v2.0.0**

一个基于Flask的综合性学术资源管理系统，支持用户管理、学术文献管理、文件夹分类、个人分类标记等功能。系统采用模块化设计，提供完整的用户隔离和权限控制机制。

## 功能特性

### 🔐 用户管理
- 用户注册和登录
- 响应式Web界面
- 主题切换（白天/黑夜模式）
- 缓存清除功能
- 安全的Session管理

### 📚 学术资源库
- **文献管理**：上传、编辑、删除学术文献
- **文件支持**：PDF、DOC、DOCX、TXT格式
- **文件夹分类**：创建和管理个人文件夹
- **自定义分类**：创建个人标签和分类
- **搜索功能**：按标题、作者、摘要搜索
- **阅读状态**：未读、阅读中、已完成、复习中
- **文件预览**：PDF文件在线预览
- **文件下载**：安全的文件下载机制

### 👨‍💼 管理员功能
- 管理员权限授予和撤销
- 用户列表查看和管理
- 系统日志查看（管理员日志和调试日志）
- 服务器状态监控
- 手动日志刷新

### 🛡️ 安全特性
- **用户隔离**：每个用户只能访问自己的数据
- **权限控制**：严格的API权限验证
- **数据完整性**：外键约束和事务处理
- **SQL注入防护**：参数化查询
- **文件安全**：文件类型验证和路径安全

### 🏗️ 系统特性
- 模块化架构设计
- MySQL数据库支持
- 请求日志记录
- 权限验证机制
- 安全的Cookie认证
- RESTful API设计

## 项目结构

```
mysite/
├── config.py                    # 配置模块（数据库、日志配置）
├── auth.py                      # 用户认证模块
├── admin.py                     # 管理员功能模块
├── logs.py                      # 日志功能模块
├── version.py                   # 版本管理文件
├── routes.py                    # 主路由文件
├── server.py                    # 服务器启动文件
├── create_admin.py              # 创建管理员用户脚本
├── create_academic_tables.py    # 创建学术资源库表结构
├── requirements.txt             # Python依赖包列表
├── modules/                     # 模块目录
│   ├── __init__.py
│   └── academic/                # 学术资源库模块
│       ├── __init__.py
│       ├── models.py            # 数据模型
│       ├── routes.py            # API路由
│       └── static/              # 模块静态文件
│           └── uploads/         # 文件上传目录
│               └── academic/    # 学术文件存储
├── static/                      # 静态文件目录
│   ├── login.html               # 登录页面
│   ├── admin.html               # 管理员页面
│   ├── login.js                 # 登录页面脚本
│   ├── admin.js                 # 管理员页面脚本
│   ├── theme.js                 # 主题切换脚本
│   ├── light.css                # 白天模式样式
│   ├── dark.css                 # 黑夜模式样式
│   └── uploads/                 # 全局上传目录
│       └── academic/            # 学术文件存储
├── templates/                   # 模板目录
│   └── academic/                # 学术资源库模板
│       ├── file_manager.html    # 文件管理器页面
│       └── index.html           # 学术资源库首页
├── logs/                        # 日志目录
│   ├── admin.log                # 管理员日志
│   └── server.log               # 服务器日志
├── admin.log                    # 管理员日志文件（兼容）
├── audit.log                    # 审计日志文件
└── README.md                    # 项目说明文档
```

## 环境要求

- **Python**: 3.7+
- **数据库**: MySQL 5.7+ 或 MariaDB 10.3+
- **浏览器**: 支持ES6+的现代浏览器
- **内存**: 建议512MB以上
- **存储**: 根据文件数量而定，建议预留足够空间

## 安装配置

### 1. 克隆项目
```bash
git clone <repository-url>
cd mysite
```

### 2. 安装依赖

**方法一：使用requirements.txt（推荐）**
```bash
pip install -r requirements.txt
```

**方法二：手动安装**
```bash
pip install flask mysql-connector-python
```

### 3. 数据库配置

创建MySQL数据库和基础表结构：

```sql
CREATE DATABASE mysite;
USE mysite;

-- 用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**自动创建学术资源库表结构**：

```bash
python create_academic_tables.py
```

这将自动创建以下表：
- `academic_resources` - 学术资源表
- `academic_folders` - 文件夹表
- `user_categories` - 用户分类表
- `academic_subjects` - 学科分类表
- `tags` - 标签表
- `academic_resource_tags` - 资源标签关联表
- `file_storage` - 文件存储表

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
2. **学术资源库**：`http://127.0.0.1:8000/academic`（需要登录）
3. **管理员页面**：`http://127.0.0.1:8000/admin`（需要管理员权限）

### 主要功能使用

#### 用户注册和登录
- 在登录页面可以注册新用户或登录现有用户
- 支持主题切换和缓存清除功能

#### 学术资源库使用
1. **创建文件夹**：点击"新建文件夹"按钮创建个人文件夹
2. **创建分类**：点击"新建分类"按钮创建个人标签分类
3. **添加文献**：点击"添加文献"按钮上传学术文献
4. **编辑文献**：点击文献卡片的编辑按钮修改文献信息
5. **文件管理**：支持PDF预览、文件下载、删除等操作
6. **搜索功能**：使用搜索框快速查找文献

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

### 学术资源库
- `GET /academic/` - 学术资源库首页
- `GET /academic/api/resources` - 获取文献列表
- `POST /academic/api/resources` - 创建文献
- `GET /academic/api/resources/<id>` - 获取文献详情
- `PUT /academic/api/resources/<id>` - 更新文献
- `DELETE /academic/api/resources/<id>` - 删除文献
- `GET /academic/api/download/<id>` - 下载文件
- `GET /academic/api/preview/<id>` - 预览PDF文件

### 文件夹管理
- `GET /academic/api/folders` - 获取文件夹列表
- `GET /academic/api/folders/tree` - 获取文件夹树
- `POST /academic/api/folders` - 创建文件夹
- `PUT /academic/api/folders/<id>` - 更新文件夹
- `DELETE /academic/api/folders/<id>` - 删除文件夹

### 分类管理
- `GET /academic/api/categories` - 获取用户分类
- `POST /academic/api/categories` - 创建分类
- `PUT /academic/api/categories/<id>` - 更新分类
- `DELETE /academic/api/categories/<id>` - 删除分类

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
- **version.py**：版本管理和版本信息维护
- **routes.py**：主应用文件，注册各功能模块的蓝图
- **modules/academic/**：学术资源库模块
  - **models.py**：数据模型和数据库操作
  - **routes.py**：API路由和业务逻辑

### 版本管理

项目使用严格的版本管理系统：

- **version.py**：集中管理版本信息、构建日期、版本历史
- **config.py**：导入版本信息作为全局配置
- **routes.py**：启动时显示版本信息
- **logs.py**：API接口返回版本信息

版本信息包括：
- 版本号（语义化版本控制）
- 构建日期
- 版本历史和更新日志
- 作者和描述信息

### 日志系统

系统包含两套日志机制：

1. **管理员日志**（admin.log）：记录简化的请求信息，每次启动时清空
2. **审计日志**（audit.log）：记录详细的JSON格式请求信息，持久保存

### 权限验证

- **用户认证**：通过安全的HttpOnly Cookie进行验证
- **用户隔离**：每个用户只能访问自己的数据
- **API权限**：所有API都有严格的权限检查
- **数据完整性**：外键约束确保数据关联正确

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交Issue和Pull Request来改进项目。

## 更新日志

### v2.0.0 (当前版本)
- 🆕 **学术资源库模块**：完整的文献管理系统
- 🆕 **文件夹管理**：创建、编辑、删除个人文件夹
- 🆕 **分类系统**：自定义标签和分类管理
- 🆕 **文件上传**：支持PDF、DOC、DOCX、TXT格式
- 🆕 **文件预览**：PDF文件在线预览功能
- 🆕 **搜索功能**：按标题、作者、摘要搜索文献
- 🆕 **阅读状态**：未读、阅读中、已完成、复习中状态管理
- 🆕 **用户隔离**：完整的用户数据隔离机制
- 🆕 **RESTful API**：标准化的API接口设计
- 🔧 **模块化架构**：学术资源库独立模块设计
- 🔧 **权限控制**：严格的API权限验证
- 🔧 **数据完整性**：外键约束和事务处理

### v1.0.0
- 模块化架构设计
- 用户注册和登录功能
- 管理员权限管理系统
- 系统日志记录和查看功能
- 响应式Web界面
- 主题切换功能（白天/黑夜模式）
- 缓存清除功能
- 手动日志刷新机制
- MySQL数据库支持
- 安全的Cookie认证机制
