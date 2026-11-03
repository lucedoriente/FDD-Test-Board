import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

hdr_idx = text.find('\n  (symbol (lib_id')
print(text[:hdr_idx])
