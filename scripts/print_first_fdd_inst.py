import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\04_FDD_Interfaces.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

# find first component instance
m = re.search(r'\(instances.*?\n    \)', text, re.DOTALL)
print(m.group(0))
