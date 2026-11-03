with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    s1 = f.read()

lines = s1.splitlines()
for i in range(985, min(len(lines), 1015)):
    print(f"{i+1}: {lines[i]}")
