import os, re
sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
with open(os.path.join(sym_dir, "Regulator_Switching.kicad_sym"), "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(symbol "TPS54302"')
print("Found TPS54302:", idx != -1)
if idx != -1:
    print(text[idx:idx+1500])
