import os, subprocess, re
import pcbnew

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester"
kicad_dir = os.path.join(PRJ_DIR, "kicad")
scripts_dir = os.path.join(PRJ_DIR, "scripts")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"
builder_file = os.path.join(scripts_dir, "build_zero_erc_fdd_v2.py")

with open(builder_file, "r", encoding="utf-8") as f:
    txt = f.read()

# Replace footprints in builder to point to FDD-Test-Board local library
txt = txt.replace('"Inductor_SMD:L_7.3x7.3_H4.5"', '"FDD-Test-Board:L_7.3x7.3_H4.5"')
txt = txt.replace('"Connector_IDC:IDC-Header_2x25_P2.54mm_Horizontal"', '"FDD-Test-Board:IDC-Header_2x25_P2.54mm_Horizontal"')
txt = txt.replace('"Connector_IDC:IDC-Header_2x17_P2.54mm_Horizontal"', '"FDD-Test-Board:IDC-Header_2x17_P2.54mm_Horizontal"')
txt = txt.replace('"Connector_IDC:IDC-Header_2x13_P2.54mm_Horizontal"', '"FDD-Test-Board:IDC-Header_2x13_P2.54mm_Horizontal"')
txt = txt.replace('"Connector_IDC:IDC-Header_2x10_P2.54mm_Horizontal"', '"FDD-Test-Board:IDC-Header_2x10_P2.54mm_Horizontal"')
txt = txt.replace('"Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Horizontal"', '"FDD-Test-Board:PinHeader_1x04_P2.54mm_Horizontal"')

with open(builder_file, "w", encoding="utf-8") as f:
    f.write(txt)

print("Rebuilding schematics with matching FDD-Test-Board library IDs...")
subprocess.run([r"C:\Program Files\KiCad\9.0\bin\python.exe", builder_file], capture_output=True, text=True)

# Also save J3 in local pretty so it matches FDD-Test-Board:PinHeader_1x04_P2.54mm_Horizontal
local_pretty = os.path.join(kicad_dir, "FDD-Test-Board.pretty")
for target in ["FDD-Test-Board-nozones.kicad_pcb", "FDD-Test-Board.kicad_pcb"]:
    board = pcbnew.LoadBoard(os.path.join(kicad_dir, target))
    j3 = board.FindFootprintByReference("J3")
    if j3:
        j3.SetFPID(pcbnew.LIB_ID("FDD-Test-Board", "PinHeader_1x04_P2.54mm_Horizontal"))
        pcbnew.FootprintSave(local_pretty, j3)
    board.Save(os.path.join(kicad_dir, target))

# Check parity
drc_rpt = os.path.join(kicad_dir, "FDD-Test-Board-parity-check.rpt")
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "--output", drc_rpt, os.path.join(kicad_dir, "FDD-Test-Board.kicad_pcb")]
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"DRC CLI Exit Code: {res.returncode}")
with open(drc_rpt, "r", encoding="utf-8") as f:
    for line in f:
        if any(k in line.lower() for k in ['parity', 'footprint', 'violation', 'error', 'found']):
            print("  ", line.strip())
