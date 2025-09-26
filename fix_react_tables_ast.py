#!/usr/bin/env python3
"""
Fix React component table format to standard Markdown tables.
Based on user's AST parsing approach.
"""

import re
import ast
from pathlib import Path

def convert_react_table_to_markdown(table_block):
    """Convert React table block to Markdown using AST parsing"""
    try:
        # 标准化成 Python 可解析字典
        # - 键名补上双引号
        # - 单引号改为双引号  
        # - 在末尾补上右大括号
        clean = re.sub(r"(\w+):", r'"\1":', table_block)  # headers: -> "headers":
        clean = clean.replace("'", '"') + "}"
        
        # 转为 Python dict
        data = ast.literal_eval(clean)
        
        if "headers" not in data or "rows" not in data:
            print(f"  ❌ Missing headers or rows in table")
            return table_block
        
        headers = data["headers"]
        rows = data["rows"]
        
        if not headers or not rows:
            print(f"  ❌ Empty headers or rows")
            return table_block
        
        # 生成 Markdown 表格
        lines = []
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        
        for row in rows:
            # 确保行有足够的列
            while len(row) < len(headers):
                row.append('')
            if len(row) > len(headers):
                row = row[:len(headers)]
            
            lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
        
        return "\n".join(lines)
        
    except Exception as e:
        print(f"  ❌ Error parsing table: {e}")
        return table_block

def fix_react_tables_in_file(file_path):
    """Fix all React tables in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 提取 { ... ] 这一段的正则表达式，更精确地匹配
        pattern = r"\{\s*\nheaders:\s*\[.*?\],\s*\nrows:\s*\[.*?\]\s*\n(?=\s*\n|\s*$)"
        
        def replace_table(match):
            table_block = match.group(0)
            markdown_table = convert_react_table_to_markdown(table_block)
            return markdown_table
        
        content = re.sub(pattern, replace_table, content, flags=re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 计算转换了多少个表格
            original_tables = len(re.findall(pattern, original_content, re.DOTALL))
            remaining_tables = len(re.findall(pattern, content, re.DOTALL))
            converted = original_tables - remaining_tables
            
            print(f"  ✅ Converted {converted} React tables to Markdown")
            return True
        else:
            # 检查是否有无法转换的React表格
            tables_found = len(re.findall(pattern, content, re.DOTALL))
            if tables_found > 0:
                print(f"  ⚠️  Found {tables_found} React tables but couldn't convert them")
            else:
                print(f"  ℹ️  No React tables found")
            return False
            
    except Exception as e:
        print(f"  ❌ Error processing file: {e}")
        return False

def main():
    """Main function to process all markdown files"""
    base_path = Path('products')
    
    if not base_path.exists():
        print("❌ Products directory not found")
        return
    
    # 找到所有markdown文件
    md_files = list(base_path.rglob('*.md'))
    
    print(f"Found {len(md_files)} markdown files to process\n")
    
    files_processed = 0
    files_fixed = 0
    
    for md_file in md_files:
        print(f"Processing: {md_file}")
        
        files_processed += 1
        if fix_react_tables_in_file(md_file):
            files_fixed += 1
    
    print(f"\nProcessing complete:")
    print(f"  Files processed: {files_processed}")
    print(f"  Files fixed: {files_fixed}")

if __name__ == "__main__":
    main()