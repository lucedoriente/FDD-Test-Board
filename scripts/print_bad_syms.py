import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

idx_ao = text.find('(symbol "Transistor_FET:AO3401A"')
idx_2n = text.find('(symbol "Transistor_BJT:2N3904"')

print("AO3401A definition:")
print(text[idx_ao:idx_ao+1500])
print("\n" + "="*40 + "\n")
print("2N3904 definition:")
print(text[idx_2n:idx_2n+1500])
