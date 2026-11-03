with open('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/02_MCU_Core.kicad_sch', 'r', encoding='utf-8') as f:
    s2 = f.read()

import re
matches = re.findall(r'\(symbol "([^"]+)"', s2)
print("Symbols in S2 lib_symbols:", matches[:15])
