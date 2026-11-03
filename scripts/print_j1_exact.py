import os

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
with open(os.path.join(prj_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(property "Reference" "J1"')
s = text.rfind('(symbol ', 0, idx)
e = text.find('\n  )', idx)
print("Symbol J1 block:")
print(text[s:e+5])
