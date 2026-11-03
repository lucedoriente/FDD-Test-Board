import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(property "Reference" "J5"')
s = text.rfind('(symbol ', 0, idx)
print(text[s:idx+100])
