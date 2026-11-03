import os, sys, re, uuid, subprocess

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester"
kicad_dir = os.path.join(PRJ_DIR, "kicad")
scripts_dir = os.path.join(PRJ_DIR, "scripts")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

# Read original build_zero_erc_fdd.py
with open(os.path.join(scripts_dir, "build_zero_erc_fdd.py"), "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update GLOBAL_SIGNALS to include BOOT0 and MCU_NRST
code = code.replace(
    '"BUZZER_PWM", "PROBE_TP1", "PROBE_TP2",',
    '"BUZZER_PWM", "PROBE_TP1", "PROBE_TP2", "BOOT0", "MCU_NRST",'
)

# 2. Add SW5 to components_s2
sw5_def = """    # SW5: DFU BOOT Button
    {"lib": "Switch", "sym": "SW_Push", "ref": "SW5", "val": "SW_BOOT", "fp": "Button_Switch_THT:SW_PUSH_6mm_H5mm", "x": 50.8, "y": 233.68, "unit": 1},
]"""
code = code.replace(
    '    {"lib": "Switch", "sym": "SW_Push", "ref": "SW1", "val": "BTN_RST", "fp": "Button_Switch_THT:SW_PUSH_6mm_H5mm", "x": 50.8, "y": 208.28, "unit": 1},\n]',
    '    {"lib": "Switch", "sym": "SW_Push", "ref": "SW1", "val": "BTN_RST", "fp": "Button_Switch_THT:SW_PUSH_6mm_H5mm", "x": 50.8, "y": 208.28, "unit": 1},\n' + sw5_def
)

# 3. Add SW5 net mapping to net_map_s2
sw5_net = """    ("SW1", "1"): "MCU_NRST", ("SW1", "2"): "GND",
    ("SW5", "1"): "BOOT0", ("SW5", "2"): "+3.3V","""
code = code.replace(
    '    ("SW1", "1"): "MCU_NRST", ("SW1", "2"): "GND",',
    sw5_net
)

# 4. In components_s3, replace J8 (Conn_01x02_Pin) and J9 (Conn_01x02_Pin) with 4-pin J8 and add J15 (14-pin Conn_02x07_Odd_Even)
old_j8_j9 = """    # Front Jacks
    {"lib": "Connector", "sym": "Conn_01x02_Pin", "ref": "J8", "val": "JACK_PROBE_TP1", "fp": "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Horizontal", "x": 274.32, "y": 213.36, "unit": 1},
    {"lib": "Connector", "sym": "Conn_01x02_Pin", "ref": "J9", "val": "JACK_PROBE_TP2", "fp": "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Horizontal", "x": 274.32, "y": 243.84, "unit": 1},
]"""

new_j8_j15 = """    # Scope Probe Header (4-Pin: TP1, GND, TP2, GND)
    {"lib": "Connector_Generic", "sym": "Conn_01x04", "ref": "J8", "val": "J_SCOPE", "fp": "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", "x": 274.32, "y": 213.36, "unit": 1},

    # Panel UI Header (14-Pin IDC: GND, 3V3, ENC, BTN, RST, BOOT0, 5x LEDs)
    {"lib": "Connector_Generic", "sym": "Conn_02x07_Odd_Even", "ref": "J15", "val": "J_PANEL_UI", "fp": "Connector_PinHeader_2.54mm:PinHeader_2x07_P2.54mm_Vertical", "x": 330.2, "y": 101.6, "unit": 1},
]"""

code = code.replace(old_j8_j9, new_j8_j15)

# 5. In net_map_s3, update J8 nets and add J15 nets, remove J9
old_j8_j9_net = """    # Probe Jacks
    ("J8", "1"): "PROBE_TP1", ("J8", "2"): "GND",
    ("J9", "1"): "PROBE_TP2", ("J9", "2"): "GND",
}"""

new_j8_j15_net = """    # Scope Probes (Consolidated 4-Pin)
    ("J8", "1"): "PROBE_TP1", ("J8", "2"): "GND",
    ("J8", "3"): "PROBE_TP2", ("J8", "4"): "GND",

    # Panel UI Header
    ("J15", "1"): "GND",
    ("J15", "2"): "+3.3V",
    ("J15", "3"): "ENC_A",
    ("J15", "4"): "ENC_B",
    ("J15", "5"): "ENC_SW",
    ("J15", "6"): "BTN_RUN",
    ("J15", "7"): "BTN_BACK",
    ("J15", "8"): "MCU_NRST",
    ("J15", "9"): "BOOT0",
    ("J15", "10"): "LED_READY_A",
    ("J15", "11"): "LED_BUSY_A",
    ("J15", "12"): "LED_FAULT_A",
    ("J15", "13"): "LED_INDEX_A",
    ("J15", "14"): "LED_READ_A",
}"""

code = code.replace(old_j8_j9_net, new_j8_j15_net)

# Write updated script
builder_file = os.path.join(scripts_dir, "build_zero_erc_fdd_v2.py")
with open(builder_file, "w", encoding="utf-8") as f:
    f.write(code)

print(f"Written {builder_file}. Now executing...")
res = subprocess.run([r"C:\Program Files\KiCad\9.0\bin\python.exe", builder_file], capture_output=True, text=True)
print("Return code:", res.returncode)
print(res.stdout[-500:] if res.stdout else "No stdout")
if res.stderr:
    print("Stderr:", res.stderr)

# Run ERC verification
erc_cmd = [kicad_cli, "sch", "erc", os.path.join(kicad_dir, "FDD-Test-Board.kicad_sch")]
res_erc = subprocess.run(erc_cmd, capture_output=True, text=True)
print("=== SCHEMATIC ERC RESULT ===")
print(res_erc.stdout.strip())
