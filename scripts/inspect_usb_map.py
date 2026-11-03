with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py", "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("net_map_s2 = {")
idx_end = code.find("}", idx)
s2_map = code[idx:idx_end+1]
for line in s2_map.splitlines():
    if any(k in line for k in ["USB", "J6", "D1", "R6", "R7"]):
        print(line)
