import subprocess, os, re

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"
prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

with open(os.path.join(prj_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    full_ps = f.read()

# Let's extract:
# 1. Header (up to lib_symbols)
# 2. lib_symbols block
# 3. Everything between lib_symbols and sheet_instances (wires, symbols, labels)
# 4. sheet_instances

ls_start = full_ps.find('(lib_symbols')
cnt = 0
for i, c in enumerate(full_ps[ls_start:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            ls_block = full_ps[ls_start:ls_start+i+1]
            break

hdr = full_ps[:ls_start]
body_start = ls_start + len(ls_block)
si_start = full_ps.rfind('(sheet_instances')
body = full_ps[body_start:si_start]
footer = """  (sheet_instances
    (path "/"
      (page "1")
    )
  )
)
"""

# Let's split body into sections: symbols, wires, labels
# Notice that comments separate sections! E.g. ;; --- J1 ...
sections = body.split(';; --- ')
print(f"Total sections in 01_Power_Supply body: {len(sections)}")

for i in range(1, len(sections) + 1):
    test_body = ";; --- ".join(sections[:i])
    # Let's build the test file
    test_sch = f"{hdr}\n{ls_block}\n{test_body}\n{footer}"
    with open(os.path.join(test_dir, "01_Power_Supply.kicad_sch"), "w", encoding="utf-8") as f:
        f.write(test_sch)
    out_f = os.path.join(test_dir, f"test_sec_{i}.net")
    res = subprocess.run([kicad_cli, "sch", "export", "netlist", os.path.join(test_dir, "FDD-Test-Board.kicad_sch"), "-o", out_f], capture_output=True, text=True)
    with open(out_f, "r", encoding="utf-8") as f:
        txt = f.read()
    comps = re.findall(r'\(comp \(ref "([^"]+)"\)', txt)
    sec_name = sections[i-1].split('\n')[0] if i > 1 else "Prelude"
    print(f"Section {i} ({sec_name[:40]}): {len(comps)} comps exported -> {comps}")
    if len(comps) == 0 and i > 1:
        print(f"BREAKAGE HAPPENED AT SECTION {i}!")
        break
