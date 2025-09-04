#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学术资源模块路由
处理学术资源相关的HTTP请求
"""

import os
import json
from flask import Blueprint, request, jsonify, render_template, send_file, current_app, session
from werkzeug.utils import secure_filename
from modules.academic.models import AcademicResourceManager, SubjectManager, FileManager, FolderManager, UserCategoryManager
from auth import login_required

# 创建蓝图
academic_bp = Blueprint('academic', __name__, url_prefix='/academic')

# 允许的文件类型
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@academic_bp.route('/')
@login_required
def index():
    """学术资源库首页"""
    return render_template('academic/file_manager.html')

@academic_bp.route('/classic')
@login_required
def classic_view():
    """经典视图"""
    return render_template('academic/index.html')

@academic_bp.route('/test')
def test_session():
    """测试session状态"""
    return jsonify({
        'session': dict(session),
        'user_id': session.get('user_id'),
        'username': session.get('username')
    })

@academic_bp.route('/api/resources', methods=['GET'])
@login_required
def get_resources():
    """获取学术资源列表"""
    try:
        user_id = session.get('user_id')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        folder_id = request.args.get('folder_id', type=int)
        category_id = request.args.get('category_id', type=int)
        status = request.args.get('status')
        search = request.args.get('search')
        
        resources, total = AcademicResourceManager.get_resources(
            user_id=user_id,
            page=page,
            per_page=per_page,
            folder_id=folder_id,
            category_id=category_id,
            status=status,
            search=search
        )
        
        return jsonify({
            'success': True,
            'data': {
                'resources': [resource.to_dict() for resource in resources],
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': (total + per_page - 1) // per_page
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取资源列表失败: {str(e)}'
        }), 500

@academic_bp.route('/api/resources', methods=['POST'])
@login_required
def create_resource():
    """创建新的学术资源"""
    try:
        user_id = session.get('user_id')
        
        # 获取表单数据
        title = request.form.get('title', '').strip()
        authors = request.form.get('authors', '').strip()
        abstract = request.form.get('abstract', '').strip()
        content = request.form.get('content', '').strip()
        subject = request.form.get('subject', '').strip()
        publication_year = request.form.get('publication_year')
        notes = request.form.get('notes', '').strip()
        
        # 获取文件夹和分类信息
        folder_id = request.form.get('folder_id')
        user_category_id = request.form.get('user_category_id')
        
        # 处理关键词
        keywords_str = request.form.get('keywords', '')
        keywords = [k.strip() for k in keywords_str.split(',') if k.strip()] if keywords_str else []
        
        # 处理标签
        tags_str = request.form.get('tags', '')
        tags = [t.strip() for t in tags_str.split(',') if t.strip()] if tags_str else []
        
        # 验证必填字段
        if not title:
            return jsonify({
                'success': False,
                'message': '标题不能为空'
            }), 400
        
        # 处理文件上传
        file_info = None
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename):
                # 传递文件夹ID用于文件分类存储
                file_info = FileManager.save_file(file, user_id, 'academic', 
                                                int(folder_id) if folder_id else None)
            elif file and file.filename:
                return jsonify({
                    'success': False,
                    'message': '不支持的文件类型，仅支持 PDF、DOC、DOCX、TXT 格式'
                }), 400
        
        # 准备资源数据
        resource_data = {
            'title': title,
            'authors': authors,
            'abstract': abstract,
            'content': content,
            'subject': subject,
            'keywords': keywords,
            'publication_year': int(publication_year) if publication_year else None,
            'notes': notes,
            'author_id': user_id,
            'tags': tags,
            'folder_id': int(folder_id) if folder_id else None,
            'user_category_id': int(user_category_id) if user_category_id else None
        }
        
        # 添加文件信息
        if file_info:
            resource_data.update({
                'file_path': file_info['file_path'],
                'file_type': file_info['file_type'],
                'file_size': file_info['file_size']
            })
        
        # 创建资源
        resource_id = AcademicResourceManager.create_resource(resource_data)
        
        return jsonify({
            'success': True,
            'message': '学术资源创建成功',
            'data': {'resource_id': resource_id}
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'创建资源失败: {str(e)}'
        }), 500

@academic_bp.route('/api/resources/<int:resource_id>', methods=['GET'])
@login_required
def get_resource(resource_id):
    """获取单个学术资源详情"""
    try:
        resource = AcademicResourceManager.get_resource(resource_id)
        
        if not resource:
            return jsonify({
                'success': False,
                'message': '资源不存在'
            }), 404
        
        # 检查权限（只能查看自己的资源）
        user_id = session.get('user_id')
        if resource.author_id != user_id:
            return jsonify({
                'success': False,
                'message': '无权限访问此资源'
            }), 403
        
        return jsonify({
            'success': True,
            'data': resource.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取资源详情失败: {str(e)}'
        }), 500

@academic_bp.route('/api/resources/<int:resource_id>', methods=['PUT'])
@login_required
def update_resource(resource_id):
    """更新学术资源"""
    try:
        user_id = session.get('user_id')
        
        # 检查资源是否存在
        resource = AcademicResourceManager.get_resource(resource_id)
        if not resource:
            return jsonify({
                'success': False,
                'message': '资源不存在'
            }), 404
        
        # 检查权限
        if resource.author_id != user_id:
            return jsonify({
                'success': False,
                'message': '无权限修改此资源'
            }), 403
        
        # 获取更新数据
        data = request.get_json()
        
        # 准备更新数据
        update_data = {}
        for field in ['title', 'authors', 'abstract', 'content', 'subject', 
                     'publication_year', 'reading_status', 'notes', 'folder_id', 'user_category_id']:
            if field in data:
                update_data[field] = data[field]
        
        # 处理关键词
        if 'keywords' in data:
            update_data['keywords'] = data['keywords']
        
        # 处理标签
        if 'tags' in data:
            update_data['tags'] = data['tags']
        
        # 更新资源
        success = AcademicResourceManager.update_resource(resource_id, update_data)
        
        if success:
            return jsonify({
                'success': True,
                'message': '资源更新成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '资源更新失败'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'更新资源失败: {str(e)}'
        }), 500

@academic_bp.route('/api/resources/<int:resource_id>', methods=['DELETE'])
@login_required
def delete_resource(resource_id):
    """删除学术资源"""
    try:
        user_id = session.get('user_id')
        
        # 检查资源是否存在
        resource = AcademicResourceManager.get_resource(resource_id)
        if not resource:
            return jsonify({
                'success': False,
                'message': '资源不存在'
            }), 404
        
        # 检查权限
        if resource.author_id != user_id:
            return jsonify({
                'success': False,
                'message': '无权限删除此资源'
            }), 403
        
        # 删除资源
        success = AcademicResourceManager.delete_resource(resource_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': '资源删除成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '资源删除失败'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'删除资源失败: {str(e)}'
        }), 500

@academic_bp.route('/api/subjects', methods=['GET'])
@login_required
def get_subjects():
    """获取学科分类列表"""
    try:
        subjects = SubjectManager.get_all_subjects()
        return jsonify({
            'success': True,
            'data': subjects
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取学科分类失败: {str(e)}'
        }), 500

@academic_bp.route('/api/upload', methods=['POST'])
@login_required
def upload_file():
    """上传文件"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': '没有选择文件'
            }), 400
        
        file = request.files['file']
        if not file or not file.filename:
            return jsonify({
                'success': False,
                'message': '没有选择文件'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'message': '不支持的文件类型，仅支持 PDF、DOC、DOCX、TXT 格式'
            }), 400
        
        user_id = session.get('user_id')
        file_info = FileManager.save_file(file, user_id, 'academic')
        
        return jsonify({
            'success': True,
            'message': '文件上传成功',
            'data': file_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'文件上传失败: {str(e)}'
        }), 500

@academic_bp.route('/api/download/<int:resource_id>')
@login_required
def download_file(resource_id):
    """下载文件"""
    try:
        user_id = session.get('user_id')
        
        # 获取资源信息
        resource = AcademicResourceManager.get_resource(resource_id)
        if not resource:
            return jsonify({
                'success': False,
                'message': '资源不存在'
            }), 404
        
        # 检查权限
        if resource.author_id != user_id:
            return jsonify({
                'success': False,
                'message': '无权限下载此文件'
            }), 403
        
        # 检查文件是否存在
        if not resource.file_path or not os.path.exists(resource.file_path):
            return jsonify({
                'success': False,
                'message': '文件不存在'
            }), 404
        
        # 返回文件
        return send_file(
            resource.file_path,
            as_attachment=True,
            download_name=resource.title + '.' + resource.file_type
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'文件下载失败: {str(e)}'
        }), 500

@academic_bp.route('/api/preview/<int:resource_id>')
@login_required
def preview_file(resource_id):
    """预览文件（仅支持PDF）"""
    try:
        user_id = session.get('user_id')
        
        # 获取资源信息
        resource = AcademicResourceManager.get_resource(resource_id)
        if not resource:
            return jsonify({
                'success': False,
                'message': '资源不存在'
            }), 404
        
        # 检查权限
        if resource.author_id != user_id:
            return jsonify({
                'success': False,
                'message': '无权限预览此文件'
            }), 403
        
        # 检查文件类型
        if resource.file_type.lower() != 'pdf':
            return jsonify({
                'success': False,
                'message': '仅支持PDF文件预览'
            }), 400
        
        # 检查文件是否存在
        if not resource.file_path or not os.path.exists(resource.file_path):
            return jsonify({
                'success': False,
                'message': '文件不存在'
            }), 404
        
        # 返回PDF文件用于预览
        return send_file(resource.file_path, mimetype='application/pdf')
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'文件预览失败: {str(e)}'
        }), 500

# 文件夹管理API
@academic_bp.route('/api/folders', methods=['GET'])
@login_required
def get_folders():
    """获取文件夹列表"""
    try:
        user_id = session.get('user_id')
        parent_id = request.args.get('parent_id', type=int)
        
        if parent_id is None:
            folders = FolderManager.get_folders(user_id)
        else:
            folders = FolderManager.get_folders(user_id, parent_id)
        
        return jsonify({
            'success': True,
            'data': folders
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取文件夹列表失败: {str(e)}'
        }), 500

@academic_bp.route('/api/folders/tree', methods=['GET'])
@login_required
def get_folder_tree():
    """获取文件夹树形结构"""
    try:
        user_id = session.get('user_id')
        tree = FolderManager.get_folder_tree(user_id)
        
        return jsonify({
            'success': True,
            'data': tree
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取文件夹树失败: {str(e)}'
        }), 500

@academic_bp.route('/api/folders', methods=['POST'])
@login_required
def create_folder():
    """创建文件夹"""
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        
        name = data.get('name', '').strip()
        parent_id = data.get('parent_id')
        description = data.get('description', '').strip()
        color = data.get('color', '#007bff')
        
        if not name:
            return jsonify({
                'success': False,
                'message': '文件夹名称不能为空'
            }), 400
        
        folder_id = FolderManager.create_folder(name, user_id, parent_id, description, color)
        
        return jsonify({
            'success': True,
            'message': '文件夹创建成功',
            'data': {'folder_id': folder_id}
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'创建文件夹失败: {str(e)}'
        }), 500

@academic_bp.route('/api/folders/<int:folder_id>', methods=['PUT'])
@login_required
def update_folder(folder_id):
    """更新文件夹"""
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        
        # 检查文件夹是否属于当前用户
        folders = FolderManager.get_folders(user_id)
        folder_exists = any(f['id'] == folder_id for f in folders)
        
        if not folder_exists:
            return jsonify({
                'success': False,
                'message': '文件夹不存在或无权限'
            }), 403
        
        success = FolderManager.update_folder(
            folder_id,
            name=data.get('name'),
            description=data.get('description'),
            color=data.get('color')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': '文件夹更新成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '文件夹更新失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'更新文件夹失败: {str(e)}'
        }), 500

@academic_bp.route('/api/folders/<int:folder_id>', methods=['DELETE'])
@login_required
def delete_folder(folder_id):
    """删除文件夹"""
    try:
        user_id = session.get('user_id')
        
        # 检查文件夹是否属于当前用户
        folders = FolderManager.get_folders(user_id)
        folder_exists = any(f['id'] == folder_id for f in folders)
        
        if not folder_exists:
            return jsonify({
                'success': False,
                'message': '文件夹不存在或无权限'
            }), 403
        
        success = FolderManager.delete_folder(folder_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': '文件夹删除成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '文件夹删除失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'删除文件夹失败: {str(e)}'
        }), 500

# 用户分类管理API
@academic_bp.route('/api/categories', methods=['GET'])
@login_required
def get_user_categories():
    """获取用户自定义分类"""
    try:
        user_id = session.get('user_id')
        categories = UserCategoryManager.get_categories(user_id)
        
        return jsonify({
            'success': True,
            'data': categories
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取分类列表失败: {str(e)}'
        }), 500

@academic_bp.route('/api/categories', methods=['POST'])
@login_required
def create_user_category():
    """创建用户自定义分类"""
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        color = data.get('color', '#6c757d')
        
        if not name:
            return jsonify({
                'success': False,
                'message': '分类名称不能为空'
            }), 400
        
        category_id = UserCategoryManager.create_category(name, user_id, description, color)
        
        return jsonify({
            'success': True,
            'message': '分类创建成功',
            'data': {'category_id': category_id}
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'创建分类失败: {str(e)}'
        }), 500

@academic_bp.route('/api/categories/<int:category_id>', methods=['PUT'])
@login_required
def update_user_category(category_id):
    """更新用户自定义分类"""
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        
        # 检查分类是否属于当前用户
        categories = UserCategoryManager.get_categories(user_id)
        category_exists = any(c['id'] == category_id for c in categories)
        
        if not category_exists:
            return jsonify({
                'success': False,
                'message': '分类不存在或无权限'
            }), 403
        
        success = UserCategoryManager.update_category(
            category_id,
            name=data.get('name'),
            description=data.get('description'),
            color=data.get('color')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': '分类更新成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '分类更新失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'更新分类失败: {str(e)}'
        }), 500

@academic_bp.route('/api/categories/<int:category_id>', methods=['DELETE'])
@login_required
def delete_user_category(category_id):
    """删除用户自定义分类"""
    try:
        user_id = session.get('user_id')
        
        # 检查分类是否属于当前用户
        categories = UserCategoryManager.get_categories(user_id)
        category_exists = any(c['id'] == category_id for c in categories)
        
        if not category_exists:
            return jsonify({
                'success': False,
                'message': '分类不存在或无权限'
            }), 403
        
        success = UserCategoryManager.delete_category(category_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': '分类删除成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '分类删除失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'删除分类失败: {str(e)}'
        }), 500
