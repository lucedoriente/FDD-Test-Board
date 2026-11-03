import os, re, subprocess

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"
prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

with open(os.path.join(prj_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    ps = f.read()

# Let's see: what if we add wires and labels one by one?
# In ps, elements are (wire ...), (global_label ...), (label ...), (symbol ...)
# We know all (symbol ...) are fine.
# Let's extract all non-symbol elements from the body:
ls_start = ps.find('(lib_symbols')
cnt = 0
for i, c in enumerate(ps[ls_start:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            full_ls = ps[ls_start:ls_start+i+1]
            break

body_start = ls_start + len(full_ls)
si_start = ps.rfind('(sheet_instances')
body = ps[body_start:si_start]

# Parse top-level expressions in body
top_exprs = []
idx = 0
while idx < len(body):
    while idx < len(body) and body[idx] in ' \t\r\n':
        idx += 1
    if idx >= len(body): break
    if body[idx] == ';': # comment
        c_end = body.find('\n', idx)
        if c_end == -1: c_end = len(body)
        idx = c_end + 1
        continue
    if body[idx] == '(':
        c_cnt = 0
        start = idx
        for j in range(idx, len(body)):
            if body[j] == '(': c_cnt += 1
            elif body[j] == ')':
                c_cnt -= 1
                if c_cnt == 0:
                    top_exprs.append(body[start:j+1])
                    idx = j + 1
                    break
    else:
        idx += 1

print(f"Total top-level expressions in body: {len(top_exprs)}")
types = {}
for e in top_exprs:
    tag = e.split()[0][1:]
    types[tag] = types.get(tag, 0) + 1
print("Expression types:", types)

# Now, let's incrementally add expressions from 0 to N and test export!
# We can bisect!
low = 0
high = len(top_exprs)
last_working = 0

def test_expr_count(count):
    sub_body = "\n".join(top_exprs[:count])
    test_sch = f"""(kicad_sch
  (version 20250114)
  (generator "eeschema")
  (generator_version "9.0")
  (uuid "b20a3201-2001-4001-8001-000000000002")
  (paper "A3")
  {full_ls}
  {sub_body}
  (sheet_instances
    (path "/"
      (page "1")
    )
  )
)
"""
    with open(os.path.join(test_dir, "01_Power_Supply.kicad_sch"), "w", encoding="utf-8") as f:
        f.write(test_sch)
    out_f = os.path.join(test_dir, f"test_bisect.net")
    res = subprocess.run([kicad_cli, "sch", "export", "netlist", os.path.join(test_dir, "FDD-Test-Board.kicad_sch"), "-o", out_f], capture_output=True, text=True)
    with open(out_f, "r", encoding="utf-8") as f:
        txt = f.read()
    comps = re.findall(r'\(comp \(ref "([^"]+)"\)', txt)
    return len(comps)

print("Testing count = len(top_exprs):", test_expr_count(len(top_exprs)))

# Binary search for the first breaking expression
while low <= high:
    mid = (low + high) // 2
    n_comps = test_expr_count(mid)
    # Count how many symbols are in top_exprs[:mid]
    expected_syms = sum(1 for e in top_exprs[:mid] if e.startswith('(symbol') and not re.search(r'\(property "Reference" "#', e))
    print(f"Mid={mid}/{len(top_exprs)}, n_comps={n_comps}, expected_syms={expected_syms}")
    if n_comps == 0 and mid > 0:
        # Broken! The bad element is <= mid
        high = mid - 1
    else:
        last_working = mid
        low = mid + 1

first_bad = last_working + 1
print(f"FIRST BAD EXPRESSION IS AT INDEX {first_bad-1}:")
if first_bad - 1 < len(top_exprs):
    print(top_exprs[first_bad - 1])
