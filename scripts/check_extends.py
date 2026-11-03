import re

s1_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch"
txt = open(s1_path, encoding="utf-8").read()

extends = re.findall(r'\(extends\s+"[^"]+"\)', txt)
print(f"Extends in S1: {extends}")

for sch in ['02_MCU_Core.kicad_sch', '03_UI_Controls.kicad_sch', '04_FDD_Interfaces.kicad_sch']:
    t = open(f"C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/{sch}", encoding="utf-8").read()
    ext = re.findall(r'\(extends\s+"[^"]+"\)', t)
    print(f"Extends in {sch}: {ext}")
