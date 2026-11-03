import re

txt = open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\03_UI_Controls.kicad_sch", encoding='utf-8').read()
idx = txt.find('(lib_symbols')
end_idx = txt.find('(wire', idx)
snippet = txt[idx:end_idx]
for m in re.finditer(r'\(symbol "([^"]+)"', snippet):
    print(m.group(1))
