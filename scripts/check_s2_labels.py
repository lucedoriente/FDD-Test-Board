import os, re
with open(r'C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()
labels = re.findall(r'\(global_label "([^"]+)"', text)
for l in ['EN_24V', 'ISENSE_24V', 'EN_12V', 'ISENSE_12V', 'EN_5V', 'ISENSE_5V', 'USART1_TX', 'USART1_RX']:
    print(l, 'in Sheet 2?', l in labels)
