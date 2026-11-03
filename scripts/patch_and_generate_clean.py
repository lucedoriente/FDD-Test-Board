import os, sys, re, subprocess

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
scripts_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts"
local_sym_path = os.path.join(prj_dir, "FDD-Test-Board.kicad_sym")
cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

# 1. Update FDD-Test-Board.kicad_sym with clean flattened symbols
from test_clean_flatten import get_flattened

syms_to_flatten = [
    ("Transistor_BJT", "2N3904"),
    ("Amplifier_Operational", "LMV358"),
    ("74xx", "74LS06"),
    ("Transistor_FET", "AO3401A"),
]

local_sym_bodies = []
for lib, sname in syms_to_flatten:
    flat = get_flattened(lib, sname)
    flat_no_lib = flat.replace(f'(symbol "{lib}:{sname}"', f'(symbol "{sname}"', 1)
    local_sym_bodies.append(flat_no_lib)

local_sym_file_content = f"""(kicad_symbol_lib
  (version 20231120)
  (generator "kicad_symbol_editor")
  {chr(10).join(local_sym_bodies)}
)
"""

with open(local_sym_path, "w", encoding="utf-8") as f:
    f.write(local_sym_file_content)

print("1. FDD-Test-Board.kicad_sym updated with 4 flattened symbols.")

# 2. Modify build_zero_erc_fdd.py
with open(os.path.join(scripts_dir, "build_zero_erc_fdd.py"), "r", encoding="utf-8") as f:
    code = f.read()

# Make sure extract_raw_sym_text and get_symbol_pins_for_unit support FDD-Test-Board
new_raw_fn = """def extract_raw_sym_text(lib_name, sym_name):
    if lib_name == "FDD-Test-Board":
        p = os.path.join(kicad_dir, "FDD-Test-Board.kicad_sym")
    else:
        p = os.path.join(sym_dir, f"{lib_name}.kicad_sym")
    if not os.path.exists(p):
        return ""
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    start_tag = f'(symbol "{sym_name}"'
    idx = content.find(start_tag)
    if idx == -1: return ""
    cnt, end = 0, 0
    for i in range(idx, len(content)):
        if content[i] == '(': cnt += 1
        elif content[i] == ')':
            cnt -= 1
            if cnt == 0:
                end = i + 1; break
    return content[idx:end]
"""

# Replace extract_raw_sym_text in code
code = re.sub(r'def extract_raw_sym_text\(lib_name, sym_name\):.*?(?=def extract_symbol_exact_with_parent)', new_raw_fn + "\n", code, flags=re.DOTALL)

# Ensure get_symbol_pins_for_unit supports FDD-Test-Board
new_pins_top = """def get_symbol_pins_for_unit(lib_name, sym_name, unit=1):
    if lib_name == "FDD-Test-Board":
        p = os.path.join(kicad_dir, "FDD-Test-Board.kicad_sym")
    else:
        p = os.path.join(sym_dir, f"{lib_name}.kicad_sym")
"""
code = re.sub(r'def get_symbol_pins_for_unit\(lib_name, sym_name, unit=1\):\s*p = os\.path\.join\(sym_dir, f"\{lib_name\}\.kicad_sym"\)', new_pins_top, code)

# Switch the 4 symbols to use "FDD-Test-Board"
code = code.replace('"lib": "Transistor_BJT", "sym": "2N3904"', '"lib": "FDD-Test-Board", "sym": "2N3904"')
code = code.replace('"lib": "Amplifier_Operational", "sym": "LMV358"', '"lib": "FDD-Test-Board", "sym": "LMV358"')
code = code.replace('"lib": "74xx", "sym": "74LS06"', '"lib": "FDD-Test-Board", "sym": "74LS06"')
code = code.replace('"lib": "Transistor_FET", "sym": "AO3401A"', '"lib": "FDD-Test-Board", "sym": "AO3401A"')

# Fix Sheet 2 overlaps:
# Move D1 from x: 88.9 to x: 101.6
code = code.replace('"ref": "D1", "val": "USBLC6-2SC6", "fp": "Package_TO_SOT_SMD:SOT-23-6", "x": 88.9', '"ref": "D1", "val": "USBLC6-2SC6", "fp": "Package_TO_SOT_SMD:SOT-23-6", "x": 101.6')
# Move R5 from x: 25.4 to x: 38.1
code = code.replace('"ref": "R5", "val": "5.1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 25.4', '"ref": "R5", "val": "5.1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 38.1')
# Move D3, C18, R12
code = code.replace('"ref": "D3", "val": "1N4148", "fp": "Diode_SMD:D_SOD-123", "x": 365.76', '"ref": "D3", "val": "1N4148", "fp": "Diode_SMD:D_SOD-123", "x": 381.0')
code = code.replace('"ref": "C18", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 386.08, "y": 111.76', '"ref": "C18", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 406.4, "y": 111.76')
code = code.replace('"ref": "R12", "val": "100k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 386.08, "y": 132.08', '"ref": "R12", "val": "100k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 406.4, "y": 132.08')

# Fix Sheet 4 overlaps:
# Move U4, U8, U9 unit 7 to y: 127.0
code = code.replace('"ref": "U4", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 76.2, "y": 111.76, "unit": 7', '"ref": "U4", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 76.2, "y": 127.0, "unit": 7')
code = code.replace('"ref": "U8", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 147.32, "y": 111.76, "unit": 7', '"ref": "U8", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 147.32, "y": 127.0, "unit": 7')
code = code.replace('"ref": "U9", "val": "74HC14_HEX_SCHMITT", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 218.44, "y": 111.76, "unit": 7', '"ref": "U9", "val": "74HC14_HEX_SCHMITT", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 218.44, "y": 127.0, "unit": 7')

# Add PWR_FLAG support in build_sheet for Sheet 1
# Check if PWR_FLAG is in lib_symbols
pwr_flag_check = """
    if out_filename == "01_Power_Supply.kicad_sch":
        pwr_flg = extract_symbol_exact_with_parent("power", "PWR_FLAG")
        embedded_syms_dict["power:PWR_FLAG"] = pwr_flg
"""
if "01_Power_Supply.kicad_sch" not in code or "embedded_syms_dict[\"power:PWR_FLAG\"]" not in code:
    code = code.replace('embedded_syms_dict["power:+3.3V"] = pwr_3v3', 'embedded_syms_dict["power:+3.3V"] = pwr_3v3\n' + pwr_flag_check)

# Add PWR_FLAG instances in Sheet 1
pwr_flags_insts = """
    if out_filename == "01_Power_Supply.kicad_sch":
        # Add PWR_FLAG on GND, +24V_RAW, +12V_REG, +5V_REG
        pwr_flags_to_add = [
            ("GND", 60.96, 48.26),
            ("+24V_RAW", 45.72, 45.72),
            ("+12V_REG", 114.3, 127.0),
            ("+5V_REG", 228.6, 127.0),
        ]
        for pf_net, pfx, pfy in pwr_flags_to_add:
            global pwr_counter
            pwr_counter += 1
            pf_ref = f"#FLG{pwr_counter:04d}"
            pf_blk = make_instances_block(pf_ref, sheet_uuid, doc_uuid, unit=1)
            inst = f'''  (symbol (lib_id "power:PWR_FLAG") (at {pfx:.2f} {pfy:.2f} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{u()}")
    (property "Reference" "{pf_ref}" (at {pfx:.2f} {pfy - 1.91:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "PWR_FLAG" (at {pfx:.2f} {pfy - 3.81:.2f} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at {pfx:.2f} {pfy:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "{u()}"))
{pf_blk}
  )'''
            instances_str.append(inst)
"""
if "pwr_flags_to_add" not in code:
    code = code.replace('instances_str.append(inst)\n\n        handled_coords = set()', 'instances_str.append(inst)\n\n        handled_coords = set()')
    code = code.replace('lib_symbols_txt = "  (lib_symbols\\n"', pwr_flags_insts + '\n    lib_symbols_txt = "  (lib_symbols\\n"')

with open(os.path.join(scripts_dir, "build_zero_erc_fdd.py"), "w", encoding="utf-8") as f:
    f.write(code)

print("2. build_zero_erc_fdd.py updated with all fixes.")
