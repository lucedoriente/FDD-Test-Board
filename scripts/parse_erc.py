import os, re
from collections import Counter

rpt_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board-erc.rpt"
if not os.path.exists(rpt_path):
    rpt_path = "FDD-Test-Board-erc.rpt"

with open(rpt_path, "r", encoding="utf-8") as f:
    text = f.read()

types = re.findall(r'\[([^\]]+)\]:', text)
c = Counter(types)
print("Violation counts by type:")
for t, cnt in c.most_common():
    print(f"  {t}: {cnt}")

lines = text.split("\n")
print("\nFirst 30 lines of violations:")
for l in lines[:40]:
    if l.strip():
        print(l)
