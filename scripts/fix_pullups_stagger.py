import os, sys, re

scripts_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts"

with open(os.path.join(scripts_dir, "build_zero_erc_fdd.py"), "r", encoding="utf-8") as f:
    code = f.read()

# Stagger pull-up resistors R24-R29 in Sheet 4 so they don't overlap vertically
old_pullups = """    # Pull-up Resistors (1k to +5V_REG on input signals)
    {"lib": "Device", "sym": "R", "ref": "R24", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 335.28, "y": 50.8, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R25", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 335.28, "y": 66.04, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R26", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 335.28, "y": 81.28, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R27", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 335.28, "y": 96.52, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R28", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 335.28, "y": 111.76, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R29", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 335.28, "y": 127.0, "unit": 1},"""

new_pullups = """    # Pull-up Resistors (1k to +5V_REG on input signals) - Staggered X to prevent vertical stub collision
    {"lib": "Device", "sym": "R", "ref": "R24", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 325.12, "y": 50.8, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R25", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 340.36, "y": 50.8, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R26", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 325.12, "y": 76.2, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R27", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 340.36, "y": 76.2, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R28", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 325.12, "y": 101.6, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R29", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 340.36, "y": 101.6, "unit": 1},"""

code = code.replace(old_pullups, new_pullups)

with open(os.path.join(scripts_dir, "build_zero_erc_fdd.py"), "w", encoding="utf-8") as f:
    f.write(code)

print("Staggered R24-R29 in Sheet 4!")
