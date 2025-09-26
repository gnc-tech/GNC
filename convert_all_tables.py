#!/usr/bin/env python3
"""
Convert all React component tables to standard Markdown tables.
Uses multi_replace_string_in_file for efficient batch processing.
"""

import re
from pathlib import Path
import json

def parse_react_table(table_text):
    """Parse React table and return headers and rows"""
    # Extract headers
    headers_match = re.search(r"headers:\s*\[(.*?)\]", table_text, re.DOTALL)
    if not headers_match:
        return None, None
    
    headers_content = headers_match.group(1)
    headers = re.findall(r"'([^']*)'", headers_content)
    
    if not headers:
        return None, None
    
    # Extract rows
    rows_match = re.search(r"rows:\s*\[(.*?)\]", table_text, re.DOTALL)
    if not rows_match:
        return None, None
    
    rows_content = rows_match.group(1)
    
    # Find all row arrays
    rows = []
    row_pattern = r"\[\s*([^\]]+)\s*\]"
    row_matches = re.findall(row_pattern, rows_content)
    
    for row_match in row_matches:
        # Skip comments
        if '//' in row_match:
            continue
        
        # Extract quoted values
        cells = re.findall(r"'([^']*)'", row_match)
        if cells:
            rows.append(cells)
    
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

def find_react_tables_in_file(file_path):
    """Find all React tables in a file and return replacement operations"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        replacements = []
        
        # Pattern to find React tables - more flexible to handle different formats
        pattern = r'\{\s*\n\s*headers:\s*\[.*?\],\s*\n\s*rows:\s*\[.*?\]\s*\n.*?(?=\n\s*\n|\n\s*#|\Z)'
        
        for match in re.finditer(pattern, content, re.DOTALL | re.MULTILINE):
            table_text = match.group(0)
            headers, rows = parse_react_table(table_text)
            
            if headers and rows:
                markdown_table = build_markdown_table(headers, rows)
                if markdown_table:
                    replacements.append({
                        'explanation': f'Convert React table with {len(headers)} columns and {len(rows)} rows to Markdown',
                        'filePath': str(file_path),
                        'oldString': table_text,
                        'newString': markdown_table + '\n'
                    })
        
        return replacements
        
    except Exception as e:
        print(f"  ❌ Error reading {file_path}: {e}")
        return []

def main():
    """Process all markdown files"""
    base_path = Path('products')
    
    if not base_path.exists():
        print("❌ Products directory not found")
        return
    
    md_files = list(base_path.rglob('*.md'))
    print(f"Found {len(md_files)} markdown files to process\n")
    
    all_replacements = []
    
    for md_file in md_files:
        print(f"Processing: {md_file}")
        replacements = find_react_tables_in_file(md_file)
        if replacements:
            print(f"  Found {len(replacements)} React tables to convert")
            all_replacements.extend(replacements)
        else:
            print(f"  No React tables found")
    
    if all_replacements:
        print(f"\nTotal tables to convert: {len(all_replacements)}")
        print(f"Applying all conversions...")
        
        # Group replacements by file for more efficient processing
        from collections import defaultdict
        replacements_by_file = defaultdict(list)
        
        for replacement in all_replacements:
            file_path = replacement['filePath']
            replacements_by_file[file_path].append(replacement)
        
        total_files = len(replacements_by_file)
        successful_files = 0
        
        for file_path, file_replacements in replacements_by_file.items():
            try:
                # Apply all replacements for this file
                from multi_replace_string_in_file import multi_replace_string_in_file
                
                # We'll just manually do the replacements since multi_replace_string_in_file isn't available
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for replacement in file_replacements:
                    content = content.replace(replacement['oldString'], replacement['newString'])
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                successful_files += 1
                print(f"✅ Converted {len(file_replacements)} tables in {file_path}")
                
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")
        
        print(f"\nProcessing complete:")
        print(f"  Files with tables: {total_files}")
        print(f"  Files successfully processed: {successful_files}")
        print(f"  Total tables converted: {len(all_replacements)}")
    
    else:
        print("\nNo React tables found to convert.")

if __name__ == "__main__":
    main()