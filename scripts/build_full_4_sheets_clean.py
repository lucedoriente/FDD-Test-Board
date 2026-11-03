import os, sys, re, subprocess
from generate_all_4_sheets_clean import build_sheet
import build_zero_erc_fdd as bz

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

# --- SHEET 1: POWER SUPPLY & CONNECTORS ---
components_s1 = [
    # Power Input J1 (Phoenix 2-pin 24V Mean Well)
    {"lib": "Connector", "sym": "Conn_01x02_Pin", "ref": "J1", "val": "J_IN_24V",
     "fp": "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal", "x": 50.8, "y": 45.72, "unit": 1},

    # Drive Power Headers:
    # J2: Molex 5.25" Power
    {"lib": "Connector", "sym": "Conn_01x04_Pin", "ref": "J2", "val": "J_PWR_525",
     "fp": "Connector_Molex:Molex_0015244048_1x04_P5.08mm_Horizontal", "x": 127.0, "y": 45.72, "unit": 1},
    
    # J3: Berg 3.5" Power
    {"lib": "Connector", "sym": "Conn_01x04_Pin", "ref": "J3", "val": "J_PWR_350",
     "fp": "Connector_TE-Connectivity:TE_171826-4_1x04_P2.50mm_Horizontal", "x": 203.2, "y": 45.72, "unit": 1},

    # J4: Phoenix 8" Power
    {"lib": "Connector", "sym": "Conn_01x04_Pin", "ref": "J4", "val": "J_PWR_800",
     "fp": "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal", "x": 279.4, "y": 45.72, "unit": 1},

    # J5: Sunton 7" Smart Display Console Header
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

# 9 single PWR_FLAGs to power all rails cleanly without duplicates
pwr_flags_s1 = [
    ("+24V_RAW", 279.4, 215.9),
    ("GND",      304.8, 215.9),
    ("+12V_REG", 330.2, 215.9),
    ("+5V_REG",  355.6, 215.9),
    ("+3.3V",    381.0, 215.9),
    ("+24V_DRV", 279.4, 241.3),
    ("+12V_DRV", 304.8, 241.3),
    ("+5V_DRV",  330.2, 241.3),
    ("-12V_DRV", 355.6, 241.3),
]

print("Generating Sheet 1: Power Supply...")
build_sheet(
    "Power Supply & E-Fuses Subsystem",
    "Mean Well 24V Input, Buck 12V TPS54302, Buck 5V TPS54302, INA180 Current Sense, Active MOSFET E-Fuses",
    components_s1,
    net_map_s1,
    "01_Power_Supply.kicad_sch",
    0,
    pwr_flags=pwr_flags_s1
)

print("Generating Sheet 2: MCU Core...")
build_sheet(
    "MCU Core & Analog Front-End",
    "STM32F407VET6, LDO 3.3V, USB-C, HSE 8MHz, LMV358 Differential Cat-Eye Pre-Amp",
    bz.components_s2,
    bz.net_map_s2,
    "02_MCU_Core.kicad_sch",
    1
)

print("Generating Sheet 3: UI Controls...")
build_sheet(
    "UI Controls, LEDs, Buzzer & Scope Test Points",
    "Bourns PEC11R Encoder, RUN/BACK Buttons, 5x Status LEDs, Buzzer Driver, Test Points & Probe Jacks",
    bz.components_s3,
    bz.net_map_s3,
    "03_UI_Controls.kicad_sch",
    2
)

print("Generating Sheet 4: FDD Physical Interfaces...")
build_sheet(
    "FDD Physical Interfaces & Bus Drivers",
    "IDC-50 (8-inch), IDC-34 (5.25-inch and 3.5-inch), IDC-26, IDC-20 Apple II, 7406 Drivers, 74HC14, ULN2003A",
    bz.components_s4,
    bz.net_map_s4,
    "04_FDD_Interfaces.kicad_sch",
    3
)

print("\n--- Running ERC Gate Check ---")
erc_rpt = os.path.join(prj_dir, "FDD-Test-Board-erc.rpt")
res_erc = subprocess.run([kicad_cli, "sch", "erc", os.path.join(prj_dir, "FDD-Test-Board.kicad_sch"), "-o", erc_rpt], capture_output=True, text=True)
print("ERC stdout:", res_erc.stdout.strip())

with open(erc_rpt, "r", encoding="utf-8") as f:
    rpt_lines = f.readlines()

v_count = sum(1 for l in rpt_lines if l.strip().startswith("["))
print(f"Total ERC Violations: {v_count}")
for l in rpt_lines:
    if l.strip().startswith("["):
        print(" ", l.strip())

print("\n--- Running Full Netlist Export ---")
net_path = os.path.join(prj_dir, "FDD-Test-Board.net")
res_net = subprocess.run([kicad_cli, "sch", "export", "netlist", os.path.join(prj_dir, "FDD-Test-Board.kicad_sch"), "-o", net_path], capture_output=True, text=True)

with open(net_path, "r", encoding="utf-8") as f:
    net_txt = f.read()

comps = re.findall(r'\(comp \(ref "([^"]+)"\)', net_txt)
nets = re.findall(r'\(net \(code "[^"]+"\)\s+\(name "([^"]+)"\)', net_txt)
print(f"Exported Netlist: {len(comps)} components, {len(nets)} nets!")
print("Components sample:", sorted(comps)[:30])
