import glob, re

for sch in sorted(glob.glob(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\0*.kicad_sch")):
    txt = open(sch, encoding="utf-8").read()
    fname = sch.split("\\")[-1]
    matches = re.findall(r'\(global_label\s+([^\s\)]+)', txt)
    drv_12 = [m for m in matches if "12V" in m]
    if drv_12:
        print(f"{fname}: {drv_12}")
