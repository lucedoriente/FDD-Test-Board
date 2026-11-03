with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py", "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("GLOBAL_SIGNALS = ")
idx_end = code.find("]", idx)
print(code[idx:idx_end+1])
