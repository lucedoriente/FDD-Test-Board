script_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py"

with open(script_path, "r", encoding="utf-8") as f:
    text = f.read()

idx1 = text.find("def get_raw_sym_text(")
idx2 = text.find("def get_symbol_pins_for_unit(")

orig_func = '''def extract_symbol_exact_with_parent(lib_name, sym_name):
    p = os.path.join(sym_dir, f"{lib_name}.kicad_sym")
    if not os.path.exists(p):
        return ""
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()

    def get_sym(name):
        start_tag = f'(symbol "{name}"'
        idx = content.find(start_tag)
        if idx == -1: return ""
        count, end = 0, 0
        for i in range(idx, len(content)):
            if content[i] == '(': count += 1
            elif content[i] == ')':
                count -= 1
                if count == 0:
                    end = i + 1; break
        return content[idx:end]

    raw_child = get_sym(sym_name)
    if not raw_child:
        return ""
    
    m = re.search(r'\\(extends "([^"]+)"\\)', raw_child)
    if m:
        parent_name = m.group(1)
        raw_parent = get_sym(parent_name)
        if raw_parent:
            m_gp = re.search(r'\\(extends "([^"]+)"\\)', raw_parent)
            gp_txt = ""
            if m_gp:
                gp_name = m_gp.group(1)
                raw_gp = get_sym(gp_name)
                if raw_gp:
                    gp_txt = raw_gp.replace(f'(symbol "{gp_name}"', f'(symbol "{lib_name}:{gp_name}"', 1)
                    raw_parent = raw_parent.replace(f'(extends "{gp_name}"', f'(extends "{lib_name}:{gp_name}"', 1)
            raw_parent = raw_parent.replace(f'(symbol "{parent_name}"', f'(symbol "{lib_name}:{parent_name}"', 1)
            raw_child = raw_child.replace(f'(symbol "{sym_name}"', f'(symbol "{lib_name}:{sym_name}"', 1)
            raw_child = raw_child.replace(f'(extends "{parent_name}"', f'(extends "{lib_name}:{parent_name}"', 1)
            parts = [p for p in [gp_txt, raw_parent, raw_child] if p]
            return "\\n".join(parts)
        
    return raw_child.replace(f'(symbol "{sym_name}"', f'(symbol "{lib_name}:{sym_name}"', 1)

'''

new_text = text[:idx1] + orig_func + text[idx2:]
with open(script_path, "w", encoding="utf-8") as f:
    f.write(new_text)

print("Restored original extract_symbol_exact_with_parent!")
