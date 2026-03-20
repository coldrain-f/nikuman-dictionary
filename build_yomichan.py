import os
import json
import zipfile
import re
import shutil

txt_path = r"resources\yomitan\raw_dump.txt"
extract_dir = r"resources\yomitan\custom_export"
os.makedirs(extract_dir, exist_ok=True)

patterns = {
    'v5': re.compile(r'\[.*?5단.*?\]'),
    'v1': re.compile(r'\[.*?[상하]1단.*?\]'),
    'vs': re.compile(r'\[.*?サ(?:변격| 행| 行).*?\]'),
    'vk': re.compile(r'\[.*?カ(?:변격| 행| 行).*?\]'),
    'adj-i': re.compile(r'\[형용사\]|\[형용사ク활용\]')
}

term_bank = []
term_count = 0
bank_index = 1
seen_entries = set()

def flush_bank():
    global term_bank, bank_index, extract_dir
    if not term_bank: return
    filepath = os.path.join(extract_dir, f"term_bank_{bank_index}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(term_bank, f, ensure_ascii=False, separators=(',', ':'))
    term_bank.clear()
    bank_index += 1

with open(txt_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('##'): continue
        
        parts = line.split('\t')
        if len(parts) < 2: continue
        
        word = parts[0]
        # sometimes definitions have literal \n or <br>
        defi_str = parts[1].replace('<br>', '\n')
        lines = defi_str.split('\n')
        
        reading = ""
        cand = ""
        first_line = lines[0].strip() if lines else ""
        
        # Match headword and reading bracket: e.g. "逆[ぎゃく]"
        reading_match = re.search(r'^(.+?)\s*\[([^\]]+)\]', first_line)
        
        if reading_match:
            cand = reading_match.group(2).split('|')[0]
            head_part = reading_match.group(1)
            
            # Check for Kanji to swap logic
            has_kanji_word = any('\u4e00' <= c <= '\u9fff' for c in word)
            cand_has_kanji = any('\u4e00' <= c <= '\u9fff' for c in cand)
            
            if cand_has_kanji and not has_kanji_word:
                reading = word
                word = cand
            elif not cand_has_kanji:
                reading = cand
                
            # If the first line is literally the header, strip it
            if head_part == parts[0]:
                lines = lines[1:]
        else:
            if first_line == word:
                lines = lines[1:]

        # Create the final, cleaned definition string
        clean_defi = '\n'.join(lines).strip()
        if not clean_defi:
            clean_defi = defi_str # fallback if we stripped everything

        rules = set()
        for tag, pat in patterns.items():
            if pat.search(defi_str):
                rules.add(tag)

        # Deduplication check
        signature = (word, reading, clean_defi)
        if signature in seen_entries:
            continue
        seen_entries.add(signature)
                
        term_entry = [
            word,
            reading,
            "",
            " ".join(sorted(rules)),
            0,
            [clean_defi],
            term_count,
            ""
        ]
        term_bank.append(term_entry)
        term_count += 1
        
        if len(term_bank) >= 10000:
            flush_bank()

flush_bank()

print("Writing index.json...")
index_data = {
    "title": "Ja-Ko_DIC_2018",
    "revision": "Custom No-Merge",
    "sequenced": True,
    "format": 3,
    "author": "Antigravity",
    "url": "",
    "description": "StarDict to Yomichan. Kana/Kanji swapped, tags injected, duplicates removed."
}
with open(os.path.join(extract_dir, "index.json"), "w", encoding="utf-8") as f:
    json.dump(index_data, f, ensure_ascii=False)

zip_path = r"resources\yomitan\Ja-Ko_DIC_2018.zip"
print(f"Creating {zip_path}...")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for filename in os.listdir(extract_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(extract_dir, filename)
            z.write(filepath, arcname=filename)

shutil.rmtree(extract_dir)
print(f"Exported {term_count} terms successfully!")
