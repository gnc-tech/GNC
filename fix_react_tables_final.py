#!/usr/bin/env python3
"""
Extract headers and rows from React tables and reformat as Markdown tables.
Direct approach: find the data, extract it, rebuild as Markdown.
"""

import re
from pathlib import Path

def extract_and_convert_table(table_match):
    """Extract headers and rows from React table format and convert to Markdown"""
    table_text = table_match.group(0)
    
    # Extract headers using regex
    headers_match = re.search(r"headers:\s*\[(.*?)\]", table_text, re.DOTALL)
    if not headers_match:
        return table_text
    
    headers_content = headers_match.group(1)
    # Extract all quoted strings as headers
    headers = re.findall(r"'([^']*)'", headers_content)
    
    if not headers:
        return table_text
    
    # Extract rows using regex
    rows_match = re.search(r"rows:\s*\[(.*?)\]", table_text, re.DOTALL)
    if not rows_match:
        return table_text
    
    rows_content = rows_match.group(1)
    
    # Find all row arrays [...]
    row_pattern = r"\[\s*([^\]]+)\s*\]"
    row_matches = re.findall(row_pattern, rows_content)
    
    rows = []
    for row_match in row_matches:
        # Skip comment lines
        if row_match.strip().startswith('//'):
            continue
        
        # Extract all quoted values in this row
        cells = re.findall(r"'([^']*)'", row_match)
        if cells:
            rows.append(cells)
    
    if not rows:
        return table_text
    
    # Build Markdown table
    markdown_lines = []
    
    # Header row
    markdown_lines.append('| ' + ' | '.join(headers) + ' |')
    
    # Separator row
    markdown_lines.append('|' + '---|' * len(headers))
    
    # Data rows
    for row in rows:
        # Ensure row has correct number of columns
        while len(row) < len(headers):
            row.append('')
        if len(row) > len(headers):
            row = row[:len(headers)]
        
        markdown_lines.append('| ' + ' | '.join(row) + ' |')
    
    return '\n'.join(markdown_lines)

def fix_react_tables_in_file(file_path):
    """Fix all React tables in a markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to match React table structure starting with '{'
        # Look for { followed by headers: [...], rows: [...] ending with ]
        pattern = r'\{\s*\nheaders:\s*\[.*?\],\s*\nrows:\s*\[.*?\]\s*\n'
        
        # Replace all matches
        new_content = re.sub(pattern, extract_and_convert_table, content, flags=re.DOTALL | re.MULTILINE)
        
        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Count conversions
            original_tables = len(re.findall(r'\{\s*\nheaders:', original_content, re.MULTILINE))
            remaining_tables = len(re.findall(r'\{\s*\nheaders:', new_content, re.MULTILINE))
            converted = original_tables - remaining_tables
            
            print(f"  ✅ Converted {converted} React tables to Markdown")
            return True
        else:
            tables_found = len(re.findall(r'\{\s*\nheaders:', content, re.MULTILINE))
            if tables_found > 0:
                print(f"  ⚠️  Found {tables_found} React tables but couldn't convert")
            else:
                print(f"  ℹ️  No React tables found")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Process all markdown files"""
    base_path = Path('products')
    
    if not base_path.exists():
        print("❌ Products directory not found")
        return
    
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