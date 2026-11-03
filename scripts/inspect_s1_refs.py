import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

refs = re.findall(r'\(property "Reference" "([^#"][^"]*)"', text)
print("Sheet 1 components:", sorted(set(refs)))
