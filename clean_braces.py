#!/usr/bin/env python3
"""
清理孤立的{ 字符
"""

import re
from pathlib import Path

def clean_orphaned_braces():
    base_path = Path('products')
    md_files = list(base_path.rglob('*.md'))
    
    files_cleaned = 0
    total_braces_removed = 0
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 移除孤立的{ 字符（独立成行的）
            content = re.sub(r'^\s*\{\s*$', '', content, flags=re.MULTILINE)
            
            # 移除多余的空行（超过两个连续空行合并为两个）
            content = re.sub(r'\n\n\n+', '\n\n', content)
            
            if content != original_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # 计算删除的{ 数量
                removed_count = len(re.findall(r'^\s*\{\s*$', original_content, re.MULTILINE))
                if removed_count > 0:
                    print(f"  {md_file}: 删除 {removed_count} 个孤立的{{字符")
                    files_cleaned += 1
                    total_braces_removed += removed_count
                    
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    print(f"\n清理完成:")
    print(f"  处理文件数: {files_cleaned}")
    print(f"  删除的{{字符总数: {total_braces_removed}")

if __name__ == "__main__":
    clean_orphaned_braces()