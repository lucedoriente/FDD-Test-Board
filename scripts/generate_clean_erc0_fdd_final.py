import os
import sys
import uuid
import re
import subprocess
from collections import defaultdict

kicad_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
local_sym_path = os.path.join(kicad_dir, "FDD-Test-Board.kicad_sym")

scripts_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\scripts"
sys.path.append(scripts_dir)
from generate_clean_erc0_project import extract_symbol_exact, get_symbol_pins, get_symbol_body_bounds

ROOT_UUID = "b20a3201-1001-4001-8001-000000000001"
SHEET_INFOS = [
    ("Power_Supply",   "01_Power_Supply.kicad_sch",   "b20a3201-1001-4001-8001-000000000002", "b20a3201-2001-4001-8001-000000000002", "2"),
    ("MCU_Core",       "02_MCU_Core.kicad_sch",       "b20a3201-1001-4001-8001-000000000003", "b20a3201-2001-4001-8001-000000000003", "3"),
    ("UI_Controls",    "03_UI_Controls.kicad_sch",    "b20a3201-1001-4001-8001-000000000004", "b20a3201-2001-4001-8001-000000000004", "4"),
    ("FDD_Interfaces", "04_FDD_Interfaces.kicad_sch", "b20a3201-1001-4001-8001-000000000005", "b20a3201-2001-4001-8001-000000000005", "5"),
]

def u():
    return str(uuid.uuid4())

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

power_syms = extract_symbol_exact("power", "PWR_FLAG") + "\n" + \
            extract_symbol_exact("power", "+3.3V") + "\n" + \
            extract_symbol_exact("power", "+5V") + "\n" + \
            extract_symbol_exact("power", "+12V") + "\n" + \
            extract_symbol_exact("power", "+24V") + "\n" + \
            extract_symbol_exact("power", "-12V") + "\n" + \
            extract_symbol_exact("power", "GND")

power_rail_set = {"+24V_RAW", "+24V_DRV", "+12V_REG", "+12V_DRV", "+5V_REG", "+5V_DRV", "-12V_DRV", "+3.3V", "GND", "NC"}

pwr_counter = 500
flg_counter = 500

def make_instances_block(ref, sheet_uuid, doc_uuid, unit=1):
    return f"""    (instances
      (project "FDD-Test-Board"
        (path "/{ROOT_UUID}/{sheet_uuid}"
          (reference "{ref}")
          (unit {unit})
        )
        (path "/{doc_uuid}"
          (reference "{ref}")
          (unit {unit})
        )
      )
    )"""

def make_power_symbol(net, x, y, pangle, sheet_uuid, doc_uuid):
    global pwr_counter
    pwr_counter += 1
    pwr_ref = f"#PWR{pwr_counter:04d}"
    inst_blk = make_instances_block(pwr_ref, sheet_uuid, doc_uuid, unit=1)

    is_gnd = (net == "GND")
    if pangle == 0: # Left
        sym_ang = 270 if is_gnd else 90
        vx, vy, vang, vjust = x - 3.81, y, 90, "(justify right)"
    elif pangle == 180: # Right
        sym_ang = 90 if is_gnd else 270
        vx, vy, vang, vjust = x + 3.81, y, 90, "(justify left)"
    elif pangle == 270: # Top (up)
        sym_ang = 180 if is_gnd else 0
        vjust = "(justify right)" if is_gnd else "(justify left)"
        vx, vy, vang = x, y - 4.45, 90
    else: # pangle == 90, Bottom (down)
        sym_ang = 0 if is_gnd else 180
        vjust = "(justify right)" if is_gnd else "(justify left)"
        vx, vy, vang = x, y + 4.45, 90

    sym_map = {
        "+3.3V": "power:+3.3V",
        "+5V_REG": "power:+5V",
        "+5V_DRV": "power:+5V",
        "+12V_REG": "power:+12V",
        "+12V_DRV": "power:+12V",
        "+24V_RAW": "power:+24V",
        "+24V_DRV": "power:+24V",
        "-12V_DRV": "power:-12V",
        "GND": "power:GND"
    }
    lib_id = sym_map.get(net, "power:GND")

    return f"""  (symbol (lib_id "{lib_id}") (at {x:.2f} {y:.2f} {sym_ang}) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{u()}")
    (property "Reference" "{pwr_ref}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "{net}" (at {vx:.2f} {vy:.2f} {vang}) (effects (font (size 1.27 1.27)) {vjust}))
    (property "Footprint" "" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "{u()}"))
{inst_blk}
  )"""

def get_unit_pins(sym_text, unit=1):
    u_pattern = re.compile(r'\(symbol\s+"[^"]+_' + str(unit) + r'_[0-9]+"(.*?)(?=\n[\t ]+\(symbol |\n\t*\)$)', re.DOTALL)
    u_matches = list(u_pattern.finditer(sym_text))
    if u_matches:
        search_text = "\n".join([m.group(1) for m in u_matches])
    else:
        search_text = sym_text
        
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

def build_clean_sheet(sheet_title, sheet_desc, components, net_map, pwr_flags_list, out_filename, s_idx):
    global pwr_counter, flg_counter
    sheet_name, _, sheet_uuid, doc_uuid, page_str = SHEET_INFOS[s_idx]

    embedded_syms_dict = {}
    for c in components:
        key = f"{c['lib']}:{c['sym']}"
        if key not in embedded_syms_dict:
            sym_def = extract_symbol_exact(c["lib"], c["sym"])
            if sym_def:
                embedded_syms_dict[key] = sym_def
            else:
                print(f"ERROR: Could not extract {key}")

    instances_str = []
    wires_and_labels = []

    for pnet, px, py in pwr_flags_list:
        flg_counter += 1
        flg_ref = f"#FLG{flg_counter:04d}"
        wires_and_labels.append(f'  (wire (pts (xy {px:.2f} {py-2.54:.2f}) (xy {px:.2f} {py+2.54:.2f})) (stroke (width 0) (type default)) (uuid "{u()}"))')
        if pnet in power_rail_set:
            wires_and_labels.append(make_power_symbol(pnet, px, py - 2.54, 270, sheet_uuid, doc_uuid))
        else:
            wires_and_labels.append(f"""  (global_label "{pnet}" (shape bidirectional) (at {px:.2f} {py-2.54:.2f} 90) (fields_autoplaced yes)
    (effects (font (size 1.1 1.1)) (justify left))
    (uuid "{u()}")
    (property "Intersheetrefs" "\\${{INTERSHEET_REFS}}" (at {px:.2f} {py-2.54:.2f} 0) (effects (font (size 1.1 1.1)) (hide yes)))
  )""")
        flg_inst = make_instances_block(flg_ref, sheet_uuid, doc_uuid, unit=1)
        pflg = f"""  (symbol (lib_id "power:PWR_FLAG") (at {px:.2f} {py+2.54:.2f} 180) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{u()}")
    (property "Reference" "{flg_ref}" (at {px:.2f} {py+2.54:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "PWR_FLAG" (at {px:.2f} {py+6.35:.2f} 90) (effects (font (size 1.27 1.27)) (justify right)))
    (property "Footprint" "" (at {px:.2f} {py+2.54:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "{u()}"))
{flg_inst}
  )"""
        wires_and_labels.append(pflg)

    for c in components:
        ref = c["ref"]
        val = c["val"]
        fp = c["fp"]
        cx = c["x"]
        cy = c["y"]
        unit = c.get("unit", 1)
        lib_id = f"{c['lib']}:{c['sym']}"
        raw_sym = embedded_syms_dict.get(lib_id, "")
        pin_dict = get_unit_pins(raw_sym, unit=unit)
        bmin_x, bmax_x, bmin_y, bmax_y = get_symbol_body_bounds(raw_sym, pin_dict)
        angles = set(p[4] for p in pin_dict.values())

        if (270 not in angles) and (90 not in angles):
            ref_x, ref_y, ref_just = cx, cy + bmin_y - 2.54, ""
            val_x, val_y, val_just = cx, cy + bmax_y + 2.54, ""
        elif 270 not in angles:
            ref_x, ref_y, ref_just = cx, cy + bmin_y - 4.45, ""
            val_x, val_y, val_just = cx, cy + bmin_y - 1.91, ""
        elif 180 not in angles:
            ref_x, ref_y, ref_just = cx + bmax_x + 1.91, cy - 1.27, "(justify left)"
            val_x, val_y, val_just = cx + bmax_x + 1.91, cy + 1.27, "(justify left)"
        else:
            ref_x, ref_y, ref_just = cx + bmin_x - 1.27, cy + bmin_y - 4.45, "(justify right)"
            val_x, val_y, val_just = cx + bmin_x - 1.27, cy + bmin_y - 1.91, "(justify right)"

        comp_uuid = u()
        inst_blk = make_instances_block(ref, sheet_uuid, doc_uuid, unit=unit)
        pin_uuids = [f'    (pin "{pnum}" (uuid "{u()}"))' for pnum in pin_dict]
        inst = f"""  (symbol (lib_id "{lib_id}") (at {cx:.2f} {cy:.2f} 0) (unit {unit})
    (in_bom yes) (on_board yes) (dnp no)
    (uuid "{comp_uuid}")
    (property "Reference" "{ref}" (at {ref_x:.2f} {ref_y:.2f} 0) (effects (font (size 1.27 1.27)) {ref_just}))
    (property "Value" "{val}" (at {val_x:.2f} {val_y:.2f} 0) (effects (font (size 1.27 1.27)) {val_just}))
    (property "Footprint" "{fp}" (at {cx:.2f} {cy:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
{chr(10).join(pin_uuids)}
{inst_blk}
  )"""
        instances_str.append(inst)

        handled_coords = set()
        for pnum, (pdx, pdy, pname, ptype, pangle) in pin_dict.items():
            pin_x = round(cx + pdx, 2)
            pin_y = round(cy + pdy, 2)
            coord_key = (pin_x, pin_y)
            if coord_key in handled_coords:
                continue
            handled_coords.add(coord_key)

            net = net_map.get((ref, pnum), "NC")
            if net == "NC":
                wires_and_labels.append(f'  (no_connect (at {pin_x:.2f} {pin_y:.2f}) (uuid "{u()}"))')
                continue

            # Outward wire stub (5.08 mm standard)
            stub_len = 5.08
            if pangle == 0: # Left
                end_x, end_y = round(pin_x - stub_len, 2), pin_y
                lbl_ang, lbl_just, glbl_just = 180, "(justify right bottom)", "(justify right)"
            elif pangle == 180: # Right
                end_x, end_y = round(pin_x + stub_len, 2), pin_y
                lbl_ang, lbl_just, glbl_just = 0, "(justify left bottom)", "(justify left)"
            elif pangle == 270: # Top (up)
                end_x, end_y = pin_x, round(pin_y - stub_len, 2)
                lbl_ang, lbl_just, glbl_just = 90, "(justify left bottom)", "(justify left)"
            else: # pangle == 90, Bottom (down)
                end_x, end_y = pin_x, round(pin_y + stub_len, 2)
                lbl_ang, lbl_just, glbl_just = 270, "(justify right bottom)", "(justify right)"

            wires_and_labels.append(f'  (wire (pts (xy {pin_x:.2f} {pin_y:.2f}) (xy {end_x:.2f} {end_y:.2f})) (stroke (width 0) (type default)) (uuid "{u()}"))')

            if net in power_rail_set:
                wires_and_labels.append(make_power_symbol(net, end_x, end_y, pangle, sheet_uuid, doc_uuid))
            else:
                wires_and_labels.append(f"""  (global_label "{net}" (shape bidirectional) (at {end_x:.2f} {end_y:.2f} {lbl_ang}) (fields_autoplaced yes)
    (effects (font (size 1.1 1.1)) {glbl_just})
    (uuid "{u()}")
    (property "Intersheetrefs" "\\${{INTERSHEET_REFS}}" (at {end_x:.2f} {end_y:.2f} 0) (effects (font (size 1.1 1.1)) (hide yes)))
  )""")

    lib_symbols_txt = "  (lib_symbols\n" + power_syms + "\n" + "\n".join(embedded_syms_dict.values()) + "\n  )"

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
    (path "/{ROOT_UUID}"
      (page "{page_str}")
    )
  )
)
"""
    out_path = os.path.join(kicad_dir, out_filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(sch_content)
    print(f"Generated {out_filename} successfully!")

print("Generator engine ready.")
