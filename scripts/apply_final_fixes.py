import os, sys, re, subprocess

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
scripts_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts"
cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

with open(os.path.join(scripts_dir, "build_zero_erc_fdd.py"), "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update PWR_FLAG coordinates in Sheet 1:
code = code.replace('("+24V_RAW", 45.72, 45.72)', '("+24V_RAW", 60.96, 45.72)')
code = code.replace('("+12V_REG", 114.3, 127.0)', '("+12V_REG", 114.30, 118.11)')
code = code.replace('("+5V_REG", 228.6, 127.0)', '("+5V_REG", 228.60, 118.11)')

# 2. Update Sheet 2: Place R7 side-by-side with R6
code = code.replace('"ref": "R7", "val": "22R", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 121.92, "y": 104.14', '"ref": "R7", "val": "22R", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 139.7, "y": 88.9')

# 3. Update Sheet 4: Place U4, U8, U9 unit 7 safely at x: 381.0
code = code.replace('"ref": "U4", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 76.2, "y": 127.0, "unit": 7', '"ref": "U4", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 381.0, "y": 50.8, "unit": 7')
code = code.replace('"ref": "U8", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 147.32, "y": 127.0, "unit": 7', '"ref": "U8", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 381.0, "y": 81.28, "unit": 7')
code = code.replace('"ref": "U9", "val": "74HC14_HEX_SCHMITT", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 218.44, "y": 127.0, "unit": 7', '"ref": "U9", "val": "74HC14_HEX_SCHMITT", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 381.0, "y": 111.76, "unit": 7')

with open(os.path.join(scripts_dir, "build_zero_erc_fdd.py"), "w", encoding="utf-8") as f:
    f.write(code)

print("Updated build_zero_erc_fdd.py with clean positions!")
