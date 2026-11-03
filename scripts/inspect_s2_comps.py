with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py", "r", encoding="utf-8") as f:
    code = f.read()

idx_s2 = code.find("components_s2 = [")
idx_s2_end = code.find("net_map_s2 = {", idx_s2)
print(code[idx_s2:idx_s2_end])
