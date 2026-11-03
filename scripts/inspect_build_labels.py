with open('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/scripts/build_zero_erc_fdd.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'GLOBAL_SIGNALS' in line:
        for j in range(max(0, i-5), min(len(lines), i+30)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
