import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

insts = re.findall(r'\(symbol \(lib_id "([^"]+)"\)', text)
print("Symbol instances in Sheet 2:", len(insts))
print("Sample lib_ids:", insts[:10])

# Look at U5 instance
idx = text.find('(property "Reference" "U5"')
if idx != -1:
    s_idx = text.rfind('(symbol ', 0, idx)
    e_idx = text.find('  )', idx)
    print("U5 instance:\n", text[s_idx:e_idx+3])
