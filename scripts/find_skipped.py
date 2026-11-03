import os
from bisect_wires_labels import top_exprs

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
with open(os.path.join(prj_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    orig = f.read()

# Let's find body in orig
ls_start = orig.find('(lib_symbols')
cnt = 0
for i, c in enumerate(orig[ls_start:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            ls_end = ls_start + i + 1
            break

si_start = orig.rfind('(sheet_instances')
body = orig[ls_end:si_start]

# Reconstruct what was skipped in body
curr = 0
skipped_chunks = []
for expr in top_exprs:
    idx = body.find(expr, curr)
    if idx > curr:
        skipped = body[curr:idx].strip()
        if skipped:
            skipped_chunks.append(skipped)
    curr = idx + len(expr)

rem = body[curr:].strip()
if rem:
    skipped_chunks.append(rem)

print(f"Skipped {len(skipped_chunks)} chunks in body:")
for c in skipped_chunks:
    print("--- CHUNK ---")
    print(c)
