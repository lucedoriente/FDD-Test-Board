import os, sys

scripts_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\scripts"
sys.path.append(scripts_dir)
from generate_clean_erc0_project import extract_symbol_exact, get_symbol_pins

for lib, sym in [("Transistor_BJT", "2N3904"), ("Device", "Crystal_GND24"), ("Device", "Buzzer"), ("Device", "LED"), ("Device", "D_Small")]:
    stxt = extract_symbol_exact(lib, sym)
    pins = get_symbol_pins(stxt)
    print(f"{sym} pins:")
    for p in sorted(pins.keys()):
        print(f"  pin {p}: {pins[p][2]} ({pins[p][3]})")
