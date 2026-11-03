import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    t = f.read()

idx1 = t.find('(symbol "power:GND"')
print("Is power:GND in IC sheet 1 lib_symbols?", idx1 != -1)
if idx1 != -1:
    print(t[idx1:idx1+400])
else:
    # let's see what is in IC lib_symbols
    idx_ls = t.find('(lib_symbols')
    print("IC lib_symbols first 500 chars:")
    print(t[idx_ls:idx_ls+500])
