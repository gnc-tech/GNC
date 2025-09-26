#!/usr/bin/env python3
"""
更稳健的React表格转换脚本
按照用户建议：分段提取headers和rows，然后重组处理
"""

import re
import ast
from pathlib import Path

def extract_and_convert_table(text_block):
    """分段提取headers和rows，重组后转换为Markdown表格"""
    try:
        # 1. 分别提取headers和rows
        headers_match = re.search(r'headers:\s*(\[.*?\])', text_block, re.DOTALL)
        rows_match = re.search(r'rows:\s*(\[.*?\])', text_block, re.DOTALL)
        
        if not headers_match or not rows_match:
            print(f"  ❌ Could not find headers or rows")
            return text_block
        
        headers_text = headers_match.group(1)
        rows_text = rows_match.group(1)
        
        # 2. 清洗和标准化
        # 将单引号替换为双引号
        headers_clean = headers_text.replace("'", '"')
        rows_clean = rows_text.replace("'", '"')
        
        # 3. 解析为Python对象 - 直接解析，不重组JSON
        headers = ast.literal_eval(headers_clean)
        rows = ast.literal_eval(rows_clean)
        
        if not headers or not rows:
            print(f"  ❌ Empty headers or rows")
            return text_block
        
        # 5. 生成Markdown表格
        lines = []
        
        # 表头行
        header_row = '| ' + ' | '.join(headers) + ' |'
        lines.append(header_row)
        
        # 分隔行
        separator = '| ' + ' | '.join(['---'] * len(headers)) + ' |'
        lines.append(separator)
        
        # 数据行
        for row in rows:
            # 确保列数匹配
            while len(row) < len(headers):
                row.append('')
            if len(row) > len(headers):
                row = row[:len(headers)]
            
            row_str = '| ' + ' | '.join(str(cell) for cell in row) + ' |'
            lines.append(row_str)
        
        return '\n'.join(lines)
        
    except Exception as e:
        print(f"  ❌ Error converting table: {e}")
        return text_block

def fix_react_tables_robust(file_path):
    """更稳健地修复React表格"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 更准确的匹配模式：确保提取完整的数组
        pattern = r'headers:\s*(\[.*?\]),\s*\n\s*rows:\s*(\[(?:[^\[\]]*|\[[^\]]*\])*\])'
        
        tables_converted = 0
        
        def replace_table(match):
            nonlocal tables_converted
            # 直接使用正则组，不再调用extract函数
            headers_text = match.group(1)
            rows_text = match.group(2)
            
            try:
                # 清理并解析
                headers_clean = headers_text.replace("'", '"')
                rows_clean = rows_text.replace("'", '"')
                
                headers = ast.literal_eval(headers_clean)
                rows = ast.literal_eval(rows_clean)
                
                # 生成Markdown表格
                lines = []
                header_row = '| ' + ' | '.join(headers) + ' |'
                lines.append(header_row)
                separator = '| ' + ' | '.join(['---'] * len(headers)) + ' |'
                lines.append(separator)
                
                for row in rows:
                    while len(row) < len(headers):
                        row.append('')
                    if len(row) > len(headers):
                        row = row[:len(headers)]
                    row_str = '| ' + ' | '.join(str(cell) for cell in row) + ' |'
                    lines.append(row_str)
                
                tables_converted += 1
                return '\n'.join(lines)
                
            except Exception as e:
                print(f"  ❌ Error converting table: {e}")
                return match.group(0)
        
        content = re.sub(pattern, replace_table, content, flags=re.MULTILINE | re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Converted {tables_converted} React tables to Markdown")
            return True
        else:
            tables_found = len(re.findall(pattern, original_content, re.MULTILINE | re.DOTALL))
            if tables_found > 0:
                print(f"  ⚠️  Found {tables_found} tables but couldn't convert them")
            else:
                print(f"  ℹ️  No React tables found")
            return False
            
    except Exception as e:
        print(f"  ❌ Error processing file: {e}")
        return False

def main():
    """处理剩余的React表格文件"""
    # 手动指定需要处理的文件（基于之前的统计）
    target_files = [
        "products/navigation-systems/mems-inertial-devices/gyroscopes/mems-gyroscope-advanced-dg073-083.md",
        "products/navigation-systems/mems-inertial-devices/gyroscopes/mems-gyroscope-tactical-grade-ltm210s10.md",
        "products/navigation-systems/mems-inertial-devices/imus/mems-imu-10-dof-cgm92ad10.md",
        "products/navigation-systems/mems-inertial-devices/imus/mems-imu-3-axis-cgm66ek10.md",
        "products/navigation-systems/mems-inertial-devices/imus/mems-imu-6-dof-cgm91ad10.md",
        "products/navigation-systems/mems-inertial-devices/imus/mems-imu-tactical-grade-cgm300s10.md",
        "products/navigation-systems/quartz-accelerometers/qac-accelerometer-flexure-bjgm25a01.md",
        "products/navigation-systems/quartz-accelerometers/qac-accelerometer-flexure-jdsj18tk01.md",
        "products/navigation-systems/quartz-accelerometers/qac-accelerometer-flexure-jdsj25tk01.md",
        "products/navigation-systems/quartz-accelerometers/qac-accelerometer-flexure-jdsj25tk02.md",
        "products/navigation-systems/quartz-accelerometers/qac-accelerometer-miniature-bjgm18t01.md",
        "products/navigation-systems/quartz-accelerometers/qac-accelerometer-navigation-bjgm25n01.md",
        "products/navigation-systems/mems-inertial-devices/gyroscopes/quartz-mems-gyroscope-lttb10cj01.md",
        "products/navigation-systems/mems-inertial-devices/gyroscopes/quartz-mems-gyroscope-lttb10cj02.md",
        "products/navigation-systems/mems-inertial-devices/gyroscopes/quartz-mems-gyroscope-ltys11cj01.md",
        "products/navigation-systems/mems-inertial-devices/gyroscopes/quartz-mems-gyroscope-ltys11cj02.md",
        "products/navigation-systems/mems-inertial-devices/gyroscopes/quartz-mems-gyroscope-ltys11cj1x.md",
        "products/navigation-systems/mems-inertial-devices/gyroscopes/quartz-mems-gyroscope-ltys12cj1x.md",
        "products/navigation-systems/mems-inertial-devices/gyroscopes/quartz-mems-gyroscope-ltys12cj2x.md",
        "products/navigation-systems/mems-inertial-devices/gyroscopes/quartz-mems-gyroscope-ltys13cj1x.md",
        "products/navigation-systems/mems-inertial-devices/gyroscopes/quartz-mems-gyroscope-ltys13cj2a.md",
        "products/navigation-systems/mems-inertial-devices/imus/quartz-mems-imu-cgsm40cj1.md",
        "products/navigation-systems/mems-inertial-devices/imus/quartz-mems-imu-cgys30cj1x.md",
        "products/navigation-systems/mems-inertial-devices/imus/quartz-mems-imu-cgys30cj2x.md",
        "products/navigation-systems/mems-inertial-devices/imus/quartz-mems-imu-cgys30cj3x.md",
        "products/navigation-systems/quartz-mems-devices/navigation-grade/quartz-mems-nav-dgys60cj10.md",
        "products/navigation-systems/quartz-mems-devices/navigation-grade/quartz-mems-nav-hdtd80cj1x.md",
        "products/navigation-systems/quartz-mems-devices/navigation-grade/quartz-mems-nav-hdts90cj1x.md",
        "products/navigation-systems/quartz-mems-devices/navigation-grade/quartz-mems-nav-jqys50cj1a.md",
        "products/navigation-systems/quartz-mems-devices/navigation-grade/quartz-mems-nav-zhys70cj10.md"
    ]
    
    print(f"处理 {len(target_files)} 个包含React表格的文件\n")
    
    files_processed = 0
    files_fixed = 0
    
    for file_path in target_files:
        path_obj = Path(file_path)
        if path_obj.exists():
            print(f"Processing: {path_obj}")
            files_processed += 1
            if fix_react_tables_robust(path_obj):
                files_fixed += 1
        else:
            print(f"File not found: {path_obj}")
    
    print(f"\n处理完成:")
    print(f"  处理文件数: {files_processed}")
    print(f"  修复文件数: {files_fixed}")

if __name__ == "__main__":
    main()