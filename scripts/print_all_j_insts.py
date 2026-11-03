import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

for ref in ["J1", "J2", "J3", "J4", "J5"]:
    idx = text.find(f'(property "Reference" "{ref}"')
    if idx != -1:
        s = text.rfind('(symbol ', 0, idx)
        e = text.find('(instances', idx)
        inst_e = text.find('\n    )', e)
        print(f"=== {ref} ===")
        print(text[e:inst_e+7])
    else:
        print(f"=== {ref} NOT FOUND ===")
