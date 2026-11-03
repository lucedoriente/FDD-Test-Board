import os, re, subprocess

cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"
td = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"
prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"

with open(os.path.join(prj_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    ps = f.read()

# Extract individual symbols from lib_symbols in ps
ls_start = ps.find('(lib_symbols')
# Find matching end of lib_symbols
cnt = 0
for i, c in enumerate(ps[ls_start:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            ls_body = ps[ls_start + len('(lib_symbols'): ls_start + i]
            break

# Now parse individual top-level (symbol ... in ls_body
symbols = []
idx = 0
while True:
    pos = ls_body.find('(symbol "', idx)
    if pos == -1: break
    c = 0
    for j in range(pos, len(ls_body)):
        if ls_body[j] == '(': c += 1
        elif ls_body[j] == ')':
            c -= 1
            if c == 0:
                symbols.append(ls_body[pos:j+1])
                idx = j + 1
                break

print(f"Total symbols in 01_Power_Supply lib_symbols: {len(symbols)}")

# Base working sub.kicad_sch J1 instance
with open(os.path.join(td, "sub.kicad_sch"), "r", encoding="utf-8") as f:
    base_sub = f.read()
# Extract J1 instance
j1_inst_start = base_sub.find('(symbol (lib_id')
j1_inst = base_sub[j1_inst_start:]

# Test adding symbols one by one
accumulated_syms = []
for s in symbols:
    m = re.match(r'\(symbol "([^"]+)"', s)
    sname = m.group(1) if m else "unknown"
    accumulated_syms.append(s)
    
    test_sub = f"""(kicad_sch
  (version 20250114)
  (generator "eeschema")
  (generator_version "9.0")
  (uuid "33333333-3333-3333-3333-333333333333")
  (paper "A4")
  (lib_symbols
    {' '.join(accumulated_syms)}
  )
  {j1_inst}
"""
    with open(os.path.join(td, "sub.kicad_sch"), "w", encoding="utf-8") as f:
        f.write(test_sub)
    
    out_net = os.path.join(td, "out_sub.net")
    res = subprocess.run([cli, "sch", "export", "netlist", os.path.join(td, "FDD-Test-Board.kicad_sch"), "-o", out_net], capture_output=True, text=True)
    with open(out_net, "r", encoding="utf-8") as f:
        txt = f.read()
    comps = re.findall(r'\(comp \(ref "([^"]+)"\)', txt)
    if len(comps) == 0:
        print(f"FAILED on adding symbol: {sname}!")
        break
    else:
        print(f"OK with {sname}")
