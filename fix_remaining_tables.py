#!/usr/bin/env python3
"""
Final cleanup script to convert all remaining React tables to Markdown.
This script handles various edge cases and formats.
"""

import re
import ast
from pathlib import Path

def convert_simple_react_table_final(table_text):
    """Convert React table text to Markdown - handles various formats"""
    try:
        # Clean up the text - remove extra whitespace and comments
        lines = table_text.strip().split('\n')
        cleaned_lines = []
        
        in_headers = False
        in_rows = False
        headers = []
        rows = []
        
        for line in lines:
            line = line.strip()
            
            # Skip comment lines
            if line.startswith('//') or not line:
                continue
                
            # Extract headers
            if 'headers:' in line:
                in_headers = True
                # Extract headers from this line if they're on the same line
                headers_match = re.search(r'headers:\s*\[(.*?)\]', line, re.DOTALL)
                if headers_match:
                    headers_str = headers_match.group(1)
                    headers = [h.strip("'\" ") for h in re.findall(r"'([^']*)'|\"([^\"]*)\"", headers_str)]
                    if not headers:  # Try alternative parsing
                        headers = [h.strip("'\" ") for h in headers_str.split(',')]
                continue
            
            # Extract rows
            if 'rows:' in line:
                in_rows = True
                continue
                
            # Process data rows
            if in_rows and line.startswith('[') and (line.endswith('],') or line.endswith(']')):
                # Extract cell values
                row_content = line.strip('[](),')
                cells = []
                
                # Handle quoted strings
                for match in re.finditer(r"'([^']*)'|\"([^\"]*)\"", row_content):
                    cell = match.group(1) or match.group(2)
                    cells.append(cell)
                
                if cells:
                    rows.append(cells)
        
        # If we couldn't parse headers/rows from the multiline format, try single-line parsing
        if not headers or not rows:
            # Try to extract as a complete object
            clean_text = table_text.replace('\n', ' ')
            # Remove comments
            clean_text = re.sub(r'//[^,\]]*', '', clean_text)
            
            headers_match = re.search(r'headers:\s*\[(.*?)\]', clean_text)
            rows_match = re.search(r'rows:\s*\[(.*?)\]', clean_text, re.DOTALL)
            
            if headers_match:
                headers_str = headers_match.group(1)
                headers = [h.strip("'\" ") for h in re.findall(r"'([^']*)'|\"([^\"]*)\"", headers_str)]
                
            if rows_match:
                rows_str = rows_match.group(1)
                # Find all row arrays
                row_arrays = re.findall(r'\[(.*?)\]', rows_str)
                for row_array in row_arrays:
                    cells = [c.strip("'\" ") for c in re.findall(r"'([^']*)'|\"([^\"]*)\"", row_array)]
                    if cells:
                        rows.append(cells)
        
        if not headers or not rows:
            print(f"  ❌ Could not extract headers or rows")
            return table_text
        
        # Build Markdown table
        lines = []
        
        # Header row  
        header_row = '| ' + ' | '.join(headers) + ' |'
        lines.append(header_row)
        
        # Separator row
        separator = '| ' + ' | '.join(['---'] * len(headers)) + ' |'
        lines.append(separator)
        
        # Data rows
        for row in rows:
            # Ensure row has same number of columns
            while len(row) < len(headers):
                row.append('')
            if len(row) > len(headers):
                row = row[:len(headers)]
            
            row_str = '| ' + ' | '.join(str(cell) for cell in row) + ' |'
            lines.append(row_str)
        
        return '\n'.join(lines)
        
    except Exception as e:
        print(f"  ❌ Error converting table: {e}")
        return table_text

def fix_remaining_react_tables(file_path):
    """Fix all remaining React tables in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # More flexible pattern to catch various React table formats
        patterns = [
            r'\{\s*\n\s*headers:\s*\[.*?\],\s*\n\s*rows:\s*\[.*?\]\s*\n\s*\}',  # Complete tables with closing brace
            r'\{\s*\n\s*headers:\s*\[.*?\],\s*\n\s*rows:\s*\[.*?\]\s*\n(?=\s*\n|\s*#|\s*$)',  # Tables without closing brace
            r'headers:\s*\[.*?\],\s*\n\s*rows:\s*\[.*?\](?=\s*\n|\s*$)',  # Tables without opening brace
        ]
        
        tables_converted = 0
        
        for pattern in patterns:
            def replace_table(match):
                nonlocal tables_converted
                table_text = match.group(0)
                markdown_table = convert_simple_react_table_final(table_text)
                if markdown_table != table_text:
                    tables_converted += 1
                return markdown_table
            
            content = re.sub(pattern, replace_table, content, flags=re.MULTILINE | re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Converted {tables_converted} React tables to Markdown")
            return True
        else:
            print(f"  ℹ️  No React tables found or converted")
            return False
            
    except Exception as e:
        print(f"  ❌ Error processing file: {e}")
        return False

def main():
    """Process all remaining files"""
    base_path = Path('products')
    
    if not base_path.exists():
        print("❌ Products directory not found")
        return
    
    # Get files that still have React tables
    files_with_tables = []
    
    for md_file in base_path.rglob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'headers:' in content and '[' in content:
                    files_with_tables.append(md_file)
        except:
            continue
    
    print(f"Found {len(files_with_tables)} files with remaining React tables\n")
    
    files_processed = 0
    files_fixed = 0
    
    for md_file in files_with_tables:
        print(f"Processing: {md_file}")
        
        files_processed += 1
        if fix_remaining_react_tables(md_file):
            files_fixed += 1
    
    print(f"\nProcessing complete:")
    print(f"  Files processed: {files_processed}")
    print(f"  Files fixed: {files_fixed}")

if __name__ == "__main__":
    main()