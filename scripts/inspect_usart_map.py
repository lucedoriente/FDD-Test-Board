with open('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/02_MCU_Core.kicad_sch', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(5855, min(len(lines), 5885)):
    print(f"{i+1}: {lines[i].rstrip()}")
