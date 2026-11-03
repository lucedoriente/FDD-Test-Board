import os, re

def check_instances(sch_path):
    with open(sch_path, 'r', encoding='utf-8') as f:
        txt = f.read()
    # find first non-power symbol
    syms = re.findall(r'\(symbol \(lib_id [^\)]+\).*?\(instances.*?\n    \)', txt, re.DOTALL)
    for s in syms:
        ref = re.search(r'\(property "Reference" "([^"]+)"', s)
        if ref and not ref.group(1).startswith('#'):
            inst = re.search(r'\(instances.*?\n    \)', s, re.DOTALL)
            return ref.group(1), inst.group(0) if inst else "NO INSTANCES"
    return "NONE", "NONE"

print("IC sheet 1:")
r, i = check_instances(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\01_Power_Supply.kicad_sch")
print(r, i)

print("\nFDD sheet 1:")
r, i = check_instances(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch")
print(r, i)

print("\nFDD sheet 2:")
r, i = check_instances(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch")
print(r, i)
