with open('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/04_FDD_Interfaces.kicad_sch', 'r', encoding='utf-8') as f:
    s4 = f.read()

lines = s4.splitlines()
for i, line in enumerate(lines):
    if "-12V_DRV" in line:
        print(f"L{i+1}: {line}")
        for j in range(max(0, i-4), min(len(lines), i+8)):
            print(f"  {lines[j]}")
