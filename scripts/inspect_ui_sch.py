import re

txt = open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\03_UI_Controls.kicad_sch", encoding='utf-8').read()
for m in re.finditer(r'\(symbol \(lib_id "([^"]+)"\) \(at ([^)]+)\) \(unit (\d+)\)', txt):
    # find reference following this symbol
    start = m.start()
    snippet = txt[start:start+400]
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', snippet)
    val_m = re.search(r'\(property "Value" "([^"]+)"', snippet)
    fp_m = re.search(r'\(property "Footprint" "([^"]+)"', snippet)
    ref = ref_m.group(1) if ref_m else '?'
    val = val_m.group(1) if val_m else '?'
    fp = fp_m.group(1) if fp_m else '?'
    print(f"{ref:8s}: {val:20s} | LibID={m.group(1)} | Pos=({m.group(2)}) | FP={fp}")
