import os, sys, re, subprocess

scripts_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts"

with open(os.path.join(scripts_dir, "build_zero_erc_fdd.py"), "r", encoding="utf-8") as f:
    code = f.read()

# Separate U4, U8, U9 unit 7 on different X columns
code = code.replace('"ref": "U4", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 381.0, "y": 50.8, "unit": 7', '"ref": "U4", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 360.68, "y": 81.28, "unit": 7')
code = code.replace('"ref": "U8", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 381.0, "y": 81.28, "unit": 7', '"ref": "U8", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 386.08, "y": 81.28, "unit": 7')
code = code.replace('"ref": "U9", "val": "74HC14_HEX_SCHMITT", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 381.0, "y": 111.76, "unit": 7', '"ref": "U9", "val": "74HC14_HEX_SCHMITT", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 411.48, "y": 81.28, "unit": 7')

with open(os.path.join(scripts_dir, "build_zero_erc_fdd.py"), "w", encoding="utf-8") as f:
    f.write(code)

print("Separated U4, U8, U9 unit 7 horizontally!")
