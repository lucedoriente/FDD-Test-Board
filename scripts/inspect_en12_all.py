with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch", "r", encoding="utf-8") as f:
    s2 = f.read()

import re
matches = [m.start() for m in re.finditer(r'EN_12V', s2)]
print("Occurrences of EN_12V in S2:", len(matches))
for idx in matches:
    print(s2[idx-50:idx+150])
