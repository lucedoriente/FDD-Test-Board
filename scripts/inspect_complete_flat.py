with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_complete.py", "r", encoding="utf-8") as f:
    c = f.read()

idx = c.find("def get_flattened_symbol")
if idx != -1:
    print(c[idx:idx+1500])
else:
    print("Not found")
