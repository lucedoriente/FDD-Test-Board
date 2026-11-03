import glob, os, re

ic_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad"
for f in sorted(os.listdir(ic_dir)):
    if f.endswith(".kicad_sch"):
        path = os.path.join(ic_dir, f)
        txt = open(path, encoding="utf-8").read()
        print(f"=== {f} ({len(txt)} bytes) ===")
        # check sheet instances or global labels
        glbls = re.findall(r'\(global_label\s+"([^"]+)"', txt)
        print(f"  Global labels count: {len(glbls)}, unique: {len(set(glbls))}")
        # print first few global labels
        if glbls:
            print(f"  First 5 glbls: {glbls[:5]}")
