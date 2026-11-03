import os, re

sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
p = os.path.join(sym_dir, "74xx.kicad_sym")
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

target = '(symbol "74LS06"'
idx = text.find(target)
print(text[idx:idx+500])
