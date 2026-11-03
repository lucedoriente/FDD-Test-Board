import os, re

ic_kicad = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad"
for f in os.listdir(ic_kicad):
    if f.endswith(".kicad_sch"):
        p = os.path.join(ic_kicad, f)
        with open(p, "r", encoding="utf-8") as s:
            txt = s.read()
        for target in ["2N3904", "LMV358", "74LS06", "74HC14"]:
            if target in txt:
                # check if it is in lib_symbols
                ls_idx = txt.find("(lib_symbols")
                ls_end = txt.find("\n  )\n", ls_idx)
                in_ls = target in txt[ls_idx:ls_end]
                print(f"{f}: has {target}, in lib_symbols? {in_ls}")
