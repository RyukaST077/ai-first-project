import sys
import re

with open('templates/テスト観点カタログ/テスト観点カタログ__04_機能テスト_共通.md', 'r') as f:
    lines = f.read().splitlines()

def process_table(table_lines):
    # Find the real header row (the one with '大項目' or '観点')
    header_idx = -1
    for i, line in enumerate(table_lines):
        if '大項目' in line and '観点' in line:
            header_idx = i
            break
            
    if header_idx == -1:
        return table_lines
        
    headers = [col.strip() for col in table_lines[header_idx].strip('|').split('|')]
    
    # Try to find section title (like ■データベースアクセス)
    section_title = None
    for i in range(header_idx):
        if '■' in table_lines[i]:
            match = re.search(r'■([^|\s]+)', table_lines[i])
            if match:
                section_title = match.group(1)
                break
                
    data_lines = table_lines[header_idx + 1:]
    
    out = []
    if section_title:
        out.append(f"## {section_title}")
        
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
    if idx_kanten == -1: idx_kanten = get_col_idx('観点（★）')
    idx_count = get_col_idx('カウント対象')
    if idx_count == -1: idx_count = get_col_idx('カウント対象（★）')
    idx_hosoku = get_col_idx('補足')

    last_dai = ""
    last_chu = ""
    last_sho = ""
    last_shosai = ""
    
    for line in data_lines:
        if re.match(r'^\|[\s\-]+\|', line):
            continue
            
        cols = [col.strip() for col in line.strip('|').split('|')]
        if not any(cols):
            continue
            
        # skip row if not enough columns, or if it's just Col1 formatting
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
        
        # When cells are empty, inherit from previous row
        if dai and dai != "-":
            last_dai = dai
            last_chu = ""
            last_sho = ""
            last_shosai = ""
        if chu and chu != "-" and chu != "※ファイルアップロードを含む" and chu != "※ファイルダウンロードを含む": # Exception for specific notes in 中項目 column
            last_chu = chu
            last_sho = ""
            last_shosai = ""
        if '※' in dai: # Sometimes notes are in 大項目
            last_dai = dai
        if '※' in chu:
            pass # Keep previous chu
            
        res_dai = dai if dai and dai != "-" and '※' not in dai else last_dai
        res_chu = chu if chu and chu != "-" and '※' not in chu else last_chu
        
        if sho and sho != "-":
            last_sho = sho
            last_shosai = ""
        if shosai and shosai != "-":
            last_shosai = shosai
            
        res_sho = sho if sho and sho != "-" else last_sho
        res_shosai = shosai if shosai and shosai != "-" else last_shosai

        # Avoid printing "★" or generic lines
        if "★：" in "".join(cols):
            continue
            
        # Handle continuation of 補足
        if not kanten and not kanten.strip():
            if not any([no, dai, chu, sho, shosai, count]) and hosoku:
                out.append(f"    - {hosoku}")
            continue

        base_level = 2 if not section_title else 3

        # Add headers if changed
        if dai and dai != "-" and '※' not in dai:
            out.append(f"\n{'#' * base_level} {res_dai}")
        if chu and chu != "-" and '※' not in chu:
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

output = []
current_table_lines = []
in_table = False

for line in lines:
    if line.startswith('|'):
        in_table = True
        current_table_lines.append(line)
    else:
        if in_table:
            output.extend(process_table(current_table_lines))
            current_table_lines = []
            in_table = False
        output.append(line)

if in_table:
    output.extend(process_table(current_table_lines))

with open('templates/テスト観点カタログ/テスト観点カタログ__04_機能テスト_共通.md.converted2', 'w') as f:
    f.write('\n'.join(output))
