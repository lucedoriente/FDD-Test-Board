with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_fdd_pcb.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(50, min(180, len(lines))):
    print(lines[i], end="")
