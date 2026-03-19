import re

import sys

with open('templates/テスト観点カタログ/テスト観点カタログ__04_機能テスト_共通.md', 'r') as f:
    lines = f.read().splitlines()

output = []
current_table_lines = []
in_table = False
section_title = None

def process_table(lines, section_title=None):
    if not lines:
        return []

    # Find where the data starts
    header_idx = -1
    for i, line in enumerate(lines):
        if re.match(r'^\|[\s\-]+\|', line):
            header_idx = i - 1
            break
    
    if header_idx < 0:
        return lines

    headers = [col.strip() for col in lines[header_idx].strip('|').split('|')]
    
    data_lines = lines[header_idx + 2:]
    
    out = []
    if section_title:
        out.append(f"## {section_title}")
    else:
        # Check if first row is generic like Col1 ...
        if headers[0] == "Col1":
            return lines # Something wrong
            
    # Indices for columns
    def get_col_idx(name):
        for i, h in enumerate(headers):
            if name in h:
                return i
        return -1
    
    idx_no = get_col_idx('No')
    idx_dai = get_col_idx('大項目')
    idx_chu = get_col_idx('中項目')
    idx_sho = get_col_idx('小項目')
    idx_shosai = get_col_idx('詳細')
    idx_kanten = get_col_idx('観点')
    idx_count = get_col_idx('カウント対象')
    idx_hosoku = get_col_idx('補足')

    last_dai = ""
    last_chu = ""
    last_sho = ""
    last_shosai = ""
    
    for line in data_lines:
        cols = [col.strip() for col in line.strip('|').split('|')]
        if not any(cols):
            continue
            
        # check if this is the generic comment line or something
        if len(cols) > 0 and '■' in cols[0]:
            continue
            
        # skip row if not enough columns
        if len(cols) <= max(idx_dai, idx_kanten):
            continue

        no = cols[idx_no] if idx_no >= 0 and idx_no < len(cols) else ""
        dai = cols[idx_dai] if idx_dai >= 0 and idx_dai < len(cols) else ""
        chu = cols[idx_chu] if idx_chu >= 0 and idx_chu < len(cols) else ""
        sho = cols[idx_sho] if idx_sho >= 0 and idx_sho < len(cols) else ""
        shosai = cols[idx_shosai] if idx_shosai >= 0 and idx_shosai < len(cols) else ""
        kanten = cols[idx_kanten] if idx_kanten >= 0 and idx_kanten < len(cols) else ""
        count = cols[idx_count] if idx_count >= 0 and idx_count < len(cols) else ""
        hosoku = cols[idx_hosoku] if idx_hosoku >= 0 and idx_hosoku < len(cols) else ""
        
        # When cells are empty, inherit from previous row (only for grouping columns)
        if dai and dai != "-":
            last_dai = dai
            last_chu = ""
            last_sho = ""
            last_shosai = ""
        if chu and chu != "-":
            last_chu = chu
            last_sho = ""
            last_shosai = ""
        if sho and sho != "-":
            last_sho = sho
            last_shosai = ""
        if shosai and shosai != "-":
            last_shosai = shosai
            
        # Special case: headers with ★ or similar
        if "★" in "".join(cols):
            continue
            
        # Handle cases where "観点" is empty but there's a supplement
        if not kanten and not kanten.strip():
            # might be continuation of 補足
            if not any([no, dai, chu, sho, shosai, count]) and hosoku:
                out.append(f"    - {hosoku}")
            continue

        res_dai = dai if dai and dai != "-" else last_dai
        res_chu = chu if chu and chu != "-" else last_chu
        res_sho = sho if sho and sho != "-" else last_sho
        res_shosai = shosai if shosai and shosai != "-" else last_shosai

        # Add headers if changed
        # We need to print headers if they are explicitly present on the row
        base_level = 2 if not section_title else 3

        if dai and dai != "-":
            out.append(f"\n{'#' * base_level} {res_dai}")
        if chu and chu != "-":
            out.append(f"\n{'#' * (base_level + 1)} {res_chu}")
        if sho and sho != "-":
            out.append(f"\n{'#' * (base_level + 2)} {res_sho}")
        if shosai and shosai != "-":
            out.append(f"\n{'#' * (base_level + 3)} {res_shosai}")
            
        # Write the data point
        out.append(f"- **観点**: {kanten}")
        if count and count != "-":
            out.append(f"  - **カウント対象**: {count}")
        if hosoku and hosoku != "-":
            out.append(f"  - **補足**: {hosoku}")
            
    return out

for i, line in enumerate(lines):
    if line.startswith('|'):
        if not in_table:
            # check if it's a section title row
            cols = [c.strip() for c in line.strip('|').split('|')]
            # if the table starts with Col1 Col2, skip to the actual headers row
            if cols and cols[0] == 'Col1':
                # The section title might be in row i+2 if it's Col1 format
                # But sometimes it's like | ■データベースアクセス | ... |
                pass
            elif cols and cols[0].startswith('■'):
                section_title = cols[0].replace('■', '')
            in_table = True
        current_table_lines.append(line)
    else:
        if in_table:
            output.extend(process_table(current_table_lines))
            current_table_lines = []
            in_table = False
            section_title = None
        output.append(line)

if in_table:
    output.extend(process_table(current_table_lines))

with open('templates/テスト観点カタログ/テスト観点カタログ__04_機能テスト_共通.md.converted', 'w') as f:
    f.write('\n'.join(output))

