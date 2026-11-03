import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    t = f.read()

idx1 = t.find('(symbol "power:GND"')
print(t[idx1:idx1+800])
