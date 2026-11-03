import os, re
from test_parse_ls import parse_lib_symbols

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
for f in ["03_UI_Controls.kicad_sch", "04_FDD_Interfaces.kicad_sch"]:
    with open(os.path.join(prj_dir, f), "r", encoding="utf-8") as file:
        text = file.read()
    ls_start = text.find('(lib_symbols')
    cnt = 0
    for i, c in enumerate(text[ls_start:]):
        if c == '(': cnt += 1
        elif c == ')':
            cnt -= 1
            if cnt == 0:
                ls_end = ls_start + i + 1
                break
    ls = text[ls_start:ls_end]
    parsed = parse_lib_symbols(ls)
    print(f"=== {f} ({len(parsed)} symbols) ===")
    for k, v in parsed.items():
        has_ext = re.search(r'\(extends "([^"]+)"\)', v)
        ext_val = has_ext.group(1) if has_ext else "NONE"
        if ext_val != "NONE":
            print(f"  {k} -> extends: {ext_val}")
