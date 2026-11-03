import os
import sys
import uuid
import re
import subprocess
from collections import defaultdict

kicad_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
local_sym_path = os.path.join(kicad_dir, "FDD-Test-Board.kicad_sym")

ROOT_UUID = "b20a3201-1001-4001-8001-000000000001"
SHEET_INFOS = [
    ("Power_Supply",   "01_Power_Supply.kicad_sch",   "b20a3201-1001-4001-8001-000000000002", "b20a3201-2001-4001-8001-000000000002", "2"),
    ("MCU_Core",       "02_MCU_Core.kicad_sch",       "b20a3201-1001-4001-8001-000000000003", "b20a3201-2001-4001-8001-000000000003", "3"),
    ("UI_Controls",    "03_UI_Controls.kicad_sch",    "b20a3201-1001-4001-8001-000000000004", "b20a3201-2001-4001-8001-000000000004", "4"),
    ("FDD_Interfaces", "04_FDD_Interfaces.kicad_sch", "b20a3201-1001-4001-8001-000000000005", "b20a3201-2001-4001-8001-000000000005", "5"),
]

def u():
    return str(uuid.uuid4())

def extract_symbol_exact(lib_name, sym_name):
    if lib_name == "FDD-Test-Board":
        lib_path = local_sym_path
    else:
        lib_path = os.path.join(sym_dir, lib_name + ".kicad_sym")
        
    with open(lib_path, "r", encoding="utf-8") as f:
        content = f.read()
    start_tag = f'(symbol "{sym_name}"'
    idx = content.find(start_tag)
    if idx == -1:
        return ""
    depth = 0
    end_idx = idx
    for i in range(idx, len(content)):
        if content[i] == '(':
            depth += 1
        elif content[i] == ')':
            depth -= 1
            if depth == 0:
                end_idx = i + 1
                break
    sym_text = content[idx:end_idx]
    
    # Check if extends
    m_ext = re.search(r'\(extends "([^"]+)"\)', sym_text)
    if m_ext:
        parent_name = m_ext.group(1)
        p_start_tag = f'(symbol "{parent_name}"'
        p_idx = content.find(p_start_tag)
        if p_idx != -1:
            p_depth = 0
            p_end = p_idx
            for i in range(p_idx, len(content)):
                if content[i] == '(':
                    p_depth += 1
                elif content[i] == ')':
                    p_depth -= 1
                    if p_depth == 0:
                        p_end = i + 1
                        break
            p_sym_text = content[p_idx:p_end]
            sub_pattern = re.compile(r'[\t ]+\(symbol "' + re.escape(parent_name) + r'_([0-9]+_[0-9]+)"(.*?)(?=\n[\t ]+\(symbol |\n\t*\)$)', re.DOTALL)
            parent_sub_symbols = []
            for m in sub_pattern.finditer(p_sym_text):
                sub_id = m.group(1)
                sub_body = m.group(2)
                parent_sub_symbols.append(f'  (symbol "{sym_name}_{sub_id}"{sub_body}')
            
            parent_graphics = "\n".join(parent_sub_symbols)
            idx_ext = sym_text.find('(extends')
            idx_ext_end = sym_text.find(')', idx_ext) + 1
            sym_clean = sym_text[:idx_ext] + sym_text[idx_ext_end:]
            idx_last = sym_clean.rfind(')')
            sym_text = sym_clean[:idx_last] + "\n" + parent_graphics + "\n)"

    if not sym_text.startswith(f'(symbol "{lib_name}:'):
        sym_text = sym_text.replace(f'(symbol "{sym_name}"', f'(symbol "{lib_name}:{sym_name}"', 1)
    return sym_text

def get_symbol_pins(sym_text, unit=1):
    # If symbol has sub-units with _unit_
    u_pattern = re.compile(r'\(symbol\s+"[^"]+_' + str(unit) + r'_[0-9]+"(.*?)(?=\n[\t ]+\(symbol |\n\t*\)$)', re.DOTALL)
    u_matches = list(u_pattern.finditer(sym_text))
    search_text = sym_text
    if u_matches:
        search_text = "\n".join([m.group(1) for m in u_matches])
        
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

print("Symbol extraction engine ready.")
