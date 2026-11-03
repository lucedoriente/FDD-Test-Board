with open(r'C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
flags = re.findall(r'PWR_FLAG', text)
print("PWR_FLAG occurrences in build_zero_erc_fdd.py:", len(flags))
