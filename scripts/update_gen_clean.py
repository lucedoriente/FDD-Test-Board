import os, sys, re, subprocess
from test_flatten_engine import get_flattened_symbol
import build_zero_erc_fdd as bz

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

# In build_full_4_sheets_clean.py, let's update build_sheet to use exact coordinates:
with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\generate_all_4_sheets_clean.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace the coordinate calculation:
old_calc = """            pin_x = snap(cx + px)
            pin_y = snap(cy - py)
            stub_len = 5.08
            if pang == 0:
                end_x, end_y = snap(pin_x - stub_len), pin_y
                lbl_ang = 180
                lbl_just = "(justify right)"
            elif pang == 180:
                end_x, end_y = snap(pin_x + stub_len), pin_y
                lbl_ang = 0
                lbl_just = "(justify left)"
            elif pang == 270:
                end_x, end_y = pin_x, snap(pin_y + stub_len)
                lbl_ang = 270
                lbl_just = "(justify right)"
            elif pang == 90:
                end_x, end_y = pin_x, snap(pin_y - stub_len)
                lbl_ang = 90
                lbl_just = "(justify left)"
            else:
                end_x, end_y = snap(pin_x + stub_len), pin_y
                lbl_ang = 0
                lbl_just = "(justify left)" """

# Note that in get_symbol_pins_for_unit:
# py was positive UP, so cy - py was correct, BUT stub direction for pang was:
# pang == 270 is DOWN, so pin_y + stub_len is DOWN
# pang == 90 is UP, so pin_y - stub_len is UP
# And wire must start at round(cx + px, 4), round(cy - py, 4)!
new_calc = """            pin_x = round(cx + px, 4)
            pin_y = round(cy - py, 4)
            stub_len = 5.08
            if pang == 0:
                end_x, end_y = round(pin_x - stub_len, 4), pin_y
                lbl_ang = 180
                lbl_just = "(justify right)"
            elif pang == 180:
                end_x, end_y = round(pin_x + stub_len, 4), pin_y
                lbl_ang = 0
                lbl_just = "(justify left)"
            elif pang == 270:
                end_x, end_y = pin_x, round(pin_y + stub_len, 4)
                lbl_ang = 270
                lbl_just = "(justify right)"
            elif pang == 90:
                end_x, end_y = pin_x, round(pin_y - stub_len, 4)
                lbl_ang = 90
                lbl_just = "(justify left)"
            else:
                end_x, end_y = round(pin_x + stub_len, 4), pin_y
                lbl_ang = 0
                lbl_just = "(justify left)" """

code = code.replace(old_calc, new_calc)

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\generate_all_4_sheets_clean.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated generate_all_4_sheets_clean.py!")
