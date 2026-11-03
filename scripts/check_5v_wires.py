with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'\(wire.*?\(global_label "\+5V_REG"', text, re.DOTALL)
print("Matches with +5V_REG:", len(matches))
for m in matches[:3]:
    print("---")
    print(m)
