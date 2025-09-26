#!/usr/bin/env python3
"""
Fix duplicate Product Images titles in all markdown files
"""

import os
import re
from pathlib import Path

def fix_duplicate_titles(content):
    """Fix duplicate Product Images titles"""
    
    # Fix the specific pattern: ### Product Images followed by #### Product Images
    content = re.sub(
        r'### Product Images\s*\n\s*#### Product Images\s*\n',
        '### Product Images\n\n',
        content,
        flags=re.MULTILINE
    )
    
    # Also fix any standalone "Product Images" text that appears after ### Product Images
    content = re.sub(
        r'(### Product Images\s*\n)\s*Product Images\s*\n',
        r'\1\n',
        content,
        flags=re.MULTILINE
    )
    
    return content

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_duplicate_titles(content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function"""
    script_dir = Path(__file__).parent
    products_dir = script_dir / "products"
    
    if not products_dir.exists():
        print(f"Error: Products directory not found at {products_dir}")
        return
    
    # Find all markdown files
    md_files = list(products_dir.rglob("*.md"))
    md_files = [f for f in md_files if f.name != "README.md"]
    
    print(f"Processing {len(md_files)} markdown files...")
    
    fixed_count = 0
    for md_file in md_files:
        if process_file(md_file):
            fixed_count += 1
    
    print(f"Fixed {fixed_count} files with duplicate titles")

if __name__ == "__main__":
    main()