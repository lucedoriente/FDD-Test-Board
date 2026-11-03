import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_sym"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

syms = re.findall(r'\(symbol\s+"([^"]+)"', text)
print("Symbols in FDD-Test-Board.kicad_sym:", syms)
