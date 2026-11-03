import glob, re

ic_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad"
for sch in glob.glob(ic_dir + r"\*.kicad_sch"):
    txt = open(sch, encoding="utf-8").read()
    if "2N3904" in txt:
        print("2N3904 in:", sch)
    if "74LS06" in txt:
        print("74LS06 in:", sch)
    if "LMV358" in txt:
        print("LMV358 in:", sch)
