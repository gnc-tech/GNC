#!/usr/bin/env python3
"""
Fix React component table format to standard Markdown tables.
- Remove leading '{' character
- Convert React table format to Markdown table format
"""

import re
import json
from pathlib import Path

def convert_react_table_to_markdown(react_table_text):
    """Convert React component table format to Markdown table"""
    try:
        # Extract headers and rows using regex
        headers_match = re.search(r'headers:\s*\[(.*?)\]', react_table_text, re.DOTALL)
        rows_match = re.search(r'rows:\s*\[(.*?)\]', react_table_text, re.DOTALL | re.MULTILINE)
        
        if not headers_match or not rows_match:
            print(f"  ❌ Could not parse table structure")
            return react_table_text
        
        # Parse headers
        headers_str = headers_match.group(1)
        headers = []
        for header in re.findall(r"'([^']*)'", headers_str):
            headers.append(header)
        
        # Parse rows
        rows_str = rows_match.group(1)
        rows = []
        
        # Find all row arrays
        row_pattern = r'\[\s*([^\]]+)\s*\]'
        row_matches = re.findall(row_pattern, rows_str, re.DOTALL)
        
        for row_match in row_matches:
            # Skip comments and empty matches
            if row_match.strip().startswith('//') or not row_match.strip():
                continue
            
            # Extract individual cell values
            cell_pattern = r"'([^']*)'"
            row_cells = re.findall(cell_pattern, row_match)
            
            if row_cells:  # Only add non-empty rows
                rows.append(row_cells)
        
        # Build Markdown table
        if not headers or not rows:
            print(f"  ❌ No valid headers or rows found")
            return react_table_text
        
        markdown_lines = []
        
        # Header row
        header_row = '| ' + ' | '.join(headers) + ' |'
        markdown_lines.append(header_row)
        
        # Separator row
        separator = '|' + '---|' * len(headers)
        markdown_lines.append(separator)
        
        # Data rows
        for row in rows:
            # Pad row with empty cells if needed
            while len(row) < len(headers):
                row.append('')
            
            # Truncate row if it has too many cells
            if len(row) > len(headers):
                row = row[:len(headers)]
            
            row_str = '| ' + ' | '.join(row) + ' |'
            markdown_lines.append(row_str)
        
        return '\n'.join(markdown_lines)
        
    except Exception as e:
        print(f"  ❌ Error converting table: {e}")
        return react_table_text

def fix_react_tables_in_file(file_path):
    """Fix all React tables in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match React table format starting with '{'
        # This pattern looks for { followed by headers and rows
        pattern = r'\{\s*\nheaders:\s*\[.*?\],\s*\nrows:\s*\[.*?\]\n\}'
        
        tables_found = 0
        tables_fixed = 0
        
        def replace_table(match):
            nonlocal tables_found, tables_fixed
            tables_found += 1
            
            table_text = match.group(1)
            markdown_table = convert_react_table_to_markdown(table_text)
            
            if markdown_table != table_text:
                tables_fixed += 1
                return markdown_table
            else:
                return table_text
        
        new_content = re.sub(pattern, replace_table, content, flags=re.DOTALL | re.MULTILINE)
        
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