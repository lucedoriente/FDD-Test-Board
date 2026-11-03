import os

rpt_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board-erc.rpt"
with open(rpt_path, "r", encoding="utf-8") as f:
    text = f.read()

for l in text.splitlines():
    if l.startswith("[") or "Sheet" in l or "error" in l or "warning" in l:
        print(l)
