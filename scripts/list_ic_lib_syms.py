import os, re

ic_s1 = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\01_Power_Supply.kicad_sch"
with open(ic_s1, "r", encoding="utf-8") as f:
    text = f.read()

# Let's find all symbols in lib_symbols
ls_idx = text.find('(lib_symbols')
ls_end = text.find('\n  (symbol (lib_id')
ls_text = text[ls_idx:ls_end]

sym_names = re.findall(r'\(symbol "([^"]+)"', ls_text)
print("Symbols in IC sheet 1 lib_symbols:")
for name in sym_names:
    print(" ", name)
