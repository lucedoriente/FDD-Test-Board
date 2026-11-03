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

for filename, sheet_uuid in sheets:
    filepath = os.path.join(prj_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Strip all comment lines (starting with ;)
    lines = content.splitlines()
    clean_lines = [l for l in lines if not l.strip().startswith(';')]
    content = "\n".join(clean_lines)
    
    # 2. Fix sheet_instances at the bottom to (path "/" (page "1"))
    si_idx = content.rfind('(sheet_instances')
    if si_idx != -1:
        content = content[:si_idx] + """(sheet_instances
    (path "/"
      (page "1")
    )
  )
)"""
    
    # 3. Fix all instances blocks to single path
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
    
    # 4. Resolve any (extends ...) in lib_symbols
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
        
        # Check if there are extends in ls_block
        extends_list = re.findall(r'\(symbol "([^"]+)".*?\(extends "([^"]+)"\)', ls_block, re.DOTALL)
        if extends_list:
            print(f"Sheet {filename} has extends: {extends_list}")
            for child_sym, parent_sym in extends_list:
                # Get flattened version of child_sym
                p_lib, p_name = child_sym.split(":", 1) if ":" in child_sym else ("", child_sym)
                flat = get_flattened_symbol(p_lib, p_name)
                if flat:
                    # Remove the child symbol definition from ls_block
                    # and remove the parent symbol definition if present
                    for s_to_remove in [child_sym, parent_sym, f"{p_lib}:{parent_sym}"]:
                        tag = f'(symbol "{s_to_remove}"'
                        idx = ls_block.find(tag)
                        if idx != -1:
                            c_cnt = 0
                            for j, ch in enumerate(ls_block[idx:]):
                                if ch == '(': c_cnt += 1
                                elif ch == ')':
                                    c_cnt -= 1
                                    if c_cnt == 0:
                                        ls_block = ls_block[:idx] + ls_block[idx+j+1:]
                                        break
                    # Insert flat before closing paren of ls_block
                    last_p = ls_block.rfind(')')
                    ls_block = ls_block[:last_p] + f"\n{flat}\n  )"
            
            content = content[:ls_start] + ls_block + content[ls_end:]
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully processed {filename}!")

# Export full project netlist!
net_path = os.path.join(prj_dir, "FDD-Test-Board.net")
res = subprocess.run([kicad_cli, "sch", "export", "netlist", os.path.join(prj_dir, "FDD-Test-Board.kicad_sch"), "-o", net_path], capture_output=True, text=True)
print("Export return code:", res.returncode)

with open(net_path, "r", encoding="utf-8") as f:
    net_txt = f.read()

comps = re.findall(r'\(comp \(ref "([^"]+)"\)', net_txt)
nets = re.findall(r'\(net \(code "[^"]+"\)\s+\(name "([^"]+)"\)', net_txt)
print(f"Exported netlist: {len(comps)} components, {len(nets)} nets!")
print("Components list:", sorted(comps))
