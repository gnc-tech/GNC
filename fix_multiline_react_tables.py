#!/usr/bin/env python3
"""
Fix remaining multi-line React component table format to standard Markdown tables.
"""

import re
import ast
from pathlib import Path

def convert_multiline_react_table(table_block):
    """Convert multi-line React table block to Markdown using AST parsing"""
    try:
        # 移除额外的缩进和格式化
        lines = table_block.strip().split('\n')
        cleaned_lines = []
        
        for line in lines:
            # 移除行首空格和缩进
            cleaned_line = line.strip()
            if cleaned_line:
                cleaned_lines.append(cleaned_line)
        
        # 重新组合成一行
        cleaned_text = ' '.join(cleaned_lines)
        
        # 标准化成 Python 可解析字典
        clean = re.sub(r"(\w+):", r'"\1":', cleaned_text)  # headers: -> "headers":
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
        print(f"  ❌ Error parsing multi-line table: {e}")
        return table_block

def fix_multiline_react_tables_in_file(file_path):
    """Fix all multi-line React tables in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 匹配多行格式的React表格
        # 从 { 开始，包含 headers: 和 rows:，直到匹配的 ]
        pattern = r'\{\s*\n\s*headers:\s*\[\s*\n.*?\],\s*\n\s*rows:\s*\[\s*\n.*?\n\s*\]\s*\n'
        
        def replace_table(match):
            table_block = match.group(0)
            markdown_table = convert_multiline_react_table(table_block)
            return markdown_table
        
        content = re.sub(pattern, replace_table, content, flags=re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 计算转换了多少个表格
            original_tables = len(re.findall(pattern, original_content, re.DOTALL))
            remaining_tables = len(re.findall(pattern, content, re.DOTALL))
            converted = original_tables - remaining_tables
            
            print(f"  ✅ Converted {converted} multi-line React tables to Markdown")
            return True
        else:
            # 检查是否有无法转换的React表格
            tables_found = len(re.findall(pattern, content, re.DOTALL))
            if tables_found > 0:
                print(f"  ⚠️  Found {tables_found} multi-line React tables but couldn't convert them")
            else:
                print(f"  ℹ️  No multi-line React tables found")
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
        if fix_multiline_react_tables_in_file(md_file):
            files_fixed += 1
    
    print(f"\nProcessing complete:")
    print(f"  Files processed: {files_processed}")
    print(f"  Files fixed: {files_fixed}")

if __name__ == "__main__":
    main()