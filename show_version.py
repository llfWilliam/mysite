#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本信息查看工具
快速查看MySite项目的版本信息
"""

from version import print_version, get_full_version_info, VERSION_HISTORY
import json

def show_detailed_version():
    """显示详细版本信息"""
    print("=" * 50)
    print_version()
    print("=" * 50)
    
    info = get_full_version_info()
    print(f"版本号: {info['version']}")
    print(f"版本信息: {info['version_info']}")
    print(f"作者: {info['author']}")
    print(f"描述: {info['description']}")
    print(f"构建日期: {info['build_date']}")
    print()
    
    # 显示版本历史
    print("版本历史:")
    print("-" * 30)
    for version, details in VERSION_HISTORY.items():
        print(f"版本 {version} ({details['release_date']})")
        if details['features']:
            print("  新功能:")
            for feature in details['features']:
                print(f"    - {feature}")
        if details['bug_fixes']:
            print("  修复:")
            for fix in details['bug_fixes']:
                print(f"    - {fix}")
        if details['breaking_changes']:
            print("  破坏性变更:")
            for change in details['breaking_changes']:
                print(f"    - {change}")
        print()

def export_version_json():
    """导出版本信息为JSON格式"""
    info = get_full_version_info()
    version_data = {
        **info,
        "version_history": VERSION_HISTORY
    }
    
    with open('version_info.json', 'w', encoding='utf-8') as f:
        json.dump(version_data, f, ensure_ascii=False, indent=2)
    
    print("版本信息已导出到 version_info.json")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        export_version_json()
    else:
        show_detailed_version()