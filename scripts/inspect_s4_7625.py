with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\04_FDD_Interfaces.kicad_sch", "r", encoding="utf-8") as f:
    s4 = f.read()

lines = s4.splitlines()
for i in range(7625, min(len(lines), 7645)):
    print(f"{i+1}: {lines[i]}")
