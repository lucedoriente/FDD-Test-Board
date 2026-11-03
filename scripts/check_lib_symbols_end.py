import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('  (symbol (lib_id')
print("End of lib_symbols:")
print(text[idx-200:idx])
