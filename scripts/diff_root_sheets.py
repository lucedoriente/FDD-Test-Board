with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_sch", "r", encoding="utf-8") as f:
    root = f.read()

import re
sheets = list(re.finditer(r'\(sheet\s+\(at[^)]+\).*?\n  \)', root, re.DOTALL))
for i, s in enumerate(sheets):
    print(f"--- Sheet {i+1} ---")
    print(repr(s.group(0)))
