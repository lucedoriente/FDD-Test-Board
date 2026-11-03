with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_fdd_pcb.py", "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("Mounting")
print(code[idx:idx+500])
