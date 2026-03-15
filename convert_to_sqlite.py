import struct
import sqlite3
import os

def parse_ifo(ifo_path):
    info = {}
    with open(ifo_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line:
                k, v = line.strip().split('=', 1)
                info[k] = v
    return info

def convert(base_name, output_db):
    ifo_path = base_name + '.ifo'
    idx_path = base_name + '.idx'
    dict_path = base_name + '.dict'
    
    info = parse_ifo(ifo_path)
    wordcount = int(info.get('wordcount', 0))
    idxoffsetbits = int(info.get('idxoffsetbits', 32))
    sametypesequence = info.get('sametypesequence', 'm')
    
    if idxoffsetbits == 64:
        offset_format = '>Q'
        offset_size = 8
    else:
        offset_format = '>I'
        offset_size = 4
        
    conn = sqlite3.connect(output_db)
    cur = conn.cursor()
    
    table_name = os.path.basename(base_name).replace('-', '_')
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT, definition TEXT)")
    
    with open(idx_path, 'rb') as f_idx:
        idx_data = f_idx.read()
        
    entries = []
    idx_pos = 0
    idx_len = len(idx_data)
    
    # parse idx
    while idx_pos < idx_len:
        end_pos = idx_data.find(b'\0', idx_pos)
        if end_pos == -1:
            break
        word = idx_data[idx_pos:end_pos].decode('utf-8')
        idx_pos = end_pos + 1
        
        offset = struct.unpack(offset_format, idx_data[idx_pos:idx_pos+offset_size])[0]
        idx_pos += offset_size
        
        size = struct.unpack('>I', idx_data[idx_pos:idx_pos+4])[0]
        idx_pos += 4
        
        entries.append((word, offset, size))
        
    with open(dict_path, 'rb') as f_dict:
        batch = []
        for word, offset, size in entries:
            f_dict.seek(offset)
            definition_bytes = f_dict.read(size)
            definition = definition_bytes.decode('utf-8', errors='replace')
            batch.append((word, definition))
            
            if len(batch) >= 10000:
                cur.executemany(f"INSERT INTO {table_name} (word, definition) VALUES (?, ?)", batch)
                batch = []
        
        if batch:
            cur.executemany(f"INSERT INTO {table_name} (word, definition) VALUES (?, ?)", batch)
            
    cur.execute(f"CREATE INDEX idx_{table_name}_word ON {table_name}(word)")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    base_dir = r"c:\dev\JAKO_Dict\resources"
    
    print("Converting Hanja-Ko_DIC_2018...")
    convert(os.path.join(base_dir, "Hanja-Ko_DIC_2018"), os.path.join(base_dir, "Hanja-Ko_DIC_2018.sqlite"))
    
    print("Converting Ja-Ko_DIC_2018...")
    convert(os.path.join(base_dir, "Ja-Ko_DIC_2018"), os.path.join(base_dir, "Ja-Ko_DIC_2018.sqlite"))
    
    print("Done!")
