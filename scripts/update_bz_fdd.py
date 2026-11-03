with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py", "r", encoding="utf-8") as f:
    orig = f.read()

# Replace components_s1 and net_map_s1
idx_s1 = orig.find("# SHEET 1 COMPONENTS & NETS")
idx_s2 = orig.find("# SHEET 2 COMPONENTS & NETS")

s1_full_code = """# SHEET 1 COMPONENTS & NETS (Power Supply & E-Fuses Subsystem)
# ==============================================================================
components_s1 = [
    # Power Input J1 (Phoenix 2-pin 24V Mean Well)
    {"lib": "Connector", "sym": "Conn_01x02_Pin", "ref": "J1", "val": "J_IN_24V",
     "fp": "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal", "x": 50.8, "y": 45.72, "unit": 1},

    # Drive Power Headers:
    {"lib": "Connector", "sym": "Conn_01x04_Pin", "ref": "J2", "val": "J_PWR_525",
     "fp": "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal", "x": 127.0, "y": 45.72, "unit": 1},
    {"lib": "Connector", "sym": "Conn_01x04_Pin", "ref": "J3", "val": "J_PWR_350",
     "fp": "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Horizontal", "x": 203.2, "y": 45.72, "unit": 1},
    {"lib": "Connector", "sym": "Conn_01x04_Pin", "ref": "J4", "val": "J_PWR_800",
     "fp": "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal", "x": 279.4, "y": 45.72, "unit": 1},
    {"lib": "Connector_Generic", "sym": "Conn_01x04", "ref": "J5", "val": "J_DISP_7IN",
     "fp": "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", "x": 355.6, "y": 45.72, "unit": 1},

    # U1: TPS54302 Buck Converter 12V
    {"lib": "Regulator_Switching", "sym": "TPS54302", "ref": "U1", "val": "TPS54302",
     "fp": "Package_TO_SOT_SMD:SOT-23-6", "x": 50.8, "y": 127.0, "unit": 1},
    {"lib": "Device", "sym": "L", "ref": "L1", "val": "10uH",
     "fp": "Inductor_SMD:L_7.3x7.3_H4.5", "x": 88.9, "y": 127.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C24", "val": "0.1uF",
     "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 50.8, "y": 165.1, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C25", "val": "10uF",
     "fp": "Capacitor_SMD:C_1210_3225Metric", "x": 25.4, "y": 127.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C26", "val": "22uF",
     "fp": "Capacitor_SMD:C_1206_3216Metric", "x": 114.3, "y": 127.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R30", "val": "100k",
     "fp": "Resistor_SMD:R_0805_2012Metric", "x": 88.9, "y": 165.1, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R31", "val": "6.04k",
     "fp": "Resistor_SMD:R_0805_2012Metric", "x": 114.3, "y": 165.1, "unit": 1},

    # U2: TPS54302 Buck Converter 5V
    {"lib": "Regulator_Switching", "sym": "TPS54302", "ref": "U2", "val": "TPS54302",
     "fp": "Package_TO_SOT_SMD:SOT-23-6", "x": 165.1, "y": 127.0, "unit": 1},
    {"lib": "Device", "sym": "L", "ref": "L2", "val": "4.7uH",
     "fp": "Inductor_SMD:L_7.3x7.3_H4.5", "x": 203.2, "y": 127.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C27", "val": "0.1uF",
     "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 165.1, "y": 165.1, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C28", "val": "10uF",
     "fp": "Capacitor_SMD:C_1210_3225Metric", "x": 140.0, "y": 127.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C29", "val": "47uF",
     "fp": "Capacitor_SMD:C_1206_3216Metric", "x": 228.6, "y": 127.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R32", "val": "51k",
     "fp": "Resistor_SMD:R_0805_2012Metric", "x": 203.2, "y": 165.1, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R33", "val": "7.15k",
     "fp": "Resistor_SMD:R_0805_2012Metric", "x": 228.6, "y": 165.1, "unit": 1},

    # E-Fuses P-MOSFETs
    {"lib": "Transistor_FET", "sym": "AO3401A", "ref": "Q2", "val": "AO3401A",
     "fp": "Package_TO_SOT_SMD:SOT-23", "x": 279.4, "y": 127.0, "unit": 1},
    {"lib": "Transistor_FET", "sym": "AO3401A", "ref": "Q3", "val": "AO3401A",
     "fp": "Package_TO_SOT_SMD:SOT-23", "x": 330.2, "y": 127.0, "unit": 1},
    {"lib": "Transistor_FET", "sym": "AO3401A", "ref": "Q4", "val": "AO3401A",
     "fp": "Package_TO_SOT_SMD:SOT-23", "x": 381.0, "y": 127.0, "unit": 1},

    # Current Sense Amplifiers INA180
    {"lib": "Amplifier_Current", "sym": "INA180A1", "ref": "U3", "val": "INA180A1",
     "fp": "Package_TO_SOT_SMD:SOT-23-5", "x": 50.8, "y": 215.9, "unit": 1},
    {"lib": "Amplifier_Current", "sym": "INA180A1", "ref": "U11", "val": "INA180A1",
     "fp": "Package_TO_SOT_SMD:SOT-23-5", "x": 127.0, "y": 215.9, "unit": 1},
    {"lib": "Amplifier_Current", "sym": "INA180A1", "ref": "U12", "val": "INA180A1",
     "fp": "Package_TO_SOT_SMD:SOT-23-5", "x": 203.2, "y": 215.9, "unit": 1},
]

net_map_s1 = {
    # J1: 24V Input
    ("J1", "1"): "+24V_RAW", ("J1", "2"): "GND",

    # J2: 5.25" Power (+12V, GND, GND, +5V)
    ("J2", "1"): "+12V_DRV", ("J2", "2"): "GND", ("J2", "3"): "GND", ("J2", "4"): "+5V_DRV",

    # J3: 3.5" Power (+5V, GND, GND, +12V)
    ("J3", "1"): "+5V_DRV", ("J3", "2"): "GND", ("J3", "3"): "GND", ("J3", "4"): "+12V_DRV",

    # J4: 8" Power (+24V, +5V, GND, -12V)
    ("J4", "1"): "+24V_DRV", ("J4", "2"): "+5V_DRV", ("J4", "3"): "GND", ("J4", "4"): "-12V_DRV",

    # J5: 7" Sunton Display Header (+5V_REG, GND, TX, RX)
    ("J5", "1"): "+5V_REG", ("J5", "2"): "GND", ("J5", "3"): "USART1_TX", ("J5", "4"): "USART1_RX",

    # U1: TPS54302 (12V)
    ("U1", "1"): "GND", ("U1", "2"): "SW_12V", ("U1", "3"): "+24V_RAW",
    ("U1", "4"): "FB_12V", ("U1", "5"): "+24V_RAW", ("U1", "6"): "BOOT_12V",
    ("L1", "1"): "SW_12V", ("L1", "2"): "+12V_REG",
    ("C24", "1"): "BOOT_12V", ("C24", "2"): "SW_12V",
    ("C25", "1"): "+24V_RAW", ("C25", "2"): "GND",
    ("C26", "1"): "+12V_REG", ("C26", "2"): "GND",
    ("R30", "1"): "+12V_REG", ("R30", "2"): "FB_12V",
    ("R31", "1"): "FB_12V", ("R31", "2"): "GND",

    # U2: TPS54302 (5V)
    ("U2", "1"): "GND", ("U2", "2"): "SW_5V", ("U2", "3"): "+24V_RAW",
    ("U2", "4"): "FB_5V", ("U2", "5"): "+24V_RAW", ("U2", "6"): "BOOT_5V",
    ("L2", "1"): "SW_5V", ("L2", "2"): "+5V_REG",
    ("C27", "1"): "BOOT_5V", ("C27", "2"): "SW_5V",
    ("C28", "1"): "+24V_RAW", ("C28", "2"): "GND",
    ("C29", "1"): "+5V_REG", ("C29", "2"): "GND",
    ("R32", "1"): "+5V_REG", ("R32", "2"): "FB_5V",
    ("R33", "1"): "FB_5V", ("R33", "2"): "GND",

    # Q2: 24V E-Fuse (Gate: EN_24V, Source: +24V_RAW, Drain: +24V_DRV)
    ("Q2", "1"): "EN_24V", ("Q2", "2"): "+24V_RAW", ("Q2", "3"): "+24V_DRV",

    # Q3: 12V E-Fuse (Gate: EN_12V, Source: +12V_REG, Drain: +12V_DRV)
    ("Q3", "1"): "EN_12V", ("Q3", "2"): "+12V_REG", ("Q3", "3"): "+12V_DRV",

    # Q4: 5V E-Fuse (Gate: EN_5V, Source: +5V_REG, Drain: +5V_DRV)
    ("Q4", "1"): "EN_5V", ("Q4", "2"): "+5V_REG", ("Q4", "3"): "+5V_DRV",

    # U3: INA180 for 5V rail (Pin 1: OUT, 2: GND, 3: IN+, 4: IN-, 5: V+)
    ("U3", "1"): "ISENSE_5V", ("U3", "2"): "GND", ("U3", "3"): "+5V_REG", ("U3", "4"): "+5V_DRV", ("U3", "5"): "+3.3V",

    # U11: INA180 for 12V rail
    ("U11", "1"): "ISENSE_12V", ("U11", "2"): "GND", ("U11", "3"): "+12V_REG", ("U11", "4"): "+12V_DRV", ("U11", "5"): "+3.3V",

    # U12: INA180 for 24V rail
    ("U12", "1"): "ISENSE_24V", ("U12", "2"): "GND", ("U12", "3"): "+24V_RAW", ("U12", "4"): "+24V_DRV", ("U12", "5"): "+3.3V",
}

"""

new_code = orig[:idx_s1] + s1_full_code + orig[idx_s2:]

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py", "w", encoding="utf-8") as f:
    f.write(new_code)

print("Updated build_zero_erc_fdd.py with complete Sheet 1!")
