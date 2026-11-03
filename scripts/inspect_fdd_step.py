import glob, re

for sch in ['01_Power_Supply.kicad_sch', '02_MCU_Core.kicad_sch', '03_UI_Controls.kicad_sch', '04_FDD_Interfaces.kicad_sch']:
    txt = open(f"C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/{sch}", encoding="utf-8").read()
    c = len(re.findall(r'\(global_label\s+"FDD_STEP"', txt))
    print(f"{sch}: {c} FDD_STEP")
