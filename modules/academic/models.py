#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学术资源模块数据模型
定义学术资源相关的数据结构和操作方法
"""

import os
import json
import hashlib
import time
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from config import get_db_connection

class AcademicResource:
    """学术资源数据模型"""
    
    def __init__(self, **kwargs):
        """初始化学术资源对象"""
        self.id = kwargs.get('id')
        self.title = kwargs.get('title', '')
        self.authors = kwargs.get('authors', '')
        self.abstract = kwargs.get('abstract', '')
        self.content = kwargs.get('content', '')
        self.file_path = kwargs.get('file_path', '')
        self.file_type = kwargs.get('file_type', 'pdf')
        self.subject = kwargs.get('subject', '')
        self.keywords = kwargs.get('keywords', [])
        self.publication_year = kwargs.get('publication_year')
        self.citation_count = kwargs.get('citation_count', 0)
        self.reading_status = kwargs.get('reading_status', 'unread')
        self.notes = kwargs.get('notes', '')
        self.file_size = kwargs.get('file_size', 0)
        self.upload_time = kwargs.get('upload_time')
        self.author_id = kwargs.get('author_id')
        self.folder_id = kwargs.get('folder_id')
        self.user_category_id = kwargs.get('user_category_id')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'abstract': self.abstract,
            'content': self.content,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'subject': self.subject,
            'keywords': self.keywords,
            'publication_year': self.publication_year,
            'citation_count': self.citation_count,
            'reading_status': self.reading_status,
            'notes': self.notes,
            'file_size': self.file_size,
            'upload_time': self.upload_time,
            'author_id': self.author_id,
            'folder_id': self.folder_id,
            'user_category_id': self.user_category_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AcademicResource':
        """从字典创建对象"""
        return cls(**data)

class AcademicResourceManager:
    """学术资源管理器"""
    
    @staticmethod
    def create_resource(resource_data: Dict) -> int:
        """创建新的学术资源"""
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            # 处理关键词JSON
            keywords_json = json.dumps(resource_data.get('keywords', []), ensure_ascii=False)
            
            sql = """
            INSERT INTO academic_resources 
            (title, authors, abstract, content, file_path, file_type, subject, 
             keywords, publication_year, citation_count, reading_status, notes, 
             file_size, author_id, folder_id, user_category_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                resource_data.get('title'),
                resource_data.get('authors'),
                resource_data.get('abstract'),
                resource_data.get('content'),
                resource_data.get('file_path'),
                resource_data.get('file_type', 'pdf'),
                resource_data.get('subject'),
                keywords_json,
                resource_data.get('publication_year'),
                resource_data.get('citation_count', 0),
                resource_data.get('reading_status', 'unread'),
                resource_data.get('notes'),
                resource_data.get('file_size', 0),
                resource_data.get('author_id'),
                resource_data.get('folder_id'),
                resource_data.get('user_category_id')
            )
            
            cursor.execute(sql, values)
            resource_id = cursor.lastrowid
            
            # 处理标签关联
            if resource_data.get('tags'):
                AcademicResourceManager._link_tags(resource_id, resource_data['tags'])
            
            db.commit()
            return resource_id
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def get_resource(resource_id: int) -> Optional[AcademicResource]:
        """获取单个学术资源"""
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        try:
            sql = "SELECT * FROM academic_resources WHERE id = %s"
            cursor.execute(sql, (resource_id,))
            result = cursor.fetchone()
            
            if result:
                # 解析关键词JSON
                if result.get('keywords'):
                    result['keywords'] = json.loads(result['keywords'])
                else:
                    result['keywords'] = []
                
                return AcademicResource.from_dict(result)
            return None
            
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def get_resources(user_id: int, page: int = 1, per_page: int = 20, 
                     folder_id: int = None, category_id: int = None, 
                     status: str = None, search: str = None) -> Tuple[List[AcademicResource], int]:
        """获取学术资源列表"""
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        try:
            # 构建查询条件
            where_conditions = ["author_id = %s"]
            params = [user_id]
            
            if folder_id:
                where_conditions.append("folder_id = %s")
                params.append(folder_id)
            
            if category_id:
                where_conditions.append("user_category_id = %s")
                params.append(category_id)
            
            if status:
                where_conditions.append("reading_status = %s")
                params.append(status)
            
            if search:
                where_conditions.append("(title LIKE %s OR authors LIKE %s OR abstract LIKE %s)")
                search_param = f"%{search}%"
                params.extend([search_param, search_param, search_param])
            
            where_clause = " AND ".join(where_conditions)
            
            # 获取总数
            count_sql = f"SELECT COUNT(*) as total FROM academic_resources WHERE {where_clause}"
            cursor.execute(count_sql, params)
            total = cursor.fetchone()['total']
            
            # 获取分页数据
            offset = (page - 1) * per_page
            sql = f"""
            SELECT * FROM academic_resources 
            WHERE {where_clause}
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
            """
            cursor.execute(sql, params + [per_page, offset])
            results = cursor.fetchall()
            
            # 处理结果
            resources = []
            for result in results:
                if result.get('keywords'):
                    result['keywords'] = json.loads(result['keywords'])
                else:
                    result['keywords'] = []
                resources.append(AcademicResource.from_dict(result))
            
            return resources, total
            
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def update_resource(resource_id: int, resource_data: Dict) -> bool:
        """更新学术资源"""
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            # 处理关键词JSON
            keywords_json = json.dumps(resource_data.get('keywords', []), ensure_ascii=False)
            
            sql = """
            UPDATE academic_resources SET
            title = %s, authors = %s, abstract = %s, content = %s,
            subject = %s, keywords = %s, publication_year = %s,
            reading_status = %s, notes = %s, folder_id = %s, user_category_id = %s,
            updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """
            
            values = (
                resource_data.get('title'),
                resource_data.get('authors'),
                resource_data.get('abstract'),
                resource_data.get('content'),
                resource_data.get('subject'),
                keywords_json,
                resource_data.get('publication_year'),
                resource_data.get('reading_status'),
                resource_data.get('notes'),
                resource_data.get('folder_id'),
                resource_data.get('user_category_id'),
                resource_id
            )
            
            cursor.execute(sql, values)
            
            # 更新标签关联
            if 'tags' in resource_data:
                AcademicResourceManager._unlink_tags(resource_id)
                if resource_data['tags']:
                    AcademicResourceManager._link_tags(resource_id, resource_data['tags'])
            
            db.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def delete_resource(resource_id: int) -> bool:
        """删除学术资源"""
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            # 先获取文件路径
            cursor.execute("SELECT file_path FROM academic_resources WHERE id = %s", (resource_id,))
            result = cursor.fetchone()
            
            # 删除数据库记录
            cursor.execute("DELETE FROM academic_resources WHERE id = %s", (resource_id,))
            
            # 删除关联的标签
            AcademicResourceManager._unlink_tags(resource_id)
            
            # 删除物理文件
            if result and result[0]:
                file_path = result[0]
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except OSError:
                        pass  # 忽略文件删除错误
            
            db.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def _link_tags(resource_id: int, tags: List[str]):
        """关联标签到资源"""
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            for tag_name in tags:
                # 获取或创建标签
                cursor.execute("SELECT id FROM tags WHERE name = %s", (tag_name,))
                result = cursor.fetchone()
                
                if result:
                    tag_id = result[0]
                else:
                    cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag_name,))
                    tag_id = cursor.lastrowid
                
                # 关联标签
                cursor.execute(
                    "INSERT IGNORE INTO academic_resource_tags (resource_id, tag_id) VALUES (%s, %s)",
                    (resource_id, tag_id)
                )
                
                # 更新标签使用次数
                cursor.execute("UPDATE tags SET usage_count = usage_count + 1 WHERE id = %s", (tag_id,))
            
            db.commit()
            
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def _unlink_tags(resource_id: int):
        """取消标签关联"""
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            # 获取关联的标签ID
            cursor.execute("SELECT tag_id FROM academic_resource_tags WHERE resource_id = %s", (resource_id,))
            tag_ids = [row[0] for row in cursor.fetchall()]
            
            # 删除关联
            cursor.execute("DELETE FROM academic_resource_tags WHERE resource_id = %s", (resource_id,))
            
            # 更新标签使用次数
            for tag_id in tag_ids:
                cursor.execute("UPDATE tags SET usage_count = GREATEST(usage_count - 1, 0) WHERE id = %s", (tag_id,))
            
            db.commit()
            
        finally:
            cursor.close()
            db.close()

class SubjectManager:
    """学科分类管理器"""
    
    @staticmethod
    def get_all_subjects() -> List[Dict]:
        """获取所有学科分类"""
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        try:
            sql = "SELECT * FROM academic_subjects ORDER BY sort_order, name"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def create_subject(name: str, parent_id: int = None, description: str = '') -> int:
        """创建新学科分类"""
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            sql = """
            INSERT INTO academic_subjects (name, parent_id, description) 
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (name, parent_id, description))
            subject_id = cursor.lastrowid
            db.commit()
            return subject_id
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()

class FolderManager:
    """文件夹管理器"""
    
    @staticmethod
    def create_folder(name: str, user_id: int, parent_id: int = None, description: str = '', color: str = '#007bff') -> int:
        """创建文件夹"""
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            sql = """
            INSERT INTO academic_folders (name, parent_id, user_id, description, color) 
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (name, parent_id, user_id, description, color))
            folder_id = cursor.lastrowid
            db.commit()
            return folder_id
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def get_folders(user_id: int, parent_id: int = None) -> List[Dict]:
        """获取文件夹列表"""
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        try:
            if parent_id is None:
                sql = "SELECT * FROM academic_folders WHERE user_id = %s AND parent_id IS NULL ORDER BY sort_order, name"
                cursor.execute(sql, (user_id,))
            else:
                sql = "SELECT * FROM academic_folders WHERE user_id = %s AND parent_id = %s ORDER BY sort_order, name"
                cursor.execute(sql, (user_id, parent_id))
            
            return cursor.fetchall()
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def get_folder_tree(user_id: int) -> List[Dict]:
        """获取文件夹树形结构"""
        def build_tree(parent_id=None):
            folders = FolderManager.get_folders(user_id, parent_id)
            for folder in folders:
                children = build_tree(folder['id'])
                folder['children'] = children if children else []
            return folders
        
        return build_tree()
    
    @staticmethod
    def update_folder(folder_id: int, name: str = None, description: str = None, color: str = None) -> bool:
        """更新文件夹信息"""
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = %s")
                params.append(name)
            if description is not None:
                updates.append("description = %s")
                params.append(description)
            if color is not None:
                updates.append("color = %s")
                params.append(color)
            
            if updates:
                updates.append("updated_at = CURRENT_TIMESTAMP")
                params.append(folder_id)
                
                sql = f"UPDATE academic_folders SET {', '.join(updates)} WHERE id = %s"
                cursor.execute(sql, params)
                db.commit()
                return cursor.rowcount > 0
            
            return False
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def delete_folder(folder_id: int) -> bool:
        """删除文件夹（会同时删除子文件夹和移动文件到父文件夹）"""
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            # 获取文件夹信息
            cursor.execute("SELECT parent_id, user_id FROM academic_folders WHERE id = %s", (folder_id,))
            folder_info = cursor.fetchone()
            
            if not folder_info:
                return False
            
            parent_id, user_id = folder_info
            
            # 将文件夹内的文件移动到父文件夹
            cursor.execute("UPDATE academic_resources SET folder_id = %s WHERE folder_id = %s", (parent_id, folder_id))
            
            # 将子文件夹移动到父文件夹
            cursor.execute("UPDATE academic_folders SET parent_id = %s WHERE parent_id = %s", (parent_id, folder_id))
            
            # 删除文件夹
            cursor.execute("DELETE FROM academic_folders WHERE id = %s", (folder_id,))
            
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()

class UserCategoryManager:
    """用户自定义分类管理器"""
    
    @staticmethod
    def create_category(name: str, user_id: int, description: str = '', color: str = '#6c757d') -> int:
        """创建用户自定义分类"""
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            sql = """
            INSERT INTO user_categories (name, user_id, description, color) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (name, user_id, description, color))
            category_id = cursor.lastrowid
            db.commit()
            return category_id
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def get_categories(user_id: int) -> List[Dict]:
        """获取用户的所有分类"""
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        try:
            sql = "SELECT * FROM user_categories WHERE user_id = %s ORDER BY name"
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def update_category(category_id: int, name: str = None, description: str = None, color: str = None) -> bool:
        """更新分类信息"""
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = %s")
                params.append(name)
            if description is not None:
                updates.append("description = %s")
                params.append(description)
            if color is not None:
                updates.append("color = %s")
                params.append(color)
            
            if updates:
                params.append(category_id)
                sql = f"UPDATE user_categories SET {', '.join(updates)} WHERE id = %s"
                cursor.execute(sql, params)
                db.commit()
                return cursor.rowcount > 0
            
            return False
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def delete_category(category_id: int) -> bool:
        """删除分类"""
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            # 将使用该分类的资源分类设为NULL
            cursor.execute("UPDATE academic_resources SET user_category_id = NULL WHERE user_category_id = %s", (category_id,))
            
            # 删除分类
            cursor.execute("DELETE FROM user_categories WHERE id = %s", (category_id,))
            
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()

class FileManager:
    """文件管理器"""
    
    @staticmethod
    def save_file(file, user_id: int, file_type: str = 'academic', folder_id: int = None) -> Dict:
        """保存上传的文件"""
        # 生成唯一文件名
        timestamp = int(time.time())
        file_hash = hashlib.md5(f"{timestamp}_{file.filename}".encode()).hexdigest()[:8]
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{timestamp}_{file_hash}{file_ext}"
        
        # 确定存储路径
        base_dir = os.path.dirname(os.path.dirname(__file__))
        upload_dir = os.path.join(base_dir, "static", "uploads", file_type)
        
        # 如果有文件夹ID，创建子文件夹
        if folder_id:
            upload_dir = os.path.join(upload_dir, f"folder_{folder_id}")
        
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, unique_filename)
        
        # 保存文件
        file.save(file_path)
        
        # 获取文件信息
        file_size = os.path.getsize(file_path)
        
        return {
            'filename': unique_filename,
            'original_name': file.filename,
            'file_path': file_path,
            'file_size': file_size,
            'file_type': file_ext[1:] if file_ext else '',
            'mime_type': file.content_type
        }
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """删除文件"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except OSError:
            return False
    
    @staticmethod
    def get_file_info(file_path: str) -> Optional[Dict]:
        """获取文件信息"""
        if not os.path.exists(file_path):
            return None
        
        stat = os.stat(file_path)
        return {
            'size': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime)
        }
