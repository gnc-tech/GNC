#!/usr/bin/env python3
"""
Fix React component table format to standard Markdown tables.
Simple approach using string manipulation and manual parsing.
"""

import re
from pathlib import Path

def convert_simple_react_table(table_text):
    """Convert a simple React table to Markdown"""
    lines = table_text.strip().split('\n')
    
    # Find headers line
    headers_line = None
    rows_start = None
    
    for i, line in enumerate(lines):
        if 'headers:' in line:
            headers_line = line
        elif 'rows:' in line:
            rows_start = i
            break
    
    if not headers_line or rows_start is None:
        return table_text
    
    # Extract headers
    headers_match = re.search(r'\[(.*?)\]', headers_line)
    if not headers_match:
        return table_text
    
    headers_str = headers_match.group(1)
    headers = [h.strip("'\" ") for h in headers_str.split(',')]
    
    # Extract rows
    rows = []
    for i in range(rows_start + 1, len(lines)):
        line = lines[i].strip()
        if line.startswith('[') and line.endswith('],'):
            # Remove the brackets and trailing comma
            row_content = line[1:-2]  # Remove [ and ],
            # Split by comma and clean up
            cells = []
            current_cell = ""
            quote_char = None
            
            for char in row_content:
                if char in ["'", '"'] and quote_char is None:
                    quote_char = char
                elif char == quote_char:
                    quote_char = None
                elif char == ',' and quote_char is None:
                    cells.append(current_cell.strip("'\" "))
                    current_cell = ""
                    continue
                
                if quote_char is not None and char != quote_char:
                    current_cell += char
            
            # Add the last cell
            if current_cell:
                cells.append(current_cell.strip("'\" "))
            
            if cells:
                rows.append(cells)
        elif line.startswith(']'):
            break
    
    if not headers or not rows:
        return table_text
    
    # Build Markdown table
    markdown_lines = []
    
    # Header row
    header_row = '| ' + ' | '.join(headers) + ' |'
    markdown_lines.append(header_row)
    
    # Separator row
    separator = '|' + '---|' * len(headers)
    markdown_lines.append(separator)
    
    # Data rows
    for row in rows:
        # Ensure row has same number of columns as headers
        while len(row) < len(headers):
            row.append('')
        if len(row) > len(headers):
            row = row[:len(headers)]
        
        row_str = '| ' + ' | '.join(row) + ' |'
        markdown_lines.append(row_str)
    
    return '\n'.join(markdown_lines)

def fix_react_tables_in_file(file_path):
    """Fix all React tables in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Find and replace all React table patterns
        # Pattern matches: { followed by headers: [...], followed by rows: [...]
        pattern = r'^\{\s*\nheaders:\s*\[.*?\],\s*\nrows:\s*\[\s*\n(.*?\n)*?\s*\]'
        
        def replace_table(match):
            table_text = match.group(0)
            markdown_table = convert_simple_react_table(table_text)
            return markdown_table
        
        content = re.sub(pattern, replace_table, content, flags=re.MULTILINE | re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Count how many tables were converted
            original_tables = len(re.findall(r'^\{\s*\nheaders:', original_content, re.MULTILINE))
            remaining_tables = len(re.findall(r'^\{\s*\nheaders:', content, re.MULTILINE))
            converted = original_tables - remaining_tables
            
            print(f"  ✅ Converted {converted} React tables to Markdown")
            return True
        else:
            # Check if there are any React tables that couldn't be converted
            tables_found = len(re.findall(r'^\{\s*\nheaders:', content, re.MULTILINE))
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
    
    # Find all markdown files
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