with open('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/02_MCU_Core.kicad_sch', 'r', encoding='utf-8') as f:
    s2 = f.read()

import re

# find wire near USART1_TX
lines = s2.splitlines()
for i, line in enumerate(lines):
    if "USART1_TX" in line:
        print(f"L{i+1}: {line}")
        for j in range(max(0, i-5), min(len(lines), i+15)):
            print(f"  {lines[j]}")
