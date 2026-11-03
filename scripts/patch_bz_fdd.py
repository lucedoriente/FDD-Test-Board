with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace extract_symbol_exact_with_parent
old_func_start = "def extract_symbol_exact_with_parent(lib_name, sym_name):"
idx_start = code.find(old_func_start)
idx_end = code.find("def get_symbol_pins_for_unit(", idx_start)

new_func = """def extract_raw_sym_text(lib_name, sym_name):
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
    child_txt = extract_raw_sym_text(lib_name, sym_name)
    if not child_txt:
        return ""
    m = re.search(r'\\(extends "([^"]+)"\\)', child_txt)
    if not m:
        return child_txt.replace(f'(symbol "{sym_name}"', f'(symbol "{lib_name}:{sym_name}"', 1)
    
    parent_name = m.group(1)
    p_lib = lib_name
    p_sym = parent_name
    if ":" in parent_name:
        p_lib, p_sym = parent_name.split(":", 1)
    
    parent_txt = extract_raw_sym_text(p_lib, p_sym)
    m_gp = re.search(r'\\(extends "([^"]+)"\\)', parent_txt)
    while m_gp:
        gp_name = m_gp.group(1)
        gp_lib = p_lib
        gp_sym = gp_name
        if ":" in gp_name:
            gp_lib, gp_sym = gp_name.split(":", 1)
        gp_txt = extract_raw_sym_text(gp_lib, gp_sym)
        if not gp_txt: break
        parent_txt = gp_txt
        p_sym = gp_sym
        m_gp = re.search(r'\\(extends "([^"]+)"\\)', parent_txt)
    
    # Extract each sub-symbol from parent_txt
    sub_symbols = []
    idx = 0
    prefix = f'(symbol "{p_sym}_'
    while True:
        pos = parent_txt.find(prefix, idx)
        if pos == -1: break
        c, end = 0, pos
        for i in range(pos, len(parent_txt)):
            if parent_txt[i] == '(': c += 1
            elif parent_txt[i] == ')':
                c -= 1
                if c == 0:
                    end = i + 1; break
        sub_body = parent_txt[pos:end]
        sub_child = sub_body.replace(f'(symbol "{p_sym}_', f'(symbol "{sym_name}_', 1)
        sub_symbols.append(sub_child)
        idx = end
    
    # In child_txt: remove (extends ...)
    ext_idx = child_txt.find('(extends')
    ext_end = child_txt.find(')', ext_idx) + 1
    child_clean = child_txt[:ext_idx].rstrip() + "\\n" + child_txt[ext_end:].lstrip()
    
    last_paren = child_clean.rfind(')')
    child_final = child_clean[:last_paren].rstrip() + "\\n\\t\\t" + "\\n\\t\\t".join(sub_symbols) + "\\n\\t)"
    return child_final.replace(f'(symbol "{sym_name}"', f'(symbol "{lib_name}:{sym_name}"', 1)

"""

new_code = code[:idx_start] + new_func + code[idx_end:]

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py", "w", encoding="utf-8") as f:
    f.write(new_code)

print("Updated build_zero_erc_fdd.py with clean flattening engine!")
