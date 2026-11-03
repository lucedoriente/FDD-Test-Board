with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_fdd_pcb.py", "r", encoding="utf-8") as f:
    code = f.read()

# Fix C29 vs C1:
code = code.replace('pos["C29"] = (91.0, 50.0, 0)', 'pos["C29"] = (91.0, 44.0, 0)')

# Fix SW2 vs R13-R15 / C19-C21:
code = code.replace('pos["R13"] = (52.0, 112.0, 0)', 'pos["R13"] = (54.0, 112.0, 0)')
code = code.replace('pos["R14"] = (52.0, 118.0, 0)', 'pos["R14"] = (54.0, 118.0, 0)')
code = code.replace('pos["R15"] = (52.0, 124.0, 0)', 'pos["R15"] = (54.0, 124.0, 0)')
code = code.replace('pos["C19"] = (58.0, 112.0, 0)', 'pos["C19"] = (60.0, 112.0, 0)')
code = code.replace('pos["C20"] = (58.0, 118.0, 0)', 'pos["C20"] = (60.0, 118.0, 0)')
code = code.replace('pos["C21"] = (58.0, 124.0, 0)', 'pos["C21"] = (60.0, 124.0, 0)')

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_fdd_pcb.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Applied final 3 clearance adjustments!")
