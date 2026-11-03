import os, re

ic_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad"
for f in os.listdir(ic_dir):
    if f.endswith(".kicad_sch"):
        p = os.path.join(ic_dir, f)
        with open(p, "r", encoding="utf-8") as file:
            t = file.read()
        m = re.findall(r'\(symbol \(lib_id "([^"]+)"\)', t)
        print(f"{f}: {len(m)} symbols, unique: {set(m)}")
