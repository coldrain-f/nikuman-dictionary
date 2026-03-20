import zipfile
import json
import re
import os

zip_path = r'resources\yomitan\Ja-Ko_DIC_2018.zip'
extract_dir = r'resources\yomitan\extracted'

os.makedirs(extract_dir, exist_ok=True)
print("Extracting ZIP...")
with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_dir)

patterns = {
    'v5': re.compile(r'\[.*?5단.*?\]'),
    'v1': re.compile(r'\[.*?[상하]1단.*?\]'),
    'vs': re.compile(r'\[.*?サ(?:변격| 행| 行).*?\]'),
    'vk': re.compile(r'\[.*?カ(?:변격| 행| 行).*?\]'),
    'adj-i': re.compile(r'\[형용사\]|\[형용사ク활용\]')
}

print("Injecting tags...")
modified = False
match_count = 0
for filename in os.listdir(extract_dir):
    if filename.startswith('term_bank_') and filename.endswith('.json'):
        filepath = os.path.join(extract_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for term in data:
            rules = []
            # existing rules if any
            if term[3]:
                rules.extend(term[3].split(' '))
            
            # search within definitions
            definitions = term[5]
            for defi in definitions:
                for rule_tag, pat in patterns.items():
                    if pat.search(defi):
                        if rule_tag not in rules:
                            rules.append(rule_tag)
            
            if rules:
                old_rule = term[3]
                term[3] = " ".join(rules)
                if old_rule != term[3]:
                    modified = True
                    match_count += 1
                
        with open(filepath, 'w', encoding='utf-8') as f:
            # Yomichan specifies writing without excessive whitespace
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

if modified:
    print(f"Tags injected into {match_count} terms! Re-zipping...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for filename in os.listdir(extract_dir):
            filepath = os.path.join(extract_dir, filename)
            z.write(filepath, arcname=filename)
    print("Done.")
else:
    print("No changes were needed.")

# Clean up
import shutil
shutil.rmtree(extract_dir)
