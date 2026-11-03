with open('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/FDD-Test-Board.net', 'r', encoding='utf-8') as f:
    net = f.read()

import re
lines = net.splitlines()
for i, line in enumerate(lines):
    if '-12V_DRV' in line or 'J4' in line:
        for j in range(max(0, i-2), min(len(lines), i+6)):
            print(lines[j])
