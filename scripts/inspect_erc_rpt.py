import os

rpt_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board-erc.rpt"
if not os.path.exists(rpt_path):
    rpt_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\FDD-Test-Board-erc.rpt"

with open(rpt_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Total report lines:", len(lines))
counts = {}
for l in lines:
    if "ERC report" in l or "Sheet" in l or "Date" in l:
        print(l.strip())
    if l.strip().startswith("["):
        err_type = l.strip().split("]")[0] + "]"
        counts[err_type] = counts.get(err_type, 0) + 1

print("\nViolation counts:")
for k, v in counts.items():
    print(f"  {k}: {v}")

print("\nSample violations:")
for l in lines[:40]:
    print(l, end="")
