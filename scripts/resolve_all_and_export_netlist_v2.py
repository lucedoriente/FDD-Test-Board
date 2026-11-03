import os, re, subprocess
from test_flatten_engine import get_flattened_symbol

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

sheets = [
    ("01_Power_Supply.kicad_sch", "b20a3201-1001-4001-8001-000000000002"),
    ("02_MCU_Core.kicad_sch", "b20a3201-1001-4001-8001-000000000003"),
    ("03_UI_Controls.kicad_sch", "b20a3201-1001-4001-8001-000000000004"),
    ("04_FDD_Interfaces.kicad_sch", "b20a3201-1001-4001-8001-000000000005"),
]

def parse_lib_symbols(ls_block):
    start = ls_block.find('(lib_symbols')
    inner = ls_block[start+12:].rstrip()
    if inner.endswith(')'):
        inner = inner[:-1]
    
    symbols = {}
    idx = 0
    while idx < len(inner):
        s_idx = inner.find('(symbol "', idx)
        if s_idx == -1: break
        name_end = inner.find('"', s_idx + 9)
        sym_name = inner[s_idx + 9:name_end]
        
        cnt = 0
        end_idx = s_idx
        for j in range(s_idx, len(inner)):
            if inner[j] == '(': cnt += 1
            elif inner[j] == ')':
                cnt -= 1
                if cnt == 0:
                    end_idx = j + 1
                    break
        symbols[sym_name] = inner[s_idx:end_idx]
        idx = end_idx
    return symbols

for filename, sheet_uuid in sheets:
    filepath = os.path.join(prj_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Strip all comment lines (starting with ;)
    lines = content.splitlines()
    clean_lines = [l for l in lines if not l.strip().startswith(';')]
    content = "\n".join(clean_lines)
    
    # 2. Fix sheet_instances at the bottom
    si_idx = content.rfind('(sheet_instances')
    if si_idx != -1:
        content = content[:si_idx] + """(sheet_instances
    (path "/"
      (page "1")
    )
  )
)"""

    # 3. Fix instances blocks
    def fix_inst(m):
        ref = m.group(1)
        unit = m.group(2)
        return f"""    (instances
      (project "FDD-Test-Board"
        (path "/b20a3201-1001-4001-8001-000000000001/{sheet_uuid}"
          (reference "{ref}")
          (unit {unit})
        )
      )
    )"""

    pat = re.compile(r'\(instances\s+\(project\s+"[^"]*"\s+\(path\s+"[^"]*"\s+\(reference\s+"([^"]+)"\)\s+\(unit\s+(\d+)\)\s+\).*?\n    \)', re.DOTALL)
    content = pat.sub(fix_inst, content)
    
    # 4. Resolve extends in lib_symbols
    ls_start = content.find('(lib_symbols')
    if ls_start != -1:
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
        
        # Check which symbols are used by components in this sheet
        used_syms = set(re.findall(r'\(symbol \(lib_id "([^"]+)"\)', content))
        
        clean_symbols = {}
        for sym_name, sym_body in parsed.items():
            ext_m = re.search(r'\(extends "([^"]+)"\)', sym_body)
            if ext_m:
                p_lib, p_sym = sym_name.split(":", 1) if ":" in sym_name else ("", sym_name)
                print(f"Flattening {sym_name} in {filename}...")
                flat = get_flattened_symbol(p_lib, p_sym)
                clean_symbols[sym_name] = flat
            else:
                clean_symbols[sym_name] = sym_body
        
        # Now remove any parent symbols that are not used by any component
        final_syms = []
        for sym_name, sym_body in clean_symbols.items():
            if sym_name not in used_syms and not sym_name.startswith("power:"):
                # If it's not used directly by any component, we can omit it
                print(f"Dropping unused symbol {sym_name} from {filename}")
                continue
            final_syms.append(sym_body)
        
        new_ls_block = "(lib_symbols\n" + "\n".join(final_syms) + "\n  )"
        content = content[:ls_start] + new_ls_block + content[ls_end:]
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Done processing {filename}!")

# Export full project netlist!
net_path = os.path.join(prj_dir, "FDD-Test-Board.net")
res = subprocess.run([kicad_cli, "sch", "export", "netlist", os.path.join(prj_dir, "FDD-Test-Board.kicad_sch"), "-o", net_path], capture_output=True, text=True)
print("Export return code:", res.returncode)

with open(net_path, "r", encoding="utf-8") as f:
    net_txt = f.read()

comps = re.findall(r'\(comp \(ref "([^"]+)"\)', net_txt)
nets = re.findall(r'\(net \(code "[^"]+"\)\s+\(name "([^"]+)"\)', net_txt)
print(f"\n=======================================================")
print(f"FULL PROJECT NETLIST EXPORT RESULT:")
print(f"Total Components: {len(comps)}")
print(f"Total Nets: {len(nets)}")
print(f"Components list: {sorted(comps)}")
print(f"=======================================================")
