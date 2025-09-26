#!/usr/bin/env python3
"""
Fix product image paths by matching image filenames directly
"""

import os
import re
import json
from pathlib import Path
from urllib.parse import urlparse

def load_product_data():
    """Load product data from gnc-tech.json"""
    json_file = Path(__file__).parent / "gnc-tech.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['products']

def extract_model_from_file(content):
    """Extract product model from markdown content"""
    match = re.search(r'\*\*Product Model\*\*\s*\|\s*`([^`]+)`', content)
    if match:
        return match.group(1)
    return None

def extract_image_filename_from_md(content):
    """Extract image filename pattern from markdown content"""
    # Find any product image reference
    image_pattern = r'!\[Product Image\]\(([^)]+)\)'
    matches = re.findall(image_pattern, content)
    
    if matches:
        # Get the first image URL
        first_image = matches[0]
        # Extract the filename part (e.g., K-CDR-28FLX-Slide-01.webp)
        filename = first_image.split('/')[-1]
        # Extract the base part without -Slide-XX.webp (e.g., K-CDR-28FLX)
        base_filename = re.sub(r'-Slide-\d+\.webp$', '', filename)
        return base_filename
    
    return None

def find_matching_product_by_image_filename(products, image_filename):
    """Find matching product in JSON by image filename"""
    print(f"    Looking for image filename: {image_filename}")
    
    for product in products:
        image_url = product.get('image', '')
        if image_url:
            # Extract filename from JSON image URL
            json_filename = image_url.split('/')[-1]
            # Extract base part without -Slide-XX.webp
            json_base_filename = re.sub(r'-Slide-\d+\.webp$', '', json_filename)
            
            if json_base_filename == image_filename:
                print(f"    ✓ Found matching image: {json_base_filename}")
                return product
    
    print(f"    ✗ No matching image found for {image_filename}")
    return None

def get_image_base_path_from_product(product):
    """Extract base path from product image URL"""
    if not product:
        return None
    
    image_url = product.get('image', '')
    if not image_url:
        return None
    
    # Remove the filename part (everything after the last /)
    base_path = '/'.join(image_url.split('/')[:-1])
    return base_path

def fix_product_images_in_content(content, image_base_path, image_filename):
    """Fix product image paths and section titles"""
    
    # Always fix the section titles
    content = fix_slider_section_title(content)
    
    if not image_base_path or not image_filename:
        return content
    
    print(f"    Using image filename: {image_filename}")
    
    # Fix slider section and replace image URLs
    def replace_slider_section(match):
        slider_content = match.group(1)
        
        # Remove any existing #### Product Images line
        slider_content = re.sub(r'^\s*####\s*Product Images\s*\n?', '', slider_content, flags=re.MULTILINE)
        
        # Replace image URLs with correct base path
        image_counter = 1
        def replace_image_url(img_match):
            nonlocal image_counter
            new_url = f"{image_base_path}/{image_filename}-Slide-{image_counter:02d}.webp"
            image_counter += 1
            return f"![Product Image]({new_url})"
        
        # Replace all product image URLs
        slider_content = re.sub(
            r'!\[Product Image\]\([^)]+\)',
            replace_image_url,
            slider_content
        )
        
        return f"### Product Images\n\n{slider_content.strip()}"
    
    # Replace ### slider section or ### Product Images section
    content = re.sub(
        r'### (?:slider|Product Images)\s*(.*?)(?=\s*###|\s*$)',
        replace_slider_section,
        content,
        flags=re.DOTALL
    )
    
    return content

def fix_slider_section_title(content):
    """Fix slider section title without changing image paths"""
    def replace_slider_section(match):
        slider_content = match.group(1)
        
        # Remove any existing #### Product Images line
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
        
        # Extract model code for reference
        model_code = extract_model_from_file(content)
        if model_code:
            print(f"  Model: {model_code}")
        
        # Extract image filename from markdown content
        image_filename = extract_image_filename_from_md(content)
        if not image_filename:
            print(f"  Warning: Could not extract image filename")
            return False
        
        print(f"  Image filename: {image_filename}")
        
        # Find matching product in JSON by image filename
        matching_product = find_matching_product_by_image_filename(products, image_filename)
        
        if matching_product:
            image_base_path = get_image_base_path_from_product(matching_product)
            if image_base_path:
                print(f"  ✓ Found image base path: {image_base_path}")
            else:
                print(f"  Warning: Product found but no image URL")
                image_base_path = None
        else:
            print(f"  Warning: No matching product found in JSON")
            image_base_path = None
        
        # Apply fixes
        original_content = content
        content = fix_product_images_in_content(content, image_base_path, image_filename)
        
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
    """Main function"""
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
    print()
    
    # Process each file
    processed = 0
    fixed = 0
    
    for md_file in md_files:
        processed += 1
        if process_markdown_file(md_file, products):
            fixed += 1
        print()  # Add blank line for readability
    
    print(f"Processing complete:")
    print(f"  Files processed: {processed}")
    print(f"  Files fixed: {fixed}")

if __name__ == "__main__":
    main()