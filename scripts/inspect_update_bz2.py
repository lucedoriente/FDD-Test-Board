with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\update_bz_fdd.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(20, min(120, len(lines))):
    print(lines[i], end="")
