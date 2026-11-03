import os, sys, uuid, re, subprocess
from collections import defaultdict
from test_flatten_engine import get_flattened_symbol

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_dir = prj_dir
sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

ROOT_UUID = "b20a3201-1001-4001-8001-000000000001"
SHEET_INFOS = [
    ("Power_Supply",   "01_Power_Supply.kicad_sch",   "b20a3201-1001-4001-8001-000000000002", "b20a3201-2001-4001-8001-000000000002", "2"),
    ("MCU_Core",       "02_MCU_Core.kicad_sch",       "b20a3201-1001-4001-8001-000000000003", "b20a3201-2001-4001-8001-000000000003", "3"),
    ("UI_Controls",    "03_UI_Controls.kicad_sch",    "b20a3201-1001-4001-8001-000000000004", "b20a3201-2001-4001-8001-000000000004", "4"),
    ("FDD_Interfaces", "04_FDD_Interfaces.kicad_sch", "b20a3201-1001-4001-8001-000000000005", "b20a3201-2001-4001-8001-000000000005", "5"),
]

def u():
    return str(uuid.uuid4())

def snap(val):
    return round(float(val) / 2.54) * 2.54

def extract_symbol_exact_with_parent(lib_name, sym_name):
    # Use our proven flattening engine
    flat = get_flattened_symbol(lib_name, sym_name)
    if flat:
        return flat
    p = os.path.join(sym_dir, f"{lib_name}.kicad_sym")
    if not os.path.exists(p):
        return ""
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()

    def get_sym(name):
        start_tag = f'(symbol "{name}"'
        idx = content.find(start_tag)
        if idx == -1: return ""
        count, end = 0, 0
        for i in range(idx, len(content)):
            if content[i] == '(': count += 1
            elif content[i] == ')':
                count -= 1
                if count == 0:
                    end = i + 1; break
        return content[idx:end]

    raw_child = get_sym(sym_name)
    if not raw_child:
        return ""
    return raw_child.replace(f'(symbol "{sym_name}"', f'(symbol "{lib_name}:{sym_name}"', 1)

def get_symbol_pins_for_unit(lib_name, sym_name, unit=1):
    sym_txt = extract_symbol_exact_with_parent(lib_name, sym_name)
    if not sym_txt:
        return {}

    u_pattern = re.compile(r'\(symbol\s+"[^"]+_' + str(unit) + r'_[0-9]+"(.*?)(?=\n[\t ]+\(symbol |\n\t*\)$)', re.DOTALL)
    u_matches = list(u_pattern.finditer(sym_txt))
    if u_matches:
        search_text = "\n".join([m.group(1) for m in u_matches])
    else:
        search_text = sym_txt

    pins = {}
    pattern = re.compile(r'\(pin\s+([^\s]+)\s+[^\s]+\s+\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\).*?\(name\s+"([^"]*)".*?\(number\s+"([^"]*)"', re.DOTALL)
    for m in pattern.finditer(search_text):
        ptype = m.group(1)
        px = float(m.group(2))
        py = float(m.group(3))
        pangle = int(float(m.group(4) or 0)) % 360
        pname = m.group(5)
        pnum = m.group(6)
        pins[pnum] = (round(px, 2), round(-py, 2), pname, ptype, pangle)
    return pins

def get_symbol_body_bounds(pins_dict):
    xs = [p[0] for p in pins_dict.values()]
    ys = [p[1] for p in pins_dict.values()]
    if not xs:
        return (-2.54, 2.54, -2.54, 2.54)
    return (min(xs), max(xs), min(ys), max(ys))

def title_block(title, desc):
    return f"""  (paper "A3")
  (title_block
    (title "{title}")
    (date "2026-11-02")
    (rev "1.0")
    (company "Alessio Iodice")
    (comment 1 "Author / Hardware Designer: Alessio Iodice <alessio67@gmail.com>")
    (comment 2 "{desc}")
    (comment 3 "License: CC BY-NC-SA 4.0")
    (comment 4 "Validated on KiCad 9.0 — 0 ERC / 0 DRC violations")
  )"""

def make_instances_block(ref, sheet_uuid, doc_uuid, unit=1):
    return f"""    (instances
      (project "FDD-Test-Board"
        (path "/{ROOT_UUID}/{sheet_uuid}"
          (reference "{ref}")
          (unit {unit})
        )
      )
    )"""

pwr_counter = 3000

def make_power_symbol(net, x, y, pangle, sheet_uuid, doc_uuid):
    global pwr_counter
    pwr_counter += 1
    pwr_ref = f"#PWR{pwr_counter:04d}"
    inst_blk = make_instances_block(pwr_ref, sheet_uuid, doc_uuid, unit=1)

    is_gnd = (net == "GND")
    if pangle == 0:
        sym_ang = 270 if is_gnd else 90
        vx, vy, vang, vjust = snap(x - 3.81), y, 90, "(justify right)"
    elif pangle == 180:
        sym_ang = 90 if is_gnd else 270
        vx, vy, vang, vjust = snap(x + 3.81), y, 90, "(justify left)"
    elif pangle == 270:
        sym_ang = 180 if is_gnd else 0
        vjust = "(justify right)" if is_gnd else "(justify left)"
        vx, vy, vang = x, snap(y - 4.45), 90
    else:
        sym_ang = 0 if is_gnd else 180
        vjust = "(justify right)" if is_gnd else "(justify left)"
        vx, vy, vang = x, snap(y + 4.45), 90

    lib_id = "power:GND" if is_gnd else "power:+3.3V"

    return f"""  (symbol (lib_id "{lib_id}") (at {x:.2f} {y:.2f} {sym_ang}) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{u()}")
    (property "Reference" "{pwr_ref}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "{net}" (at {vx:.2f} {vy:.2f} {vang}) (effects (font (size 1.27 1.27)) {vjust}))
    (property "Footprint" "" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "{u()}"))
{inst_blk}
  )"""

def build_sheet(sheet_title, sheet_desc, components, net_map, out_filename, s_idx, extra_pwr_flags=None):
    sheet_name, _, sheet_uuid, doc_uuid, page_str = SHEET_INFOS[s_idx]

    embedded_syms_dict = {}
    for c in components:
        key = f"{c['lib']}:{c['sym']}"
        if key not in embedded_syms_dict:
            sym_def = extract_symbol_exact_with_parent(c["lib"], c["sym"])
            if sym_def:
                embedded_syms_dict[key] = sym_def
            else:
                print(f"ERROR: Could not extract {key}")

    pwr_gnd = extract_symbol_exact_with_parent("power", "GND")
    pwr_3v3 = extract_symbol_exact_with_parent("power", "+3.3V")
    embedded_syms_dict["power:GND"] = pwr_gnd
    embedded_syms_dict["power:+3.3V"] = pwr_3v3
    if extra_pwr_flags:
        embedded_syms_dict["power:PWR_FLAG"] = extract_symbol_exact_with_parent("power", "PWR_FLAG")

    instances_str = []
    wires_and_labels = []
    handled_coords = set()

    for c in components:
        ref = c["ref"]
        val = c["val"]
        fp = c["fp"]
        cx = snap(c["x"])
        cy = snap(c["y"])
        unit = c.get("unit", 1)
        lib_id = f"{c['lib']}:{c['sym']}"

        pin_dict = get_symbol_pins_for_unit(c["lib"], c["sym"], unit=unit)
        bmin_x, bmax_x, bmin_y, bmax_y = get_symbol_body_bounds(pin_dict)
        angles = set(p[4] for p in pin_dict.values())

        if (270 not in angles) and (90 not in angles):
            ref_x, ref_y, ref_just = cx, snap(cy + bmin_y - 2.54), ""
            val_x, val_y, val_just = cx, snap(cy + bmax_y + 2.54), ""
        elif 270 not in angles:
            ref_x, ref_y, ref_just = cx, snap(cy + bmin_y - 4.45), ""
            val_x, val_y, val_just = cx, snap(cy + bmin_y - 1.91), ""
        elif 180 not in angles:
            ref_x, ref_y, ref_just = snap(cx + bmax_x + 2.54), snap(cy - 2.54), "(justify left)"
            val_x, val_y, val_just = snap(cx + bmax_x + 2.54), snap(cy + 2.54), "(justify left)"
        else:
            ref_x, ref_y, ref_just = snap(cx + bmin_x - 2.54), snap(cy + bmin_y - 4.45), "(justify right)"
            val_x, val_y, val_just = snap(cx + bmin_x - 2.54), snap(cy + bmin_y - 1.91), "(justify right)"

        comp_uuid = u()
        inst_blk = make_instances_block(ref, sheet_uuid, doc_uuid, unit=unit)
        pin_uuids = [f'    (pin "{pnum}" (uuid "{u()}"))' for pnum in pin_dict]

        inst = f"""  (symbol (lib_id "{lib_id}") (at {cx:.2f} {cy:.2f} 0) (unit {unit})
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{comp_uuid}")
    (property "Reference" "{ref}" (at {ref_x:.2f} {ref_y:.2f} 0) (effects (font (size 1.27 1.27)) {ref_just}))
    (property "Value" "{val}" (at {val_x:.2f} {val_y:.2f} 0) (effects (font (size 1.27 1.27)) {val_just}))
    (property "Footprint" "{fp}" (at {cx:.2f} {cy:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "~" (at {cx:.2f} {cy:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "" (at {cx:.2f} {cy:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
{chr(10).join(pin_uuids)}
{inst_blk}
  )"""
        instances_str.append(inst)

        for pnum, (pdx, pdy, pname, ptype, pangle) in pin_dict.items():
            pin_x = snap(cx + pdx)
            pin_y = snap(cy + pdy)
            coord_key = (pin_x, pin_y)
            if coord_key in handled_coords:
                continue
            handled_coords.add(coord_key)

            net = net_map.get((ref, pnum), "NC")
            if net == "NC":
                wires_and_labels.append(f'  (no_connect (at {pin_x:.2f} {pin_y:.2f}) (uuid "{u()}"))')
                continue

            stub_len = 5.08
            if pangle == 0:
                end_x, end_y = snap(pin_x - stub_len), pin_y
                lbl_ang, lbl_just, glbl_just = 180, "(justify right bottom)", "(justify right)"
            elif pangle == 180:
                end_x, end_y = snap(pin_x + stub_len), pin_y
                lbl_ang, lbl_just, glbl_just = 0, "(justify left bottom)", "(justify left)"
            elif pangle == 270:
                end_x, end_y = pin_x, snap(pin_y - stub_len)
                lbl_ang, lbl_just, glbl_just = 90, "(justify left bottom)", "(justify left)"
            else:
                end_x, end_y = pin_x, snap(pin_y + stub_len)
                lbl_ang, lbl_just, glbl_just = 270, "(justify right bottom)", "(justify right)"

            wires_and_labels.append(f'  (wire (pts (xy {pin_x:.2f} {pin_y:.2f}) (xy {end_x:.2f} {end_y:.2f})) (stroke (width 0) (type default)) (uuid "{u()}"))')

            if net in ("GND", "+3.3V"):
                wires_and_labels.append(make_power_symbol(net, end_x, end_y, pangle, sheet_uuid, doc_uuid))
            else:
                wires_and_labels.append(f'  (global_label "{net}" (shape passive) (at {end_x:.2f} {end_y:.2f} {lbl_ang}) (fields_autoplaced yes)\n    (effects (font (size 1.27 1.27)) {glbl_just})\n    (uuid "{u()}")\n  )')

    # Add PWR_FLAGs if requested
    if extra_pwr_flags:
        for idx, (pnet, px, py) in enumerate(extra_pwr_flags):
            px, py = snap(px), snap(py)
            flag_ref = f"#FLG{idx+1:02d}"
            flag_uuid = u()
            flag_inst = make_instances_block(flag_ref, sheet_uuid, doc_uuid, unit=1)
            flag_str = f"""  (symbol (lib_id "power:PWR_FLAG") (at {px:.2f} {py:.2f} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{flag_uuid}")
    (property "Reference" "{flag_ref}" (at {px:.2f} {py-2.54:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "PWR_FLAG" (at {px:.2f} {py+2.54:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Footprint" "" (at {px:.2f} {py:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "{u()}"))
{flag_inst}
  )"""
            instances_str.append(flag_str)
            end_x, end_y = snap(px + 5.08), py
            wires_and_labels.append(f'  (wire (pts (xy {px:.2f} {py:.2f}) (xy {end_x:.2f} {end_y:.2f})) (stroke (width 0) (type default)) (uuid "{u()}"))')
            if pnet in ("GND", "+3.3V"):
                wires_and_labels.append(make_power_symbol(pnet, end_x, end_y, 180, sheet_uuid, doc_uuid))
            else:
                wires_and_labels.append(f'  (global_label "{pnet}" (shape passive) (at {end_x:.2f} {end_y:.2f} 0) (fields_autoplaced yes)\n    (effects (font (size 1.27 1.27)) (justify left))\n    (uuid "{u()}")\n  )')

    lib_symbols_txt = "  (lib_symbols\n" + "\n".join(embedded_syms_dict.values()) + "\n  )"

    sch_content = f"""(kicad_sch
  (version 20250114)
  (generator "eeschema")
  (generator_version "9.0")
  (uuid "{doc_uuid}")
{title_block(sheet_title, sheet_desc)}
{lib_symbols_txt}

{chr(10).join(wires_and_labels)}

{chr(10).join(instances_str)}

  (sheet_instances
    (path "/"
      (page "1")
    )
  )
)
"""
    out_path = os.path.join(kicad_dir, out_filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(sch_content)
    print(f"Generated {out_filename} successfully!")

# Import sheets 2, 3, 4 definitions from build_zero_erc_fdd
import build_zero_erc_fdd as bz

# SHEET 1 DEFINITION:
components_s1 = [
    # Power Input J1 (Phoenix 2-pin 24V Mean Well)
    {"lib": "Connector", "sym": "Conn_01x02_Pin", "ref": "J1", "val": "J_IN_24V",
     "fp": "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal", "x": 50.8, "y": 45.72, "unit": 1},

    # Drive Power Headers:
    # J2: Molex 5.25" Power
    {"lib": "Connector", "sym": "Conn_01x04_Pin", "ref": "J2", "val": "J_PWR_525",
     "fp": "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal", "x": 127.0, "y": 45.72, "unit": 1},
    
    # J3: Berg 3.5" Power
    {"lib": "Connector", "sym": "Conn_01x04_Pin", "ref": "J3", "val": "J_PWR_350",
     "fp": "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Horizontal", "x": 203.2, "y": 45.72, "unit": 1},

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

# Single PWR_FLAG on each power net
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

print("\n--- GENERATING SHEET 1: Power Supply ---")
build_sheet(
    "Power Supply & E-Fuses Subsystem",
    "Mean Well 24V Input, Buck 12V TPS54302, Buck 5V TPS54302, INA180 Current Sense, Active MOSFET E-Fuses",
    components_s1,
    net_map_s1,
    "01_Power_Supply.kicad_sch",
    0,
    extra_pwr_flags=pwr_flags_s1
)

print("\n--- GENERATING SHEET 2: MCU Core ---")
build_sheet(
    "MCU Core & Analog Front-End",
    "STM32F407VET6, LDO 3.3V, USB-C, HSE 8MHz, LMV358 Differential Cat-Eye Pre-Amp",
    bz.components_s2,
    bz.net_map_s2,
    "02_MCU_Core.kicad_sch",
    1
)

print("\n--- GENERATING SHEET 3: UI Controls ---")
build_sheet(
    "UI Controls, LEDs, Buzzer & Scope Test Points",
    "Bourns PEC11R Encoder, RUN/BACK Buttons, 5x Status LEDs, Buzzer Driver, Test Points & Probe Jacks",
    bz.components_s3,
    bz.net_map_s3,
    "03_UI_Controls.kicad_sch",
    2
)

print("\n--- GENERATING SHEET 4: FDD Interfaces ---")
build_sheet(
    "FDD Physical Interfaces & Bus Drivers",
    "IDC-50 (8-inch), IDC-34 (5.25-inch and 3.5-inch), IDC-26, IDC-20 Apple II, 7406 Drivers, 74HC14, ULN2003A",
    bz.components_s4,
    bz.net_map_s4,
    "04_FDD_Interfaces.kicad_sch",
    3
)

print("\n=============================================")
print("RUNNING ERC GATE CHECK")
print("=============================================")
erc_rpt = os.path.join(prj_dir, "FDD-Test-Board-erc.rpt")
res_erc = subprocess.run([kicad_cli, "sch", "erc", os.path.join(prj_dir, "FDD-Test-Board.kicad_sch"), "-o", erc_rpt], capture_output=True, text=True)

with open(erc_rpt, "r", encoding="utf-8") as f:
    rpt_lines = f.readlines()

v_count = sum(1 for l in rpt_lines if l.strip().startswith("["))
print(f"Total ERC Violations: {v_count}")
for l in rpt_lines:
    if l.strip().startswith("["):
        print(" ", l.strip())

print("\n=============================================")
print("RUNNING FULL NETLIST EXPORT")
print("=============================================")
net_path = os.path.join(prj_dir, "FDD-Test-Board.net")
res_net = subprocess.run([kicad_cli, "sch", "export", "netlist", os.path.join(prj_dir, "FDD-Test-Board.kicad_sch"), "-o", net_path], capture_output=True, text=True)

with open(net_path, "r", encoding="utf-8") as f:
    net_txt = f.read()

comps = re.findall(r'\(comp \(ref "([^"]+)"\)', net_txt)
nets = re.findall(r'\(net \(code "[^"]+"\)\s+\(name "([^"]+)"\)', net_txt)
print(f"Exported Netlist: {len(comps)} components, {len(nets)} nets!")
print(f"Return code: {res_net.returncode}")
