import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

print("Is Conn_01x02_Pin in lib_symbols?", "Conn_01x02_Pin" in text[:text.find('(symbol (lib_id')])
print("Is Conn_01x02 in lib_symbols?", "Conn_01x02" in text[:text.find('(symbol (lib_id')])
print("Lib symbols defined:")
for line in text[:text.find('(symbol (lib_id')].splitlines():
    if '(symbol "' in line:
        print(" ", line.strip())
