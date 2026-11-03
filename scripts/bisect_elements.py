import os, re, subprocess

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"
prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

with open(os.path.join(prj_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    ps = f.read()

# Extract full lib_symbols from ps
ls_start = ps.find('(lib_symbols')
cnt = 0
for i, c in enumerate(ps[ls_start:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            full_ls = ps[ls_start:ls_start+i+1]
            break

# Extract J1 symbol
j1_start = ps.find('(property "Reference" "J1"')
s = ps.rfind('(symbol ', 0, j1_start)
cnt = 0
for i, c in enumerate(ps[s:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            sym_j1 = ps[s:s+i+1]
            break

# Test A: Full lib_symbols + J1 only
test_sch_A = f"""(kicad_sch
  (version 20250114)
  (generator "eeschema")
  (generator_version "9.0")
  (uuid "b20a3201-2001-4001-8001-000000000002")
  (paper "A3")
  {full_ls}
  {sym_j1}
  (sheet_instances
    (path "/"
      (page "1")
    )
  )
)
"""
with open(os.path.join(test_dir, "01_Power_Supply.kicad_sch"), "w", encoding="utf-8") as f:
    f.write(test_sch_A)

out_f = os.path.join(test_dir, "test_A.net")
res = subprocess.run([kicad_cli, "sch", "export", "netlist", os.path.join(test_dir, "FDD-Test-Board.kicad_sch"), "-o", out_f], capture_output=True, text=True)
with open(out_f, "r", encoding="utf-8") as f:
    txt = f.read()
comps = re.findall(r'\(comp \(ref "([^"]+)"\)', txt)
print(f"Test A (Full lib_symbols + J1): {len(comps)} comps -> {comps}")
