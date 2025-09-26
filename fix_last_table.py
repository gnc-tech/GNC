#!/usr/bin/env python3
"""
处理最后一个React表格
"""

import re
import ast
from pathlib import Path

def fix_last_table():
    file_path = Path('products/control-systems/servo-actuators/rotary-actuator-zx10d040.md')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'headers:\s*(\[.*?\]),\s*\n\s*rows:\s*(\[(?:[^\[\]]*|\[[^\]]*\])*\])'
    
    def replace_table(match):
        headers_text = match.group(1)
        rows_text = match.group(2)
        
        try:
            headers_clean = headers_text.replace("'", '"')
            rows_clean = rows_text.replace("'", '"')
            
            headers = ast.literal_eval(headers_clean)
            rows = ast.literal_eval(rows_clean)
            
            lines = []
            header_row = '| ' + ' | '.join(headers) + ' |'
            lines.append(header_row)
            separator = '| ' + ' | '.join(['---'] * len(headers)) + ' |'
            lines.append(separator)
            
            for row in rows:
                while len(row) < len(headers):
                    row.append('')
                if len(row) > len(headers):
                    row = row[:len(headers)]
                row_str = '| ' + ' | '.join(str(cell) for cell in row) + ' |'
                lines.append(row_str)
            
            return '\n'.join(lines)
            
        except Exception as e:
            print(f'Error: {e}')
            return match.group(0)
    
    new_content = re.sub(pattern, replace_table, content, flags=re.MULTILINE | re.DOTALL)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('✅ Successfully converted the remaining React table!')
        return True
    else:
        print('No changes made')
        return False

if __name__ == "__main__":
    fix_last_table()