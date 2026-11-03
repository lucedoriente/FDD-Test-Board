with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\04_FDD_Interfaces.kicad_sch", "r", encoding="utf-8") as f:
    s4 = f.read()

for line in s4.splitlines():
    if "381.00" in line:
        print(line)
