import os, sys

scripts_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\scripts"
sys.path.append(scripts_dir)
from generate_clean_erc0_project import extract_symbol_exact, get_symbol_pins

stxt = extract_symbol_exact("MCU_ST_STM32F4", "STM32F407VETx")
pins = get_symbol_pins(stxt)

for num in sorted(pins.keys(), key=lambda x: int(x) if x.isdigit() else 999):
    name, ptype, px, py, ang = pins[num][2], pins[num][3], pins[num][0], pins[num][1], pins[num][4]
    if "V" in name or "BOOT" in name or "NRST" in name or "OSC" in name:
        print(f"Pin {num:3s}: {name:15s} ({ptype:12s}) at ({px:6.2f}, {py:6.2f}, {ang:3d} deg)")
