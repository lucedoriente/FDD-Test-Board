with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(0, 70):
    print(f"{i+1}: {lines[i]}", end="")
