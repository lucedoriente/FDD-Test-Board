import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

ls_idx = text.find('(lib_symbols')
ls_end = text.find('\n  (symbol (lib_id')
ls = text[ls_idx:ls_end]

sym_names = re.findall(r'\(symbol "([^"]+)"', ls)
exts = re.findall(r'\(extends "([^"]+)"\)', ls)
print("Symbols in MCU lib_symbols:", sym_names)
print("Extends in MCU lib_symbols:", exts)
