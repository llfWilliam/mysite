# MySite 个人空间系统 - 快速启动指南

## 🚀 快速开始

### 1. 环境准备

确保你的开发环境满足以下要求：
- Python 3.7+
- MySQL 5.7+
- Git

### 2. 克隆和安装

```bash
# 克隆项目
git clone <your-repository-url>
cd mysite

# 安装依赖
pip install -r requirements.txt
```

### 3. 数据库设置

```sql
-- 创建数据库
CREATE DATABASE mysite_v2;
USE mysite_v2;

-- 运行现有的用户表创建脚本
-- 然后运行新的表结构脚本（见DEVELOPMENT_PLAN.md）
```

### 4. 环境变量配置

```bash
# Windows PowerShell
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3307"
$env:DB_USER="root"
$env:DB_PASSWORD="your_password"
$env:DB_NAME="mysite_v2"

# 或者创建 .env 文件
echo "DB_HOST=127.0.0.1" > .env
echo "DB_PORT=3307" >> .env
echo "DB_USER=root" >> .env
echo "DB_PASSWORD=your_password" >> .env
echo "DB_NAME=mysite_v2" >> .env
```

### 5. 启动开发服务器

```bash
# 启动现有系统（验证基础功能）
python routes.py

# 或者使用专用启动脚本
python server.py
```

## 🛠️ 开发工作流

### 第一步：基础架构搭建
1. 创建新的数据库表结构
2. 设置文件上传目录
3. 创建基础模块结构

### 第二步：核心功能开发
1. 从游戏攻略模块开始（相对简单）
2. 然后是学术资源模块
3. 最后是博客系统

### 第三步：集成和测试
1. 模块间集成测试
2. 用户界面优化
3. 性能测试和优化

## 📁 目录结构说明

```
mysite/
├── modules/              # 新功能模块目录
│   ├── guides/          # 游戏攻略模块
│   ├── academic/        # 学术资源模块
│   ├── blog/            # 博客模块
│   ├── files/           # 文件管理模块
│   └── search/          # 搜索模块
├── static/
│   ├── uploads/         # 文件上传目录
│   ├── js/              # 新增JavaScript文件
│   └── css/             # 新增样式文件
└── templates/            # 新增页面模板
```

## 🔧 开发工具推荐

### 代码编辑器
- **VS Code**: 推荐使用，有很好的Python和Flask扩展
- **PyCharm**: 专业的Python IDE

### 数据库管理
- **MySQL Workbench**: 官方MySQL管理工具
- **phpMyAdmin**: Web端数据库管理

### API测试
- **Postman**: 测试API接口
- **Insomnia**: 轻量级API测试工具

## 📚 学习资源

### Flask相关
- [Flask官方文档](https://flask.palletsprojects.com/)
- [Flask蓝图使用指南](https://flask.palletsprojects.com/en/2.3.x/blueprints/)

### 前端技术
- [Markdown语法](https://www.markdownguide.org/)
- [JavaScript ES6+](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

### 数据库设计
- [MySQL官方文档](https://dev.mysql.com/doc/)
- [数据库设计最佳实践](https://www.databasejournal.com/features/mysql/article.php/10899_3911761_2.htm)

## 🐛 常见问题解决

### 1. 数据库连接失败
- 检查MySQL服务是否启动
- 验证数据库连接参数
- 确认用户权限

### 2. 模块导入错误
- 检查Python路径设置
- 确认模块文件存在
- 验证导入语句语法

### 3. 文件上传失败
- 检查上传目录权限
- 验证文件大小限制
- 确认文件类型支持

## 📞 获取帮助

如果在开发过程中遇到问题：

1. 查看项目文档
2. 检查错误日志
3. 搜索相关技术文档
4. 在项目Issues中提问

## 🎯 下一步

完成基础设置后，建议按以下顺序进行开发：

1. **阅读DEVELOPMENT_PLAN.md** - 了解完整的开发计划
2. **创建数据库表结构** - 按照计划中的SQL脚本
3. **搭建模块框架** - 创建基础的模块目录结构
4. **开发第一个功能** - 建议从游戏攻略模块开始

---

**祝开发顺利！** 🎉

*如有问题，请参考DEVELOPMENT_PLAN.md获取详细信息。*

