with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py", "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("net_map_s4 = {")
idx_end = code.find("}", idx)
s4_map = code[idx:idx_end+1]
for line in s4_map.splitlines():
    if "U4" in line and ("14" in line or "7" in line):
        print(line)
