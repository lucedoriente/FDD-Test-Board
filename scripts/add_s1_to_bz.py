with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py", "r", encoding="utf-8") as f:
    code = f.read()

s1_def = """# ==============================================================================
# SHEET 1 COMPONENTS & NETS (Power Supply Subsystem)
# ==============================================================================
components_s1 = [
    {"lib": "Connector", "sym": "Conn_01x02_Pin", "ref": "J1", "val": "J_IN_24V",
     "fp": "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal", "x": 50.8, "y": 45.72, "unit": 1},
    {"lib": "Connector", "sym": "Conn_01x04_Pin", "ref": "J2", "val": "J_PWR_525",
     "fp": "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal", "x": 127.0, "y": 45.72, "unit": 1},
    {"lib": "Connector", "sym": "Conn_01x04_Pin", "ref": "J3", "val": "J_PWR_350",
     "fp": "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Horizontal", "x": 203.2, "y": 45.72, "unit": 1},
    {"lib": "Connector", "sym": "Conn_01x04_Pin", "ref": "J4", "val": "J_PWR_800",
     "fp": "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal", "x": 279.4, "y": 45.72, "unit": 1},
    {"lib": "Connector_Generic", "sym": "Conn_01x04", "ref": "J5", "val": "J_DISP_7IN",
     "fp": "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", "x": 355.6, "y": 45.72, "unit": 1},
]

net_map_s1 = {
    ("J1", "1"): "+24V_RAW", ("J1", "2"): "GND",
    ("J2", "1"): "+12V_DRV", ("J2", "2"): "GND", ("J2", "3"): "GND", ("J2", "4"): "+5V_DRV",
    ("J3", "1"): "+5V_DRV", ("J3", "2"): "GND", ("J3", "3"): "GND", ("J3", "4"): "+12V_DRV",
    ("J4", "1"): "+24V_DRV", ("J4", "2"): "+5V_DRV", ("J4", "3"): "GND", ("J4", "4"): "-12V_DRV",
    ("J5", "1"): "+5V_REG", ("J5", "2"): "GND", ("J5", "3"): "USART1_TX", ("J5", "4"): "USART1_RX",
}
"""

s1_call = """print("Generating Sheet 1: Power Supply...")
build_sheet(
    "Power Supply & E-Fuses Subsystem",
    "Mean Well 24V Input, Buck Regulators, E-Fuses & Power Connectors",
    components_s1,
    net_map_s1,
    "01_Power_Supply.kicad_sch",
    0
)
"""

if "components_s1 = [" not in code:
    idx = code.find("# SHEET 2 COMPONENTS & NETS")
    code = code[:idx] + s1_def + "\n" + code[idx:]

if 'build_sheet(\n    "Power Supply' not in code:
    idx2 = code.find('print("Generating Sheet 2: MCU Core...")')
    code = code[:idx2] + s1_call + "\n" + code[idx2:]

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Added Sheet 1 to build_zero_erc_fdd.py!")
