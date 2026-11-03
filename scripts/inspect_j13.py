with open('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/04_FDD_Interfaces.kicad_sch', 'r', encoding='utf-8') as f:
    s4 = f.read()

import re
idx = s4.find('"J13"')
print(s4[idx-50:idx+450])
