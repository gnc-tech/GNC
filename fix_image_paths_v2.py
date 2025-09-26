#!/usr/bin/env python3
"""
Enhanced fix for product image paths - better model matching logic
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

def find_matching_product_by_model(products, model_code):
    """Find matching product in JSON by model code with better logic"""
    print(f"    Looking for model: {model_code}")
    
    # Direct model matches
    for product in products:
        json_model = product.get('model', '')
        
        # Try exact match first
        if json_model == model_code:
            print(f"    ✓ Exact match found: {json_model}")
            return product
        
        # Handle thermal battery naming differences
        if model_code.startswith('K-CDR-'):
            md_suffix = model_code.replace('K-CDR-', '')  # e.g., "28FLX" from "K-CDR-28FLX"
            
            # For K-CDR-28FLX -> CDR028FLX pattern
            if json_model.startswith('CDR') and json_model.endswith('FLX'):
                # Extract number from MD: "28FLX" -> "28"
                md_number = ''.join(filter(str.isdigit, md_suffix))
                # Extract number from JSON: "CDR028FLX" -> "028"
                json_number = ''.join(filter(str.isdigit, json_model))
                if md_number and json_number and int(md_number) == int(json_number):
                    print(f"    ✓ Thermal battery match found: {json_model} matches {model_code}")
                    return product
        
        # Handle K-RFX- patterns
        elif model_code.startswith('K-RFX-'):
            md_suffix = model_code.replace('K-RFX-', '')  # e.g., "JK100MH" from "K-RFX-JK100MH"
            if json_model.startswith('FX') and md_suffix in json_model:
                print(f"    ✓ RFX battery match found: {json_model} matches {model_code}")
                return product
        
        # Handle other product patterns
        elif model_code.startswith('Z-') or model_code.startswith('D-Q-'):
            # For products like Z-HY-GJKSSJQ or D-Q-JDW-CGM300S10
            if json_model in model_code or model_code.endswith(json_model):
                print(f"    ✓ Partial match found: {json_model} matches {model_code}")
                return product
            
            # Try to match the last part of the model code
            model_parts = model_code.split('-')
            if len(model_parts) >= 2:
                last_part = model_parts[-1]
                if json_model.endswith(last_part) or last_part in json_model:
                    print(f"    ✓ Last part match found: {json_model} matches {model_code}")
                    return product
        
        # Generic partial matches
        elif json_model in model_code or model_code in json_model:
            print(f"    ✓ Generic partial match found: {json_model} matches {model_code}")
            return product
    
    print(f"    ✗ No match found for {model_code}")
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

def fix_product_images_in_content(content, image_base_path, model_code):
    """Fix product image paths and section titles"""
    
    # Always fix the section titles
    content = fix_slider_section_title(content)
    
    if not image_base_path:
        return content
    
    # Extract the product code from the model for filename pattern
    if model_code.startswith('K-CDR-'):
        filename_pattern = model_code  # Use full model code
    elif model_code.startswith('Z-') or model_code.startswith('D-'):
        filename_pattern = model_code  # Use full model code
    else:
        filename_pattern = model_code
    
    print(f"    Using filename pattern: {filename_pattern}")
    
    # Fix slider section and replace image URLs
    def replace_slider_section(match):
        slider_content = match.group(1)
        
        # Remove any existing #### Product Images line
        slider_content = re.sub(r'^\s*####\s*Product Images\s*\n?', '', slider_content, flags=re.MULTILINE)
        
        # Replace image URLs with correct base path
        image_counter = 1
        def replace_image_url(img_match):
            nonlocal image_counter
            new_url = f"{image_base_path}/{filename_pattern}-Slide-{image_counter:02d}.webp"
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
        
        # Extract model code
        model_code = extract_model_from_file(content)
        if not model_code:
            print(f"  Warning: Could not extract model code")
            return False
        
        print(f"  Model: {model_code}")
        
        # Find matching product in JSON
        matching_product = find_matching_product_by_model(products, model_code)
        
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
        content = fix_product_images_in_content(content, image_base_path, model_code)
        
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