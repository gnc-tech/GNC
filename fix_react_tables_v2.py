#!/usr/bin/env python3
"""
Fix React component table format to standard Markdown tables.
- Remove leading '{' character
- Convert React table format to Markdown table format
"""

import re
from pathlib import Path

def convert_react_table_to_markdown(table_text):
    """Convert React component table format to Markdown table"""
    try:
        # Extract headers
        headers_match = re.search(r'headers:\s*\[(.*?)\]', table_text, re.DOTALL)
        if not headers_match:
            print(f"  ❌ Could not find headers")
            return table_text
        
        headers_str = headers_match.group(1)
        headers = re.findall(r"'([^']*)'", headers_str)
        
        if not headers:
            print(f"  ❌ No headers found")
            return table_text
        
        # Extract rows
        rows_match = re.search(r'rows:\s*\[(.*?)\]', table_text, re.DOTALL)
        if not rows_match:
            print(f"  ❌ Could not find rows")
            return table_text
        
        rows_str = rows_match.group(1)
        rows = []
        
        # Find all individual row arrays
        row_arrays = re.findall(r'\[\s*([^\]]+)\s*\]', rows_str)
        
        for row_array in row_arrays:
            if '//' in row_array:  # Skip comment lines
                continue
            
            # Extract cell values from each row
            cells = re.findall(r"'([^']*)'", row_array)
            if cells:
                rows.append(cells)
        
        if not rows:
            print(f"  ❌ No valid rows found")
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
        
    except Exception as e:
        print(f"  ❌ Error converting table: {e}")
        return table_text

def fix_react_tables_in_file(file_path):
    """Fix all React tables in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match the React table structure
        # Looks for lines starting with '{' followed by headers and rows
        pattern = r'^\{\s*\nheaders:\s*\[.*?\],\s*\nrows:\s*\[.*?\]\s*\n(?=\s*$|\n)'
        
        tables_found = 0
        tables_fixed = 0
        
        def replace_table(match):
            nonlocal tables_found, tables_fixed
            tables_found += 1
            
            table_text = match.group(0)
            markdown_table = convert_react_table_to_markdown(table_text)
            
            if markdown_table != table_text:
                tables_fixed += 1
                return markdown_table
            else:
                return table_text
        
        new_content = re.sub(pattern, replace_table, content, flags=re.MULTILINE | re.DOTALL)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✅ Fixed {tables_fixed}/{tables_found} tables")
            return True
        else:
            if tables_found > 0:
                print(f"  ⚠️  Found {tables_found} tables but no changes made")
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