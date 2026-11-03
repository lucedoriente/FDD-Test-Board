with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_sch", "r", encoding="utf-8") as f:
    txt = f.read()

import re
labels = re.findall(r'\(.*label.*?\)', txt)
print("Labels in FDD-Test-Board.kicad_sch:", labels)
