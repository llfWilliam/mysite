# 学术资源库快速启动指南

## 🎯 功能概述

学术资源库是MySite个人空间系统的重要组成部分，支持：

- **PDF文件上传和管理** - 支持PDF、DOC、DOCX、TXT格式
- **智能分类管理** - 按学科、阅读状态、关键词分类
- **在线预览** - PDF文件在线预览功能
- **个人笔记** - 为每个资源添加个人笔记
- **标签系统** - 灵活的标签管理
- **搜索功能** - 支持标题、作者、摘要搜索

## 🚀 快速开始

### 1. 数据库初始化

```bash
# 运行数据库初始化脚本
python create_academic_tables.py
```

### 2. 启动服务器

```bash
# 启动MySite服务器
python server.py
```

### 3. 访问学术资源库

打开浏览器访问：`http://localhost:8000/academic`

## 📁 文件结构

```
mysite/
├── modules/academic/          # 学术资源模块
│   ├── __init__.py
│   ├── models.py             # 数据模型
│   └── routes.py             # 路由处理
├── templates/academic/        # 前端模板
│   └── index.html            # 主页面
├── static/uploads/academic/   # 文件上传目录
│   ├── pdfs/                 # PDF文件存储
│   └── temp/                 # 临时文件
├── create_academic_tables.py  # 数据库初始化脚本
└── test_academic.py          # 功能测试脚本
```

## 🗄️ 数据库表结构

### 主要数据表

1. **academic_resources** - 学术资源主表
2. **academic_subjects** - 学科分类表
3. **file_storage** - 文件存储表
4. **tags** - 标签表
5. **academic_resource_tags** - 资源标签关联表

### 默认学科分类

- 计算机科学
- 数学
- 物理学
- 化学
- 生物学
- 医学
- 工程学
- 经济学
- 管理学
- 文学
- 历史学
- 哲学
- 其他

## 🔧 API接口

### 资源管理

- `GET /academic/api/resources` - 获取资源列表
- `POST /academic/api/resources` - 创建新资源
- `GET /academic/api/resources/<id>` - 获取资源详情
- `PUT /academic/api/resources/<id>` - 更新资源
- `DELETE /academic/api/resources/<id>` - 删除资源

### 文件操作

- `POST /academic/api/upload` - 上传文件
- `GET /academic/api/download/<id>` - 下载文件
- `GET /academic/api/preview/<id>` - 预览PDF文件

### 分类管理

- `GET /academic/api/subjects` - 获取学科分类

## 📝 使用说明

### 添加学术资源

1. 点击"添加资源"按钮
2. 填写资源信息（标题为必填项）
3. 选择学科分类
4. 上传PDF文件（可选）
5. 添加摘要、关键词、个人笔记
6. 点击"保存"

### 管理资源

- **编辑** - 点击资源卡片上的"编辑"按钮
- **下载** - 点击"下载"按钮下载原始文件
- **预览** - 点击"预览"按钮在线查看PDF（仅支持PDF）
- **删除** - 点击"删除"按钮删除资源

### 筛选和搜索

- **学科筛选** - 按学科分类筛选资源
- **状态筛选** - 按阅读状态筛选（未读/阅读中/已完成/复习中）
- **关键词搜索** - 在搜索框中输入关键词

## 🛠️ 开发说明

### 扩展功能

1. **添加新的文件类型支持**
   - 修改 `modules/academic/routes.py` 中的 `ALLOWED_EXTENSIONS`
   - 更新文件处理逻辑

2. **自定义学科分类**
   - 通过 `SubjectManager.create_subject()` 添加新分类
   - 或直接在数据库中插入记录

3. **添加新的资源字段**
   - 修改数据库表结构
   - 更新 `AcademicResource` 模型
   - 修改前端表单

### 测试

```bash
# 运行功能测试
python test_academic.py
```

## 🔒 权限说明

- 用户只能管理自己上传的资源
- 文件下载和预览需要登录
- 所有操作都会记录在审计日志中

## 📊 性能优化

- 文件上传支持大文件（建议限制在100MB以内）
- 分页加载资源列表
- 数据库索引优化
- 文件存储路径优化

## 🐛 故障排除

### 常见问题

1. **文件上传失败**
   - 检查文件大小限制
   - 确认文件格式支持
   - 检查磁盘空间

2. **数据库连接失败**
   - 检查数据库配置
   - 确认数据库服务运行
   - 验证用户权限

3. **PDF预览不显示**
   - 确认文件格式为PDF
   - 检查文件是否损坏
   - 确认浏览器支持PDF预览

### 日志查看

- 系统日志：`audit.log`
- 管理员日志：`admin.log`
- 服务器日志：控制台输出

## 📞 技术支持

如有问题，请检查：
1. 数据库连接配置
2. 文件权限设置
3. 服务器日志信息

---

**版本**: v1.0.0  
**更新时间**: 2024-01-22  
**维护者**: MySite Team
