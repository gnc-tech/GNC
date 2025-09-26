#!/usr/bin/env python3
"""
Fix product image paths in markdown files by:
1. Finding matching image filenames between MD and JSON files
2. Using JSON file's path prefix for all product images
3. Replacing ### slider with ### Product Images
4. Removing the #### Product Images subtitle
"""

import os
import re
import json
from pathlib import Path
from urllib.parse import urlparse

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

def get_image_base_path_from_json(products, model_code):
    """Get the base path for product images from gnc-tech.json"""
    for product in products:
        if product['model'] in model_code or model_code in product.get('model', ''):
            image_url = product.get('image', '')
            if image_url:
                # Extract base path (remove filename)
                parsed_url = urlparse(image_url)
                path_parts = parsed_url.path.split('/')
                # Remove the filename (last part)
                base_path = '/'.join(path_parts[:-1])
                return f"{parsed_url.scheme}://{parsed_url.netloc}{base_path}"
    return None

def extract_image_filename_from_md(content):
    """Extract image filenames from markdown content to match with JSON"""
    # Find all product image references
    image_pattern = r'!\[Product Image\]\(([^)]+)\)'
    matches = re.findall(image_pattern, content)
    
    if matches:
        # Get the first image to extract the pattern
        first_image = matches[0]
        parsed_url = urlparse(first_image)
        path_parts = parsed_url.path.split('/')
        
        # Look for the product code pattern (e.g., K-CDR-28FLX)
        for part in path_parts:
            if re.match(r'^[A-Z]-[A-Z0-9]+-[A-Z0-9]+', part):
                return part
    
    return None

def fix_product_images_in_content(content, image_base_path):
    """Fix product image paths and section titles"""
    
    if not image_base_path:
        # Still fix the section titles even if we don't have image paths
        content = fix_slider_section_title(content)
        return content
    
    # Fix slider section and remove #### Product Images subtitle
    def replace_slider_section(match):
        slider_content = match.group(1)
        
        # Remove the #### Product Images line if present
        slider_content = re.sub(r'^\s*####\s*Product Images\s*\n?', '', slider_content, flags=re.MULTILINE)
        
        # Replace image URLs with correct base path
        image_counter = 1
        def replace_image_url(img_match):
            nonlocal image_counter
            new_url = f"{image_base_path}-Slide-{image_counter:02d}.webp"
            image_counter += 1
            return f"![Product Image]({new_url})"
        
        # Replace all product image URLs
        slider_content = re.sub(
            r'!\[Product Image\]\([^)]+\)',
            replace_image_url,
            slider_content
        )
        
        return f"### Product Images\n\n{slider_content.strip()}"
    
    # Replace ### slider section
    content = re.sub(
        r'### slider\s*(.*?)(?=\s*###|\s*$)',
        replace_slider_section,
        content,
        flags=re.DOTALL
    )
    
    return content

def fix_slider_section_title(content):
    """Fix slider section title even without image path info"""
    def replace_slider_section(match):
        slider_content = match.group(1)
        
        # Remove the #### Product Images line if present
        slider_content = re.sub(r'^\s*####\s*Product Images\s*\n?', '', slider_content, flags=re.MULTILINE)
        
        return f"### Product Images\n\n{slider_content.strip()}"
    
    # Replace ### slider section
    content = re.sub(
        r'### slider\s*(.*?)(?=\s*###|\s*$)',
        replace_slider_section,
        content,
        flags=re.DOTALL
    )
    
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
            # Still try to fix slider section title
            original_content = content
            content = fix_slider_section_title(content)
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✓ Fixed slider section title only")
                return True
            return False
        
        print(f"  Model: {model_code}")
        
        # Get image base path from JSON
        image_base_path = get_image_base_path_from_json(products, model_code)
        
        if image_base_path:
            # Extract the filename pattern from existing images to build complete path
            md_image_pattern = extract_image_filename_from_md(content)
            if md_image_pattern:
                # Build complete base path
                complete_base_path = f"{image_base_path}/{md_image_pattern}/{md_image_pattern}"
                print(f"  Image base path: {complete_base_path}")
            else:
                complete_base_path = image_base_path
                print(f"  Image base path: {complete_base_path}")
        else:
            complete_base_path = None
            print(f"  Warning: Could not find image path for model {model_code}")
        
        # Apply fixes
        original_content = content
        content = fix_product_images_in_content(content, complete_base_path)
        
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
    md_files = [f for f in md_files if f.name != "README.md"]
    
    print(f"Found {len(md_files)} markdown files to process")
    
    # Process each file
    processed = 0
    fixed = 0
    
    for md_file in md_files:
        processed += 1
        if process_markdown_file(md_file, products):
            fixed += 1
    
    print(f"\nImage path processing complete:")
    print(f"  Files processed: {processed}")
    print(f"  Files fixed: {fixed}")

if __name__ == "__main__":
    main()