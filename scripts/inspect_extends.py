import os, re

sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"

for lib, sym in [("Transistor_BJT", "2N3904"), ("Amplifier_Operational", "LMV358"), ("74xx", "74LS06")]:
    p = os.path.join(sym_dir, f"{lib}.kicad_sym")
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'\(symbol "' + sym + r'"\s*\(extends "([^"]+)"\)', content)
    if m:
        print(f"{lib}:{sym} extends {m.group(1)}")
    else:
        print(f"{lib}:{sym} does not extend directly")
