#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学术资源库数据库表创建脚本
创建学术资源相关的数据库表结构
"""

import os
import mysql.connector
from config import get_db_connection

def create_academic_tables():
    """创建学术资源库相关的数据库表"""
    
    # 获取数据库连接
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        # 创建学术资源表
        academic_resources_sql = """
        CREATE TABLE IF NOT EXISTS academic_resources (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(300) NOT NULL COMMENT '资源标题',
            authors TEXT COMMENT '作者信息',
            abstract TEXT COMMENT '摘要',
            content TEXT COMMENT '内容描述',
            file_path VARCHAR(500) COMMENT '文件存储路径',
            file_type ENUM('pdf', 'doc', 'docx', 'txt', 'note') DEFAULT 'pdf' COMMENT '文件类型',
            subject VARCHAR(100) COMMENT '学科分类',
            keywords JSON COMMENT '关键词标签',
            publication_year INT COMMENT '发表年份',
            citation_count INT DEFAULT 0 COMMENT '引用次数',
            reading_status ENUM('unread', 'reading', 'completed', 'reviewing') DEFAULT 'unread' COMMENT '阅读状态',
            notes TEXT COMMENT '个人笔记',
            file_size BIGINT DEFAULT 0 COMMENT '文件大小（字节）',
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
            author_id INT NOT NULL COMMENT '上传用户ID',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学术资源表';
        """
        
        # 创建学科分类表
        subjects_sql = """
        CREATE TABLE IF NOT EXISTS academic_subjects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE COMMENT '学科名称',
            parent_id INT NULL COMMENT '父级学科ID',
            description TEXT COMMENT '学科描述',
            sort_order INT DEFAULT 0 COMMENT '排序顺序',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            FOREIGN KEY (parent_id) REFERENCES academic_subjects(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学科分类表';
        """
        
        # 创建文件存储表
        file_storage_sql = """
        CREATE TABLE IF NOT EXISTS file_storage (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255) NOT NULL COMMENT '存储文件名',
            original_name VARCHAR(255) NOT NULL COMMENT '原始文件名',
            file_path VARCHAR(500) NOT NULL COMMENT '文件存储路径',
            file_size BIGINT NOT NULL COMMENT '文件大小（字节）',
            file_type VARCHAR(100) COMMENT '文件类型',
            mime_type VARCHAR(100) COMMENT 'MIME类型',
            uploader_id INT NOT NULL COMMENT '上传用户ID',
            related_type ENUM('academic', 'guide', 'blog') NULL COMMENT '关联类型',
            related_id INT NULL COMMENT '关联记录ID',
            is_public BOOLEAN DEFAULT FALSE COMMENT '是否公开',
            download_count INT DEFAULT 0 COMMENT '下载次数',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            FOREIGN KEY (uploader_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文件存储表';
        """
        
        # 创建标签表
        tags_sql = """
        CREATE TABLE IF NOT EXISTS tags (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL UNIQUE COMMENT '标签名称',
            category VARCHAR(50) COMMENT '标签分类',
            usage_count INT DEFAULT 0 COMMENT '使用次数',
            color VARCHAR(7) DEFAULT '#007bff' COMMENT '标签颜色',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='标签表';
        """
        
        # 创建资源标签关联表
        resource_tags_sql = """
        CREATE TABLE IF NOT EXISTS academic_resource_tags (
            id INT AUTO_INCREMENT PRIMARY KEY,
            resource_id INT NOT NULL COMMENT '资源ID',
            tag_id INT NOT NULL COMMENT '标签ID',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            FOREIGN KEY (resource_id) REFERENCES academic_resources(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
            UNIQUE KEY unique_resource_tag (resource_id, tag_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='资源标签关联表';
        """
        
        # 执行SQL语句
        print("正在创建学术资源表...")
        cursor.execute(academic_resources_sql)
        print("✓ 学术资源表创建成功")
        
        print("正在创建学科分类表...")
        cursor.execute(subjects_sql)
        print("✓ 学科分类表创建成功")
        
        print("正在创建文件存储表...")
        cursor.execute(file_storage_sql)
        print("✓ 文件存储表创建成功")
        
        print("正在创建标签表...")
        cursor.execute(tags_sql)
        print("✓ 标签表创建成功")
        
        print("正在创建资源标签关联表...")
        cursor.execute(resource_tags_sql)
        print("✓ 资源标签关联表创建成功")
        
        # 插入默认学科分类数据
        default_subjects = [
            ('计算机科学', None, '计算机科学与技术相关领域', 1),
            ('数学', None, '数学相关领域', 2),
            ('物理学', None, '物理学相关领域', 3),
            ('化学', None, '化学相关领域', 4),
            ('生物学', None, '生物学相关领域', 5),
            ('医学', None, '医学相关领域', 6),
            ('工程学', None, '工程学相关领域', 7),
            ('经济学', None, '经济学相关领域', 8),
            ('管理学', None, '管理学相关领域', 9),
            ('文学', None, '文学相关领域', 10),
            ('历史学', None, '历史学相关领域', 11),
            ('哲学', None, '哲学相关领域', 12),
            ('其他', None, '其他学科领域', 99)
        ]
        
        print("正在插入默认学科分类...")
        insert_subject_sql = """
        INSERT IGNORE INTO academic_subjects (name, parent_id, description, sort_order) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(insert_subject_sql, default_subjects)
        print("✓ 默认学科分类插入成功")
        
        # 提交事务
        db.commit()
        print("\n🎉 学术资源库数据库表创建完成！")
        
    except mysql.connector.Error as e:
        print(f"❌ 数据库操作失败: {e}")
        db.rollback()
        raise
    finally:
        cursor.close()
        db.close()

def create_upload_directories():
    """创建文件上传目录"""
    base_dir = os.path.dirname(__file__)
    upload_dirs = [
        os.path.join(base_dir, "static", "uploads"),
        os.path.join(base_dir, "static", "uploads", "academic"),
        os.path.join(base_dir, "static", "uploads", "academic", "pdfs"),
        os.path.join(base_dir, "static", "uploads", "academic", "temp")
    ]
    
    for dir_path in upload_dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"✓ 创建目录: {dir_path}")
        else:
            print(f"✓ 目录已存在: {dir_path}")

if __name__ == "__main__":
    print("=" * 50)
    print("学术资源库数据库初始化")
    print("=" * 50)
    
    try:
        # 创建数据库表
        create_academic_tables()
        
        # 创建上传目录
        print("\n正在创建文件上传目录...")
        create_upload_directories()
        
        print("\n✅ 学术资源库初始化完成！")
        print("\n下一步:")
        print("1. 运行 python server.py 启动服务器")
        print("2. 访问 /academic 查看学术资源库")
        
    except Exception as e:
        print(f"\n❌ 初始化失败: {e}")
        exit(1)
