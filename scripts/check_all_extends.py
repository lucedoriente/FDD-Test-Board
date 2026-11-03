import os, re

kicad_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
for f in ["01_Power_Supply.kicad_sch", "02_MCU_Core.kicad_sch", "03_UI_Controls.kicad_sch", "04_FDD_Interfaces.kicad_sch"]:
    p = os.path.join(kicad_dir, f)
    with open(p, "r", encoding="utf-8") as file:
        t = file.read()
    exts = re.findall(r'\(extends "([^"]+)"\)', t)
    print(f"File {f}: {len(exts)} extends found -> {exts}")
