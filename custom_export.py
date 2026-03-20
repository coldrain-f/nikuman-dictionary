import pyglossary
import os
import json
import zipfile
import re
import shutil

pyglossary.Glossary.init()
glos = pyglossary.Glossary()

print("Reading StarDict file...")
glos.read(r"resources\stardict\Ja-Ko_DIC_2018.ifo", format="StarDict")
print(f"Loaded {len(glos)} entries.")
glos.removeHtmlTagsAll()

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

def flush_bank():
    global term_bank, bank_index, extract_dir
    if not term_bank: return
    filepath = os.path.join(extract_dir, f"term_bank_{bank_index}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(term_bank, f, ensure_ascii=False, separators=(',', ':'))
    term_bank.clear()
    bank_index += 1

print("Converting entries...")
for entry in glos:
    if entry.isData(): continue
    word = entry.l_term[0]
    defi_str = entry.defi.strip()
    
    reading = ""
    # Avoid errors if defi is empty
    if defi_str:
        first_line = defi_str.split('\n')[0]
        # Look for brackets representing the reading: word[reading] or just [reading]
        reading_match = re.search(r'\[([^\]]+)\]', first_line)
        if reading_match:
            cand = reading_match.group(1)
            # Make sure it's not a POS tag like [명사], [5단...]
            if "사" not in cand and "단" not in cand and "형용" not in cand:
                reading = cand

    rules = set()
    for tag, pat in patterns.items():
        if pat.search(defi_str):
            rules.add(tag)
            
    term_entry = [
        word,
        reading,
        "",
        " ".join(sorted(rules)),
        0,
        [defi_str],
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
    "description": "StarDict to Yomichan. Unmerged headwords."
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
