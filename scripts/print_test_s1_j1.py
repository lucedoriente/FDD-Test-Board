import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single\01_Power_Supply.kicad_sch", "r") as f:
    text = f.read()

idx = text.find('(property "Reference" "J1"')
s = text.rfind('(symbol ', 0, idx)
e = text.find('  )', idx)
print(text[s:e+5])
