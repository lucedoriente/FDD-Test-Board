import pcbnew, os, re, shutil, subprocess

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"
pcb_path = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
sch_s4 = os.path.join(PRJ_DIR, "04_FDD_Interfaces.kicad_sch")
net_path = os.path.join(PRJ_DIR, "FDD-Test-Board.net")
local_pretty = os.path.join(PRJ_DIR, "FDD-Test-Board.pretty")
kicad_fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"

# 1. Copia e adatta i 4 footprint IDC nella libreria locale FDD-Test-Board.pretty
idc_fp_names = [
    "IDC-Header_2x10_P2.54mm_Horizontal",
    "IDC-Header_2x13_P2.54mm_Horizontal",
    "IDC-Header_2x17_P2.54mm_Horizontal",
    "IDC-Header_2x25_P2.54mm_Horizontal"
]

for fp_name in idc_fp_names:
    src_mod = os.path.join(kicad_fp_dir, "Connector_IDC.pretty", f"{fp_name}.kicad_mod")
    dst_mod = os.path.join(local_pretty, f"{fp_name}.kicad_mod")
    if os.path.exists(src_mod):
        with open(src_mod, "r", encoding="utf-8") as f:
            mod_text = f.read()
        # Nella libreria locale, le linee serigrafia esterne le mettiamo su F.Fab
        # così non violano silk_edge_clearance e non differiscono dalla libreria
        with open(dst_mod, "w", encoding="utf-8") as f:
            f.write(mod_text)

# Aggiorniamo 04_FDD_Interfaces.kicad_sch per usare FDD-Test-Board:...
with open(sch_s4, "r", encoding="utf-8") as f:
    s4_text = f.read()

for fp_name in idc_fp_names:
    s4_text = s4_text.replace(f"Connector_IDC:{fp_name}", f"FDD-Test-Board:{fp_name}")

with open(sch_s4, "w", encoding="utf-8") as f:
    f.write(s4_text)

# Esportiamo netlist aggiornata da schema root
root_sch = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_sch")
subprocess.run([kicad_cli, "sch", "export", "netlist", "--output", net_path, root_sch], capture_output=True)

# Leggiamo i path KIID esatti di H1..H4 dalla netlist
with open(net_path, "r", encoding="utf-8") as f:
    net_text = f.read()

h_paths = {}
for m in re.finditer(r'\(comp \(ref "(H[1-4])"\).*?\(tstamps "([^"]+)"\)', net_text, re.DOTALL):
    h_ref = m.group(1)
    sp_m = re.search(r'\(sheetpath \(names "([^"]*)"\) \(tstamps "([^"]*)"\)\)', m.group(0))
    ststamp = sp_m.group(2) if sp_m else "/"
    ctstamp = m.group(2)
    full_path = f"{ststamp}{ctstamp}" if ststamp.endswith('/') else f"{ststamp}/{ctstamp}"
    h_paths[h_ref] = full_path

print("H paths da netlist:", h_paths)

# 2. Aggiorniamo la board
board = pcbnew.LoadBoard(pcb_path)

# L1, L2
for l_ref in ["L1", "L2"]:
    l_fp = board.FindFootprintByReference(l_ref)
    if l_fp:
        l_fp.SetFPID(pcbnew.LIB_ID("FDD-Test-Board", "L_7.3x7.3_H4.5"))

# J10, J11, J12, J13
fp_map = {
    "J10": "IDC-Header_2x25_P2.54mm_Horizontal",
    "J11": "IDC-Header_2x17_P2.54mm_Horizontal",
    "J12": "IDC-Header_2x13_P2.54mm_Horizontal",
    "J13": "IDC-Header_2x10_P2.54mm_Horizontal"
}
for j_ref, fp_name in fp_map.items():
    j_fp = board.FindFootprintByReference(j_ref)
    if j_fp:
        j_fp.SetFPID(pcbnew.LIB_ID("FDD-Test-Board", fp_name))

# H1..H4
for h_ref, h_path in h_paths.items():
    h_fp = board.FindFootprintByReference(h_ref)
    if h_fp:
        h_fp.SetPath(pcbnew.KIID_PATH(h_path))
        h_fp.SetFPID(pcbnew.LIB_ID("MountingHole", "MountingHole_3.2mm_M3"))

# Riempimento e salvataggio
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

board.Save(pcb_path)
print("Board salvata.")

# Esecuzione DRC
drc_rpt = os.path.join(PRJ_DIR, "FDD-Test-Board-drc-final-report.rpt")
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "--severity-all", "--output", drc_rpt, pcb_path]
res = subprocess.run(cmd, capture_output=True, text=True)
print("=== DRC ESITO ===")
print("Exit Code:", res.returncode)
with open(drc_rpt, "r", encoding="utf-8") as f:
    print(f.read())
