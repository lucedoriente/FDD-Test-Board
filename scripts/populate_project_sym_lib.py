import os, re, subprocess
from test_clean_flatten import get_flattened, extract_raw

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
local_sym_path = os.path.join(prj_dir, "FDD-Test-Board.kicad_sym")

# Flatten the 4 symbols: 2N3904, LMV358, 74LS06, AO3401A
syms_to_flatten = [
    ("Transistor_BJT", "2N3904"),
    ("Amplifier_Operational", "LMV358"),
    ("74xx", "74LS06"),
    ("Transistor_FET", "AO3401A"),
]

local_sym_bodies = []
for lib, sname in syms_to_flatten:
    flat = get_flattened(lib, sname)
    # in .kicad_sym file, symbol name should NOT have library prefix
    # flat starts with (symbol "lib:sname"
    flat_no_lib = flat.replace(f'(symbol "{lib}:{sname}"', f'(symbol "{sname}"', 1)
    local_sym_bodies.append(flat_no_lib)

local_sym_file_content = f"""(kicad_symbol_lib
  (version 20231120)
  (generator "kicad_symbol_editor")
  {chr(10).join(local_sym_bodies)}
)
"""

with open(local_sym_path, "w", encoding="utf-8") as f:
    f.write(local_sym_file_content)

print("Saved 4 flattened symbols to FDD-Test-Board.kicad_sym!")
