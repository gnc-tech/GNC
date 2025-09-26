#!/usr/bin/env python3
"""
Fix product markdown files by:
1. Converting MD source code display to proper markdown formatting
2. Replacing image paths with correct URLs from gnc-tech.json
3. Removing auto-generated document line
"""

import os
import re
import json
from pathlib import Path

def load_product_data():
    """Load product data from gnc-tech.json to get image path patterns"""
    json_file = Path(__file__).parent / "gnc-tech.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['products']

def extract_model_from_file(content):
    """Extract product model from markdown content"""
    # Look for Product Model in the Basic Information table
    match = re.search(r'\*\*Product Model\*\*\s*\|\s*`([^`]+)`', content)
    if match:
        return match.group(1)
    return None

def get_image_base_url(products, model_code):
    """Get the base URL for product images from gnc-tech.json"""
    for product in products:
        if product['model'] in model_code or model_code in product.get('model', ''):
            image_url = product.get('image', '')
            if image_url:
                # Extract base path (remove -Slide-01.webp part)
                base_url = re.sub(r'-Slide-\d+\.webp$', '', image_url)
                return base_url
    return None

def fix_markdown_sections(content):
    """Fix markdown sections that are displayed as code blocks"""
    
    # Fix overview section
    content = re.sub(
        r'### overview\s*```\s*# Overview\s*---\s*(.*?)```',
        lambda m: f"### Overview\n\n{m.group(1).strip()}",
        content,
        flags=re.DOTALL
    )
    
    # Another pattern for overview
    content = re.sub(
        r'### overview\s*# Overview\s*---\s*(.*?)(?=\s*###|\s*$)',
        lambda m: f"### Overview\n\n{m.group(1).strip()}",
        content,
        flags=re.DOTALL
    )
    
    # Fix features section - convert from indented text to bullet points
    def fix_features(match):
        features_text = match.group(1).strip()
        # Split by lines and clean up
        lines = [line.strip() for line in features_text.split('\n') if line.strip()]
        formatted_features = []
        for line in lines:
            if line.startswith('- '):
                formatted_features.append(line)
            elif line and not line.startswith('#'):
                formatted_features.append(f"- {line}")
        return f"### Features\n\n" + "\n".join(formatted_features)
    
    content = re.sub(
        r'### features\s*(.*?)(?=\s*###|\s*$)',
        fix_features,
        content,
        flags=re.DOTALL
    )
    
    # Fix applications section
    def fix_applications(match):
        apps_text = match.group(1).strip()
        lines = [line.strip() for line in apps_text.split('\n') if line.strip()]
        formatted_apps = []
        for line in lines:
            if line.startswith('- '):
                formatted_apps.append(line)
            elif line and not line.startswith('#'):
                formatted_apps.append(f"- {line}")
        return f"### Applications\n\n" + "\n".join(formatted_apps)
    
    content = re.sub(
        r'### applications\s*(.*?)(?=\s*###|\s*$)',
        fix_applications,
        content,
        flags=re.DOTALL
    )
    
    # Fix specifications section - convert JSON tables to markdown tables
    def fix_specifications(match):
        spec_content = match.group(1)
        
        # Extract JSON table data
        json_pattern = r'```json\s*\{\s*headers:\s*(\[.*?\]),\s*rows:\s*(\[.*?\])\s*\}\s*```'
        
        def convert_json_table(json_match):
            try:
                headers_str = json_match.group(1)
                rows_str = json_match.group(2)
                
                # Parse headers and rows (simplified parsing)
                headers = eval(headers_str)
                rows = eval(rows_str)
                
                # Create markdown table
                table_lines = []
                table_lines.append('| ' + ' | '.join(headers) + ' |')
                table_lines.append('|' + '|'.join(['---'] * len(headers)) + '|')
                
                for row in rows:
                    table_lines.append('| ' + ' | '.join(str(cell) for cell in row) + ' |')
                
                return '\n'.join(table_lines) + '\n'
            except:
                # If parsing fails, return original
                return json_match.group(0)
        
        spec_content = re.sub(json_pattern, convert_json_table, spec_content, flags=re.DOTALL)
        
        return f"### Specifications\n\n{spec_content}"
    
    content = re.sub(
        r'### specifications\s*(.*?)(?=\s*---|\s*\*This document|\s*$)',
        fix_specifications,
        content,
        flags=re.DOTALL
    )
    
    # Fix notes section
    def fix_notes(match):
        notes_text = match.group(1).strip()
        lines = [line.strip() for line in notes_text.split('\n') if line.strip()]
        formatted_notes = []
        for i, line in enumerate(lines, 1):
            if re.match(r'^\d+\.', line):
                formatted_notes.append(line)
            elif line and not line.startswith('#'):
                formatted_notes.append(f"{i}. {line}")
        return f"### Notes\n\n" + "\n".join(formatted_notes)
    
    content = re.sub(
        r'### notes\s*(.*?)(?=\s*###|\s*---|\s*\*This document|\s*$)',
        fix_notes,
        content,
        flags=re.DOTALL
    )
    
    return content

def fix_image_paths(content, image_base_url):
    """Fix image paths in the markdown content"""
    if not image_base_url:
        return content
    
    # Fix slider section images
    def replace_slider_images(match):
        slider_content = match.group(1)
        
        # Replace generic image paths with specific ones
        image_counter = 1
        def replace_image(img_match):
            nonlocal image_counter
            new_url = f"{image_base_url}-Slide-{image_counter:02d}.webp"
            image_counter += 1
            return f"![Product Image]({new_url})"
        
        slider_content = re.sub(
            r'!\[Product Image\]\(https://www\.gnc-tech\.com/images/products/[^)]+\)',
            replace_image,
            slider_content
        )
        
        return f"### Product Images\n\n{slider_content}"
    
    content = re.sub(
        r'### slider\s*#### Product Images\s*(.*?)(?=\s*###|\s*$)',
        replace_slider_images,
        content,
        flags=re.DOTALL
    )
    
    # Fix main product image
    if image_base_url:
        main_image_url = f"{image_base_url}.webp"
        content = re.sub(
            r'!\[[^\]]*\]\(https://www\.gnc-tech\.com/images/products/[^)]+\)',
            lambda m: m.group(0).replace(re.search(r'https://www\.gnc-tech\.com/images/products/[^)]+', m.group(0)).group(0), main_image_url),
            content,
            count=1  # Only replace the first one (main image)
        )
    
    return content

def remove_auto_generated_line(content):
    """Remove the auto-generated document line"""
    content = re.sub(
        r'\*This document is automatically generated from source file [^*]+\*\s*\n?',
        '',
        content
    )
    return content

def clean_markdown_formatting(content):
    """Clean up markdown formatting issues"""
    
    # Remove excessive indentation in sections
    content = re.sub(r'\n    ([^\n])', r'\n\1', content)
    
    # Fix multiple empty lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Clean up section formatting
    content = re.sub(r'\n\s*\n\s*###', '\n\n###', content)
    
    return content

def process_markdown_file(file_path, products):
    """Process a single markdown file"""
    print(f"Processing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract model code
        model_code = extract_model_from_file(content)
        if not model_code:
            print(f"  Warning: Could not extract model code from {file_path}")
            return False
        
        print(f"  Model: {model_code}")
        
        # Get image base URL
        image_base_url = get_image_base_url(products, model_code)
        if image_base_url:
            print(f"  Image base URL: {image_base_url}")
        else:
            print(f"  Warning: Could not find image URL for model {model_code}")
        
        # Apply fixes
        original_content = content
        content = fix_markdown_sections(content)
        content = fix_image_paths(content, image_base_url)
        content = remove_auto_generated_line(content)
        content = clean_markdown_formatting(content)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Fixed")
            return True
        else:
            print(f"  - No changes needed")
            return False
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Main function to process all markdown files"""
    script_dir = Path(__file__).parent
    products_dir = script_dir / "products"
    
    if not products_dir.exists():
        print(f"Error: Products directory not found at {products_dir}")
        return
    
    # Load product data
    try:
        products = load_product_data()
        print(f"Loaded {len(products)} products from gnc-tech.json")
    except Exception as e:
        print(f"Error loading product data: {e}")
        return
    
    # Find all markdown files
    md_files = list(products_dir.rglob("*.md"))
    md_files = [f for f in md_files if f.name != "README.md"]  # Exclude README files
    
    print(f"Found {len(md_files)} markdown files to process")
    
    # Process each file
    processed = 0
    fixed = 0
    
    for md_file in md_files:
        processed += 1
        if process_markdown_file(md_file, products):
            fixed += 1
    
    print(f"\nProcessing complete:")
    print(f"  Files processed: {processed}")
    print(f"  Files fixed: {fixed}")

if __name__ == "__main__":
    main()