with open('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/04_FDD_Interfaces.kicad_sch', 'r', encoding='utf-8') as f:
    s4 = f.read()

import re
pins = re.findall(r'\(pin\s+\w+\s+\w+\s+\(at\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\).*?\(number\s+"(\d+)"', s4[s4.find('Conn_02x10_Odd_Even_1_1'):], re.DOTALL)
for p in pins[:25]:
    print(f"Pin {p[3]}: at ({p[0]}, {p[1]}) rot={p[2]}")
