import os, re, subprocess

sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
local_sym_path = os.path.join(prj_dir, "FDD-Test-Board.kicad_sym")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

def extract_symbol_exact(lib_name, sym_name):
    if lib_name == "FDD-Test-Board":
        lib_path = local_sym_path
    else:
        lib_path = os.path.join(sym_dir, lib_name + ".kicad_sym")
        
    if not os.path.exists(lib_path):
        print(f"WARNING: lib not found {lib_path}")
        return ""
        
    with open(lib_path, "r", encoding="utf-8") as f:
        content = f.read()
    start_tag = f'(symbol "{sym_name}"'
    idx = content.find(start_tag)
    if idx == -1:
        print(f"WARNING: symbol {sym_name} not found in {lib_name}")
        return ""
    depth = 0
    end_idx = idx
    for i in range(idx, len(content)):
        if content[i] == '(':
            depth += 1
        elif content[i] == ')':
            depth -= 1
            if depth == 0:
                end_idx = i + 1
                break
    sym_text = content[idx:end_idx]
    
    # Check if extends
    m_ext = re.search(r'\(extends "([^"]+)"\)', sym_text)
    if m_ext:
        parent_name = m_ext.group(1)
        if ":" in parent_name:
            p_lib, p_name = parent_name.split(":", 1)
            p_lib_path = os.path.join(sym_dir, p_lib + ".kicad_sym")
            with open(p_lib_path, "r", encoding="utf-8") as pf:
                p_content = pf.read()
        else:
            p_name = parent_name
            p_content = content
            
        p_start_tag = f'(symbol "{p_name}"'
        p_idx = p_content.find(p_start_tag)
        if p_idx != -1:
            p_depth = 0
            p_end = p_idx
            for i in range(p_idx, len(p_content)):
                if p_content[i] == '(':
                    p_depth += 1
                elif p_content[i] == ')':
                    p_depth -= 1
                    if p_depth == 0:
                        p_end = i + 1
                        break
            p_sym_text = p_content[p_idx:p_end]
            sub_pattern = re.compile(r'[\t ]+\(symbol "' + re.escape(p_name) + r'_([0-9]+_[0-9]+)"(.*?)(?=\n[\t ]+\(symbol |\n\t*\)$)', re.DOTALL)
            parent_sub_symbols = []
            for m in sub_pattern.finditer(p_sym_text):
                sub_id = m.group(1)
                sub_body = m.group(2)
                parent_sub_symbols.append(f'  (symbol "{sym_name}_{sub_id}"{sub_body}')
            
            parent_graphics = "\n".join(parent_sub_symbols)
            idx_ext = sym_text.find('(extends')
            idx_ext_end = sym_text.find(')', idx_ext) + 1
            sym_clean = sym_text[:idx_ext] + sym_text[idx_ext_end:]
            idx_last = sym_clean.rfind(')')
            sym_text = sym_clean[:idx_last] + "\n" + parent_graphics + "\n)"

    if not sym_text.startswith(f'(symbol "{lib_name}:'):
        sym_text = sym_text.replace(f'(symbol "{sym_name}"', f'(symbol "{lib_name}:{sym_name}"', 1)
    return sym_text

# Standard power symbols
power_syms = "\n".join([
    extract_symbol_exact("power", "GND"),
    extract_symbol_exact("power", "PWR_FLAG"),
    extract_symbol_exact("power", "+3.3V"),
    extract_symbol_exact("power", "+5V"),
    extract_symbol_exact("power", "+12V"),
    extract_symbol_exact("power", "+24V"),
    extract_symbol_exact("power", "-12V")
])

subsheets = [
    "01_Power_Supply.kicad_sch",
    "02_MCU_Core.kicad_sch",
    "03_UI_Controls.kicad_sch",
    "04_FDD_Interfaces.kicad_sch"
]

for sfile in subsheets:
    spath = os.path.join(prj_dir, sfile)
    with open(spath, "r", encoding="utf-8") as f:
        text = f.read()
        
    # Find all used lib_ids in symbols on the sheet
    used_lib_ids = set(re.findall(r'\(symbol \(lib_id "([^"]+)"\)', text))
    print(f"\n{sfile} uses {len(used_lib_ids)} unique library symbols:")
    
    extracted_defs = []
    for lid in sorted(used_lib_ids):
        if lid.startswith("power:"):
            continue
        if ":" not in lid:
            print(f"  Skipping non-colon symbol: {lid}")
            continue
        lib, sname = lid.split(":", 1)
        sdef = extract_symbol_exact(lib, sname)
        if sdef:
            print(f"  OK: {lid} (len={len(sdef)}, extends={'extends' in sdef})")
            extracted_defs.append(sdef)
        else:
            print(f"  ERROR: could not extract {lid}")
            
    all_lib_symbols = power_syms + "\n" + "\n".join(extracted_defs)
    
    # Replace (lib_symbols ...) in text
    ls_start = text.find('(lib_symbols')
    cnt = 0
    for i, c in enumerate(text[ls_start:]):
        if c == '(':
            cnt += 1
        elif c == ')':
            cnt -= 1
            if cnt == 0:
                ls_end = ls_start + i + 1
                break
                
    new_lib_block = f"(lib_symbols\n{all_lib_symbols}\n  )"
    text = text[:ls_start] + new_lib_block + text[ls_end:]
    
    # Ensure sheet_instances at end
    idx_si = text.rfind('(sheet_instances')
    target_si = """  (sheet_instances
    (path "/"
      (page "1")
    )
  )
)
"""
    if idx_si != -1:
        text = text[:idx_si] + target_si
        
    with open(spath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Updated {sfile} successfully!")

print("\n--- Running kicad-cli sch export netlist ---")
net_path = os.path.join(prj_dir, "FDD-Test-Board.net")
cmd = [kicad_cli, "sch", "export", "netlist", os.path.join(prj_dir, "FDD-Test-Board.kicad_sch"), "-o", net_path]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)

with open(net_path, "r", encoding="utf-8") as f:
    net_txt = f.read()

comps = re.findall(r'\(comp \(ref "([^"]+)"\)', net_txt)
nets = re.findall(r'\(net \(code "[^"]+"\)\s+\(name "([^"]+)"\)', net_txt)
print(f"\nSUCCESS! Netlist exported with {len(comps)} components and {len(nets)} nets!")
print("Sample components:", comps[:25])
