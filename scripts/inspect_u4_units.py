import re

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\04_FDD_Interfaces.kicad_sch", "r", encoding="utf-8") as f:
    s4 = f.read()

idx = s4.find('(property "Reference" "U4"')
while idx != -1:
    end = s4.find('(instances', idx)
    print(s4[idx:end])
    idx = s4.find('(property "Reference" "U4"', end)
