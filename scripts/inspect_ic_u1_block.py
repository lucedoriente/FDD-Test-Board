import os

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\02_MCU_Core.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(property "Reference" "U1"')
s = text.rfind('(symbol ', 0, idx)
e = text.find('  )', idx)
print(text[s:e+3])
