#!/usr/bin/env python3
"""
Enhanced fix for product markdown files - specifically handles JSON table conversion
"""

import os
import re
import json
import ast
from pathlib import Path

def convert_json_table_to_markdown(json_str):
    """Convert JSON table format to markdown table"""
    try:
        # Try to extract and parse the JSON table
        # Handle different JSON patterns
        patterns = [
            r'\{[\s\S]*?headers:\s*(\[.*?\]),[\s\S]*?rows:\s*(\[[\s\S]*?\])\s*\}',
            r'headers:\s*(\[.*?\]),[\s\S]*?rows:\s*(\[[\s\S]*?\])'
        ]
        
        headers = None
        rows = None
        
        for pattern in patterns:
            json_match = re.search(pattern, json_str)
            if json_match:
                headers_str = json_match.group(1)
                rows_str = json_match.group(2)
                
                # Parse headers and rows using ast.literal_eval for safer evaluation
                headers = ast.literal_eval(headers_str)
                rows = ast.literal_eval(rows_str)
                break
        
        if headers is None or rows is None:
            return json_str
        
        # Create markdown table
        table_lines = []
        table_lines.append('| ' + ' | '.join(headers) + ' |')
        table_lines.append('|' + '|'.join(['---'] * len(headers)) + '|')
        
        for row in rows:
            table_lines.append('| ' + ' | '.join(str(cell) for cell in row) + ' |')
        
        return '\n'.join(table_lines) + '\n'
    except Exception as e:
        print(f"  Warning: Failed to convert JSON table: {e}")
        return json_str

def fix_json_tables_in_content(content):
    """Fix all JSON tables in the content"""
    
    # Pattern to match JSON code blocks containing table data
    json_pattern = r'```json\s*([\s\S]*?headers:[\s\S]*?rows:[\s\S]*?)\s*```'
    
    def replace_json_table(match):
        json_content = match.group(1)
        return convert_json_table_to_markdown(json_content)
    
    content = re.sub(json_pattern, replace_json_table, content)
    
    # Also handle JSON blocks without the ```json wrapper but with curly braces
    json_pattern2 = r'(\{[\s\S]*?headers:\s*\[[\s\S]*?\],[\s\S]*?rows:\s*\[[\s\S]*?\]\s*\})'
    content = re.sub(json_pattern2, convert_json_table_to_markdown, content)
    
    return content

def process_file_for_json_tables(file_path):
    """Process a single file to fix JSON tables"""
    print(f"Processing JSON tables in: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_json_tables_in_content(content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Fixed JSON tables")
            return True
        else:
            print(f"  - No JSON tables to fix")
            return False
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Main function to fix JSON tables in all markdown files"""
    script_dir = Path(__file__).parent
    products_dir = script_dir / "products"
    
    if not products_dir.exists():
        print(f"Error: Products directory not found at {products_dir}")
        return
    
    # Find all markdown files
    md_files = list(products_dir.rglob("*.md"))
    md_files = [f for f in md_files if f.name != "README.md"]
    
    print(f"Found {len(md_files)} markdown files to process for JSON table fixes")
    
    # Process each file
    processed = 0
    fixed = 0
    
    for md_file in md_files:
        processed += 1
        if process_file_for_json_tables(md_file):
            fixed += 1
    
    print(f"\nJSON table processing complete:")
    print(f"  Files processed: {processed}")
    print(f"  Files with JSON tables fixed: {fixed}")

if __name__ == "__main__":
    main()