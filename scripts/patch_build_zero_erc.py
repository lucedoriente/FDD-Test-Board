import os, sys, re

# Update build_zero_erc_fdd.py to use get_flattened_symbol instead of extract_symbol_exact_with_parent
script_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py"

with open(script_path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect where extract_symbol_exact_with_parent is defined and used
idx1 = text.find("def extract_symbol_exact_with_parent(")
idx2 = text.find("def get_symbol_pins_for_unit(")

flatten_func = '''def get_raw_sym_text(lib_name, sym_name):
    if lib_name == "FDD-Test-Board":
        p = os.path.join(kicad_dir, "FDD-Test-Board.kicad_sym")
    else:
        p = os.path.join(sym_dir, f"{lib_name}.kicad_sym")
    if not os.path.exists(p):
        return ""
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    start_tag = f'(symbol "{sym_name}"'
    idx = content.find(start_tag)
    if idx == -1: return ""
    cnt, end = 0, 0
    for i in range(idx, len(content)):
        if content[i] == '(': cnt += 1
        elif content[i] == ')':
            cnt -= 1
            if cnt == 0:
                end = i + 1; break
    return content[idx:end]

def extract_symbol_exact_with_parent(lib_name, sym_name):
    raw = get_raw_sym_text(lib_name, sym_name)
    if not raw:
        return ""
    m = re.search(r'\\(extends "([^"]+)"\\)', raw)
    if m:
        parent_name = m.group(1)
        p_lib = lib_name
        p_sym = parent_name
        if ":" in parent_name:
            p_lib, p_sym = parent_name.split(":", 1)
        parent_raw = extract_symbol_exact_with_parent(p_lib, p_sym)
        if parent_raw:
            sub_pat = re.compile(r'[\\t ]*\\(symbol "' + re.escape(p_sym) + r'_([0-9]+_[0-9]+)"(.*?)(?=\\n[\\t ]*\\(symbol |\\n\\t*\\)$)', re.DOTALL)
            parent_subs = []
            for sm in sub_pat.finditer(parent_raw):
                sub_id = sm.group(1)
                sub_body = sm.group(2)
                parent_subs.append(f'    (symbol "{sym_name}_{sub_id}"{sub_body}')
            ext_idx = raw.find('(extends')
            ext_end = raw.find(')', ext_idx) + 1
            raw_no_ext = raw[:ext_idx] + raw[ext_end:]
            last_paren = raw_no_ext.rfind(')')
            raw = raw_no_ext[:last_paren] + "\\n" + "\\n".join(parent_subs) + "\\n  )"
    if not raw.startswith(f'(symbol "{lib_name}:'):
        raw = raw.replace(f'(symbol "{sym_name}"', f'(symbol "{lib_name}:{sym_name}"', 1)
    return raw
'''

new_text = text[:idx1] + flatten_func + text[idx2:]
with open(script_path, "w", encoding="utf-8") as f:
    f.write(new_text)

print("Updated build_zero_erc_fdd.py with recursive flattening!")
