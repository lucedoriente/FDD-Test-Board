import os, re, subprocess

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
root_sch = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_sch")
netlist_path = os.path.join(PRJ_DIR, "FDD-Test-Board.net")
pcb_path = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

with open(r"C:\Program Files\KiCad\9.0\share\kicad\symbols\Mechanical.kicad_sym", "r", encoding="utf-8") as f:
    mech_text = f.read()

# Estraiamo il simbolo MountingHole
sym_match = re.search(r'(\(symbol "MountingHole"\s+.*?\n  \))', mech_text, re.DOTALL)
mh_sym_def = sym_match.group(1) if sym_match else ""

with open(root_sch, "r", encoding="utf-8") as f:
    sch_text = f.read()

# Inseriamo il lib_symbol se non presente
if 'symbol "Mechanical:MountingHole"' not in sch_text:
    mh_sym_in_lib = mh_sym_def.replace('(symbol "MountingHole"', '(symbol "Mechanical:MountingHole"')
    sch_text = sch_text.replace('(lib_symbols\n  )', f'(lib_symbols\n{mh_sym_in_lib}\n  )')

# Istanziamo H1, H2, H3, H4
instances_str = ""
coords = [(50.8, 165.1), (76.2, 165.1), (101.6, 165.1), (127.0, 165.1)]
for i, (x, y) in enumerate(coords, 1):
    h_ref = f"H{i}"
    if f'(property "Reference" "{h_ref}"' not in sch_text:
        uuid_str = f"b20a3201-1001-4001-8001-0000000000{i:02d}"
        inst = f'''  (symbol (lib_id "Mechanical:MountingHole") (at {x:.2f} {y:.2f} 0) (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
    (uuid "{uuid_str}")
    (property "Reference" "{h_ref}" (at {x:.2f} {y-2.54:.2f} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "MountingHole_3.2mm_M3" (at {x:.2f} {y+2.54:.2f} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "MountingHole:MountingHole_3.2mm_M3" (at {x:.2f} {y:.2f} 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at {x:.2f} {y:.2f} 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Mounting Hole without connection" (at {x:.2f} {y:.2f} 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (instances
      (project "FDD-Test-Board"
        (path "/b20a3201-1001-4001-8001-000000000001"
          (reference "{h_ref}") (unit 1)
        )
      )
    )
  )
'''
        instances_str += inst

if instances_str:
    sch_text = sch_text.replace('(sheet_instances', instances_str + '  (sheet_instances')

with open(root_sch, "w", encoding="utf-8") as f:
    f.write(sch_text)

print("Root schematic aggiornato con H1..H4!")

# ERC check
res_erc = subprocess.run([kicad_cli, "sch", "erc", root_sch], capture_output=True, text=True)
print("ERC Output:", res_erc.stdout.strip())

# Netlist export
res_net = subprocess.run([kicad_cli, "sch", "export", "netlist", "--output", netlist_path, root_sch], capture_output=True, text=True)
print("Netlist exported.")
