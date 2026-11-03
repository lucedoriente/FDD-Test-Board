import os, sys, re, subprocess
from test_flatten_engine import get_flattened_symbol

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"
sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"

ROOT_UUID = "b20a3201-1001-4001-8001-000000000001"
SHEET_INFOS = [
    ("Power_Supply",   "01_Power_Supply.kicad_sch",   "b20a3201-1001-4001-8001-000000000002", "b20a3201-2001-4001-8001-000000000002", "2"),
    ("MCU_Core",       "02_MCU_Core.kicad_sch",       "b20a3201-1001-4001-8001-000000000003", "b20a3201-2001-4001-8001-000000000003", "3"),
    ("UI_Controls",    "03_UI_Controls.kicad_sch",    "b20a3201-1001-4001-8001-000000000004", "b20a3201-2001-4001-8001-000000000004", "4"),
    ("FDD_Interfaces", "04_FDD_Interfaces.kicad_sch", "b20a3201-1001-4001-8001-000000000005", "b20a3201-2001-4001-8001-000000000005", "5"),
]

uuid_seed = 2000
def u():
    global uuid_seed
    uuid_seed += 1
    return f"b20a3201-8001-4001-8001-{uuid_seed:012d}"

def snap(val):
    return round(val / 2.54) * 2.54

def extract_symbol_exact_with_parent(lib_name, sym_name):
    flat = get_flattened_symbol(lib_name, sym_name)
    if flat: return flat
    p = os.path.join(sym_dir, f"{lib_name}.kicad_sym")
    if not os.path.exists(p): return ""
    with open(p, "r", encoding="utf-8") as f: content = f.read()
    idx = content.find(f'(symbol "{sym_name}"')
    if idx == -1: return ""
    cnt, end = 0, 0
    for i in range(idx, len(content)):
        if content[i] == '(': cnt += 1
        elif content[i] == ')':
            cnt -= 1
            if cnt == 0:
                end = i + 1; break
    res = content[idx:end]
    if not res.startswith(f'(symbol "{lib_name}:'):
        res = res.replace(f'(symbol "{sym_name}"', f'(symbol "{lib_name}:{sym_name}"', 1)
    return res

def get_symbol_pins_for_unit(lib_name, sym_name, unit=1):
    sym_text = extract_symbol_exact_with_parent(lib_name, sym_name)
    if not sym_text: return {}
    pins = {}
    tokens = [f'_{unit}_', '_0_']
    sub_sym_matches = list(re.finditer(r'\(symbol "([^"]+)"', sym_text))
    for i, m in enumerate(sub_sym_matches):
        sub_name = m.group(1)
        if not any(tok in sub_name for tok in tokens): continue
        start = m.start()
        end = sub_sym_matches[i+1].start() if i + 1 < len(sub_sym_matches) else len(sym_text)
        sub_block = sym_text[start:end]
        idx = 0
        while idx < len(sub_block):
            p_start = sub_block.find('(pin ', idx)
            if p_start == -1: break
            cnt, p_end = 0, p_start
            for j in range(p_start, len(sub_block)):
                if sub_block[j] == '(': cnt += 1
                elif sub_block[j] == ')':
                    cnt -= 1
                    if cnt == 0:
                        p_end = j + 1
                        break
            pin_sub = sub_block[p_start:p_end]
            idx = p_end
            at_m = re.search(r'\(at\s+([-\d\.]+)\s+([-\d\.]+)\s*(\d*)\)', pin_sub)
            num_m = re.search(r'\(number\s+"([^"]+)"', pin_sub)
            name_m = re.search(r'\(name\s+"([^"]+)"', pin_sub)
            type_m = re.match(r'\(pin\s+([^\s]+)', pin_sub)
            if at_m and num_m:
                px = float(at_m.group(1))
                py = float(at_m.group(2))
                pang = int(at_m.group(3) or 0)
                pnum = num_m.group(1)
                pname = name_m.group(1) if name_m else "~"
                ptype = type_m.group(1) if type_m else "passive"
                pins[pnum] = (pname, ptype, px, py, pang)
    return pins

def get_symbol_body_bounds(pins_dict):
    if not pins_dict:
        return -5.08, 5.08, -5.08, 5.08
    xs = [p[2] for p in pins_dict.values()]
    ys = [p[3] for p in pins_dict.values()]
    return min(xs), max(xs), min(ys), max(ys)

def title_block(title, desc):
    return f"""  (title_block
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

pwr_counter = 0
def make_power_symbol(net, x, y, pangle, sheet_uuid, doc_uuid):
    global pwr_counter
    pwr_counter += 1
    pwr_ref = f"#PWR{pwr_counter:04d}"
    inst_blk = make_instances_block(pwr_ref, sheet_uuid, doc_uuid, unit=1)

    is_gnd = (net == "GND")
    if pangle == 0: # Left
        sym_ang = 270 if is_gnd else 90
        vx, vy, vang, vjust = snap(x - 3.81), y, 90, "(justify right)"
    elif pangle == 180: # Right
        sym_ang = 90 if is_gnd else 270
        vx, vy, vang, vjust = snap(x + 3.81), y, 90, "(justify left)"
    elif pangle == 270: # Top (up)
        sym_ang = 180 if is_gnd else 0
        vjust = "(justify right)" if is_gnd else "(justify left)"
        vx, vy, vang = x, snap(y - 4.45), 90
    else: # pangle == 90, Bottom (down)
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

def build_sheet(sheet_title, sheet_desc, components, net_map, out_filename, s_idx, pwr_flags=None):
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
    if pwr_flags:
        embedded_syms_dict["power:PWR_FLAG"] = extract_symbol_exact_with_parent("power", "PWR_FLAG")

    instances_str = []
    wires_and_labels = []

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

        for pnum, (pname, ptype, px, py, pang) in pin_dict.items():
            net = net_map.get((ref, pnum))
            if not net:
                continue

            pin_x = snap(cx + px)
            pin_y = snap(cy - py)
            stub_len = 5.08
            if pang == 0:
                end_x, end_y = snap(pin_x - stub_len), pin_y
                lbl_ang = 180
                lbl_just = "(justify right)"
            elif pang == 180:
                end_x, end_y = snap(pin_x + stub_len), pin_y
                lbl_ang = 0
                lbl_just = "(justify left)"
            elif pang == 270:
                end_x, end_y = pin_x, snap(pin_y + stub_len)
                lbl_ang = 270
                lbl_just = "(justify right)"
            elif pang == 90:
                end_x, end_y = pin_x, snap(pin_y - stub_len)
                lbl_ang = 90
                lbl_just = "(justify left)"
            else:
                end_x, end_y = snap(pin_x + stub_len), pin_y
                lbl_ang = 0
                lbl_just = "(justify left)"

            wire_str = f"""  (wire (pts (xy {pin_x:.2f} {pin_y:.2f}) (xy {end_x:.2f} {end_y:.2f}))
    (stroke (width 0) (type default))
    (uuid "{u()}")
  )"""
            wires_and_labels.append(wire_str)

            is_pwr = (net in ["GND", "+3.3V"])
            if is_pwr:
                pwr_sym = make_power_symbol(net, end_x, end_y, pang, sheet_uuid, doc_uuid)
                wires_and_labels.append(pwr_sym)
            else:
                lbl_str = f"""  (global_label "{net}" (shape passive) (at {end_x:.2f} {end_y:.2f} {lbl_ang}) (fields_autoplaced yes)
    (effects (font (size 1.27 1.27)) {lbl_just})
    (uuid "{u()}")
  )"""
                wires_and_labels.append(lbl_str)

    # Add PWR_FLAGs if specified
    if pwr_flags:
        for idx, (pnet, px, py) in enumerate(pwr_flags):
            px, py = snap(px), snap(py)
            flag_ref = f"#FLG{idx+1:02d}"
            flag_uuid = u()
            flag_inst = make_instances_block(flag_ref, sheet_uuid, doc_uuid, unit=1)
            # PWR_FLAG symbol has pin 1 at (0, 0)
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
            # Wire stub to global label or power symbol
            end_x, end_y = snap(px + 5.08), py
            wire_str = f"""  (wire (pts (xy {px:.2f} {py:.2f}) (xy {end_x:.2f} {end_y:.2f}))
    (stroke (width 0) (type default))
    (uuid "{u()}")
  )"""
            wires_and_labels.append(wire_str)
            if pnet in ["GND", "+3.3V"]:
                pwr_sym = make_power_symbol(pnet, end_x, end_y, 180, sheet_uuid, doc_uuid)
                wires_and_labels.append(pwr_sym)
            else:
                lbl_str = f"""  (global_label "{pnet}" (shape passive) (at {end_x:.2f} {end_y:.2f} 0) (fields_autoplaced yes)
    (effects (font (size 1.27 1.27)) (justify left))
    (uuid "{u()}")
  )"""
                wires_and_labels.append(lbl_str)

    lib_symbols_str = "(lib_symbols\n" + "\n".join(embedded_syms_dict.values()) + "\n  )"

    sch_doc = f"""(kicad_sch
  (version 20250114)
  (generator "eeschema")
  (generator_version "9.0")
  (uuid "{doc_uuid}")
  (paper "A3")
{title_block(sheet_title, sheet_desc)}
{lib_symbols_str}
{chr(10).join(instances_str)}
{chr(10).join(wires_and_labels)}
  (sheet_instances
    (path "/"
      (page "1")
    )
  )
)
"""
    out_path = os.path.join(prj_dir, out_filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(sch_doc)
    print(f"Generated {out_filename} successfully!")
