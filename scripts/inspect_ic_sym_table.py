import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\IC-Test-Board.kicad_sym"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

syms = re.findall(r'\(symbol "([^"]+)"', text)
print("Symbols in IC-Test-Board.kicad_sym:")
for s in syms:
    print(" ", s)
