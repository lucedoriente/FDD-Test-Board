with open('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/FDD-Test-Board.kicad_sch', 'r', encoding='utf-8') as f:
    root = f.read()

import re
sheets = re.findall(r'\(sheet .*?\n  \)', root, re.DOTALL)
for s in sheets:
    print(s)
    print("="*40)
