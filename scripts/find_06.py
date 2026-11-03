import os, re

sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
p = os.path.join(sym_dir, "74xx.kicad_sym")
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

matches = re.findall(r'\(symbol "([^"]*06[^"]*)"', text)
print("06 symbols in 74xx:", matches)
