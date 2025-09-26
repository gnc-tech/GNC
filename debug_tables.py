#!/usr/bin/env python3
"""
调试脚本：查看提取到的具体内容
"""

import re
from pathlib import Path

def debug_extract_table(file_path, max_tables=2):
    """调试表格提取"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更宽松的匹配模式
        pattern = r'headers:\s*\[.*?\],\s*\n\s*rows:\s*\[.*?\](?=\s*\n\s*(?:\}|\n|##|###|$))'
        
        matches = re.findall(pattern, content, flags=re.MULTILINE | re.DOTALL)
        
        print(f"\n文件: {file_path}")
        print(f"找到 {len(matches)} 个表格")
        
        for i, match in enumerate(matches[:max_tables]):
            print(f"\n=== 表格 {i+1} ===")
            print("原始匹配内容:")
            print(repr(match))
            print("\n显示内容:")
            print(match)
            
            # 尝试分段提取
            headers_match = re.search(r'headers:\s*(\[.*?\])', match, re.DOTALL)
            rows_match = re.search(r'rows:\s*(\[.*?\])', match, re.DOTALL)
            
            if headers_match:
                print(f"\nHeaders提取: {repr(headers_match.group(1))}")
            if rows_match:
                print(f"\nRows提取前100字符: {repr(rows_match.group(1)[:100])}")
                
    except Exception as e:
        print(f"Error: {e}")

# 测试几个文件
test_files = [
    "products/navigation-systems/mems-inertial-devices/gyroscopes/mems-gyroscope-advanced-dg073-083.md",
    "products/navigation-systems/mems-inertial-devices/gyroscopes/mems-gyroscope-tactical-grade-ltm210s10.md"
]

for file_path in test_files:
    path_obj = Path(file_path)
    if path_obj.exists():
        debug_extract_table(path_obj, 1)