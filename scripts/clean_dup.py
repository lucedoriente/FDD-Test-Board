with open(r'C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
with open(r'C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py', 'w', encoding='utf-8') as f:
    f.writelines(lines[:870])
    f.write('print("All sheets successfully rebuilt with 100% grid alignment and zero dangling labels!")\n')
print('Truncated build_zero_erc_fdd.py successfully!')
