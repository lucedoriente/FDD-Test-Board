import os, re, subprocess
from test_flatten_engine import get_flattened_symbol
from test_parse_ls import parse_lib_symbols

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

def flatten_sheet(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    ls_start = content.find('(lib_symbols')
    if ls_start == -1: return
    cnt = 0
    for i, c in enumerate(content[ls_start:]):
        if c == '(': cnt += 1
        elif c == ')':
            cnt -= 1
            if cnt == 0:
                ls_end = ls_start + i + 1
                break
    ls_block = content[ls_start:ls_end]
    
    parsed = parse_lib_symbols(ls_block)
    used_syms = set(re.findall(r'\(symbol \(lib_id "([^"]+)"\)', content))
    
    clean_syms = []
    for s_name, s_body in parsed.items():
        ext_m = re.search(r'\(extends "([^"]+)"\)', s_body)
        if ext_m:
            p_lib, p_sym = s_name.split(":", 1) if ":" in s_name else ("", s_name)
            flat = get_flattened_symbol(p_lib, p_sym)
            if flat:
                clean_syms.append(flat)
            else:
                clean_syms.append(s_body)
        else:
            if s_name in used_syms or s_name.startswith("power:"):
                clean_syms.append(s_body)
    
    new_ls = "(lib_symbols\n  " + "\n  ".join(clean_syms) + "\n  )"
    new_content = content[:ls_start] + new_ls + content[ls_end:]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Flattened {os.path.basename(filepath)}!")

for s in ["01_Power_Supply.kicad_sch", "02_MCU_Core.kicad_sch", "03_UI_Controls.kicad_sch", "04_FDD_Interfaces.kicad_sch"]:
    flatten_sheet(os.path.join(prj_dir, s))

# Run ERC on full project
erc_rpt = os.path.join(prj_dir, "FDD-Test-Board-erc.rpt")
res_erc = subprocess.run([kicad_cli, "sch", "erc", os.path.join(prj_dir, "FDD-Test-Board.kicad_sch"), "-o", erc_rpt], capture_output=True, text=True)
with open(erc_rpt, "r", encoding="utf-8") as f:
    text = f.read()

sheets = text.split("***** Sheet ")
for s in sheets[1:]:
    sheet_name = s.splitlines()[0]
    lines = s.splitlines()[1:]
    v_lines = [l for l in lines if l.startswith("[")]
    print(f"Sheet {sheet_name}: {len(v_lines)} violations")

# Export Netlist
net_file = os.path.join(prj_dir, "FDD-Test-Board.net")
res_net = subprocess.run([kicad_cli, "sch", "export", "netlist", "--output", net_file, os.path.join(prj_dir, "FDD-Test-Board.kicad_sch")], capture_output=True, text=True)
print("Netlist export code:", res_net.returncode)

net_txt = open(net_file, encoding="utf-8").read()
comps = re.findall(r'\(comp\s+\(ref\s+"([^"]+)"\)', net_txt)
nets = re.findall(r'\(net\s+\(code\s+"[^"]+"\)\s+\(name\s+"([^"]+)"\)', net_txt)
print(f"Total components in netlist: {len(comps)}")
print(f"Total nets in netlist: {len(nets)}")
