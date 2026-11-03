import os

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(property "Reference" "J1"')
s = text.rfind('(symbol ', 0, idx)
e = text.find('\n  )', idx)
print(text[s:e+5])
