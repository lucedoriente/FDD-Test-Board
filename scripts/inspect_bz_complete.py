with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_complete.py", "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find('("J4", "1"): "+')
print(code[idx:idx+2500])
