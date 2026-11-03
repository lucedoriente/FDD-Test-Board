with open('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/FDD-Test-Board.net', 'r', encoding='utf-8') as f:
    net = f.read()

import re
lines = net.splitlines()
for i, line in enumerate(lines):
    if 'ref "J5"' in line:
        for j in range(max(0, i-5), min(len(lines), i+8)):
            print(lines[j])
