#!/usr/bin/env python3
"""
Comprehensive React table to Markdown converter.
Handles all variations of React table formats.
"""

import re
from pathlib import Path

def convert_react_table_comprehensive(content):
    """Convert all React tables in content to Markdown tables"""
    
    def extract_headers_and_rows(table_text):
        """Extract headers and rows from React table text"""
        # Extract headers - handle both single-line and multi-line formats
        headers_match = re.search(r'headers:\s*\[(.*?)\]', table_text, re.DOTALL)
        if not headers_match:
            return None, None
        
        headers_content = headers_match.group(1)
        # Find all quoted strings in headers
        headers = []
        for match in re.finditer(r"'([^']*)'", headers_content):
            headers.append(match.group(1))
        
        if not headers:
            return None, None
        
        # Extract rows - handle multi-line with comments
        rows_match = re.search(r'rows:\s*\[(.*?)\]', table_text, re.DOTALL)
        if not rows_match:
            return None, None
        
        rows_content = rows_match.group(1)
        
        # Find all row arrays, skipping comment lines
        rows = []
        # Split by lines and process each
        lines = rows_content.split('\n')
        current_row = []
        in_array = False
        
        for line in lines:
            line = line.strip()
            
            # Skip comment lines
            if line.startswith('//'):
                continue
            
            # Check if this line starts a new array
            if line.startswith('['):
                in_array = True
                current_row = []
                # Extract content from this line
                content_line = line[1:]  # Remove opening bracket
                if content_line.endswith('],'):
                    content_line = content_line[:-2]  # Remove closing bracket and comma
                    in_array = False
                elif content_line.endswith(']'):
                    content_line = content_line[:-1]  # Remove closing bracket
                    in_array = False
                
                # Extract quoted values from this line
                cells = re.findall(r"'([^']*)'", content_line)
                current_row.extend(cells)
                
                if not in_array and current_row:
                    rows.append(current_row)
                    current_row = []
            
            elif in_array:
                # Continue processing array content
                if line.endswith('],'):
                    line = line[:-2]  # Remove closing bracket and comma
                    in_array = False
                elif line.endswith(']'):
                    line = line[:-1]  # Remove closing bracket
                    in_array = False
                
                # Extract quoted values from this line
                cells = re.findall(r"'([^']*)'", line)
                current_row.extend(cells)
                
                if not in_array and current_row:
                    rows.append(current_row)
                    current_row = []
        
        return headers, rows
    
    def build_markdown_table(headers, rows):
        """Build Markdown table from headers and rows"""
        if not headers or not rows:
            return None
        
        lines = []
        
        # Header row
        lines.append('| ' + ' | '.join(headers) + ' |')
        
        # Separator row
        lines.append('|' + '---|' * len(headers))
        
        # Data rows
        for row in rows:
            # Ensure correct number of columns
            while len(row) < len(headers):
                row.append('')
            if len(row) > len(headers):
                row = row[:len(headers)]
            
            lines.append('| ' + ' | '.join(row) + ' |')
        
        return '\n'.join(lines)
    
    # Pattern to match React tables - very flexible
    pattern = r'\{\s*\n\s*headers:\s*\[.*?\],\s*\n\s*rows:\s*\[.*?\]\s*\n.*?(?=\n\s*(?:\n|#|####|\Z))'
    
    def replace_table(match):
        table_text = match.group(0)
        headers, rows = extract_headers_and_rows(table_text)
        
        if headers and rows:
            markdown_table = build_markdown_table(headers, rows)
            if markdown_table:
                return markdown_table + '\n'
        
        return table_text
    
    # Apply replacements
    new_content = re.sub(pattern, replace_table, content, flags=re.DOTALL | re.MULTILINE)
    
    return new_content

def process_file(file_path):
    """Process a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        new_content = convert_react_table_comprehensive(original_content)
        
        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Count conversions
            original_tables = len(re.findall(r'headers:', original_content))
            remaining_tables = len(re.findall(r'headers:', new_content))
            converted = original_tables - remaining_tables
            
            if converted > 0:
                print(f"  ✅ Converted {converted} tables")
                return True
        
        # Check for remaining tables
        remaining_tables = len(re.findall(r'headers:', new_content))
        if remaining_tables > 0:
            print(f"  ⚠️  {remaining_tables} tables still need conversion")
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
    files_converted = 0
    total_converted = 0
    
    for md_file in md_files:
        print(f"Processing: {md_file}")
        files_processed += 1
        
        if process_file(md_file):
            files_converted += 1
    
    print(f"\nProcessing complete:")
    print(f"  Files processed: {files_processed}")
    print(f"  Files with conversions: {files_converted}")

if __name__ == "__main__":
    main()