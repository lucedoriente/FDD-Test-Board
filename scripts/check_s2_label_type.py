with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

import re
labels = re.findall(r'\((global_label|label)\s+"(USART1_TX|USART1_RX|\+5V_REG|-12V_DRV)"', text)
print("Labels on Sheet 2:", labels)
