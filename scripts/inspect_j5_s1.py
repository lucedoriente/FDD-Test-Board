with open('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/scripts/build_zero_erc_fdd.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(95, 140):
    print(f"{i+1}: {lines[i].rstrip()}")
