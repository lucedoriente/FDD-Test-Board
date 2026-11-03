with open(r'C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('for pnum, (pname, ptype, px, py, pang) in pin_dict.items():')
print(text[idx:idx+1500])
