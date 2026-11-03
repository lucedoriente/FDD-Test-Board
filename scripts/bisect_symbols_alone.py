import os, re, subprocess

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"
prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

with open(os.path.join(prj_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    ps = f.read()

ls_start = ps.find('(lib_symbols')
cnt = 0
for i, c in enumerate(ps[ls_start:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            full_ls = ps[ls_start:ls_start+i+1]
            break

# Extract all (symbol ...) instances in the body
# Everything after full_ls up to sheet_instances
body_start = ls_start + len(full_ls)
si_start = ps.rfind('(sheet_instances')
body = ps[body_start:si_start]

# Find all symbol instances in body
sym_indices = [m.start() for m in re.finditer(r'\n  \(symbol ', body)]
sym_indices.append(len(body))

symbols = []
for i in range(len(sym_indices) - 1):
    chunk = body[sym_indices[i]:sym_indices[i+1]]
    # extract only the (symbol ... )
    s_start = chunk.find('(symbol ')
    # count parens
    cnt = 0
    for j, ch in enumerate(chunk[s_start:]):
        if ch == '(': cnt += 1
        elif ch == ')':
            cnt -= 1
            if cnt == 0:
                symbols.append(chunk[s_start:s_start+j+1])
                break

print(f"Total symbol instances in body: {len(symbols)}")

# Let's test each symbol instance alone!
for idx, sym in enumerate(symbols):
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', sym)
    ref = ref_m.group(1) if ref_m else f"sym_{idx}"
    
    test_sch = f"""(kicad_sch
  (version 20250114)
  (generator "eeschema")
  (generator_version "9.0")
  (uuid "b20a3201-2001-4001-8001-000000000002")
  (paper "A3")
  {full_ls}
  {sym}
  (sheet_instances
    (path "/"
      (page "1")
    )
  )
)
"""
    with open(os.path.join(test_dir, "01_Power_Supply.kicad_sch"), "w", encoding="utf-8") as f:
        f.write(test_sch)
    out_f = os.path.join(test_dir, f"test_sym_{idx}.net")
    res = subprocess.run([kicad_cli, "sch", "export", "netlist", os.path.join(test_dir, "FDD-Test-Board.kicad_sch"), "-o", out_f], capture_output=True, text=True)
    with open(out_f, "r", encoding="utf-8") as f:
        txt = f.read()
    comps = re.findall(r'\(comp \(ref "([^"]+)"\)', txt)
    print(f"Symbol {idx} ({ref}): {len(comps)} comps exported -> {comps}")
