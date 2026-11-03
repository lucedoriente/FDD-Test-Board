with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    s1 = f.read()

lines = s1.splitlines()
for i, l in enumerate(lines):
    if '"J1"' in l:
        for j in range(max(0, i-4), min(len(lines), i+18)):
            print(f"{j+1}: {lines[j]}")
        break
