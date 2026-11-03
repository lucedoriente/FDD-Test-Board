with open('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/01_Power_Supply.kicad_sch', 'r', encoding='utf-8') as f:
    s1 = f.read()

lines = s1.splitlines()
for i, line in enumerate(lines):
    if "USART1_TX" in line or "345.44" in line:
        for j in range(max(0, i-3), min(len(lines), i+6)):
            print(f"{j+1}: {lines[j]}")
