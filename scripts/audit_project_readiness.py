import os, glob, re

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
for f in sorted(glob.glob(os.path.join(PRJ_DIR, "*.kicad_sch"))):
    txt = open(f, encoding='utf-8').read()
    print(f"=== {os.path.basename(f)} ===")
    syms = re.findall(r'\(property "Reference" "([^"]+)"\)\s*\(property "Value" "([^"]+)"\)\s*\(property "Footprint" "([^"]+)"\)', txt)
    if not syms:
        # KiCad 9 format might have effects in between
        syms = re.findall(r'\(property "Reference" "([^"]+)"[^)]*\)\s*\(property "Value" "([^"]+)"[^)]*\)\s*\(property "Footprint" "([^"]+)"', txt)
    for ref, val, fp in syms:
        if any(k in ref for k in ['DISP', 'LCD', 'OLED', 'SW', 'ENC', 'BTN', 'LED', 'BZ', 'J']):
            print(f"  {ref:8s} {val:20s} {fp}")
