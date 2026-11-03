import os, re, subprocess

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"
prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

with open(os.path.join(prj_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    ps = f.read()

# Let's see: what if we take the exact working sub.kicad_sch (which exported Q1),
# and replace Q1 with J1?
with open(os.path.join(test_dir, "sub.kicad_sch"), "r", encoding="utf-8") as f:
    sub = f.read()

# Find J1 in ps
j1_start = ps.find('(property "Reference" "J1"')
s = ps.rfind('(symbol ', 0, j1_start)
# find closing paren of symbol J1
cnt = 0
for i, c in enumerate(ps[s:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            sym_j1 = ps[s:s+i+1]
            break

# Find Conn_01x02_Pin in ps lib_symbols
ls_j1_start = ps.find('(symbol "Connector:Conn_01x02_Pin"')
cnt = 0
for i, c in enumerate(ps[ls_j1_start:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            lib_j1 = ps[ls_j1_start:ls_j1_start+i+1]
            break

# Construct minimal schematic with ONLY J1
test_sch = f"""(kicad_sch
  (version 20250114)
  (generator "eeschema")
  (generator_version "9.0")
  (uuid "b20a3201-2001-4001-8001-000000000002")
  (paper "A3")
  (lib_symbols
    {lib_j1}
  )
  {sym_j1}
  (sheet_instances
    (path "/"
      (page "1")
    )
  )
)
"""

with open(os.path.join(test_dir, "01_Power_Supply.kicad_sch"), "w", encoding="utf-8") as f:
    f.write(test_sch)

out_f = os.path.join(test_dir, "test_j1_alone.net")
res = subprocess.run([kicad_cli, "sch", "export", "netlist", os.path.join(test_dir, "FDD-Test-Board.kicad_sch"), "-o", out_f], capture_output=True, text=True)

with open(out_f, "r", encoding="utf-8") as f:
    txt = f.read()

comps = re.findall(r'\(comp \(ref "([^"]+)"\)', txt)
print(f"J1 alone exported: {len(comps)} comps -> {comps}")
