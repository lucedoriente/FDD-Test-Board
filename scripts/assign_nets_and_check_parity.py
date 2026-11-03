import os, sys, re
import pcbnew

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
net_file = os.path.join(PRJ_DIR, "FDD-Test-Board.net")
pcb_nozones = os.path.join(PRJ_DIR, "FDD-Test-Board-nozones.kicad_pcb")
pcb_final = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

with open(net_file, "r", encoding="utf-8") as f:
    net_txt = f.read()

# Extract net mappings: net_name -> list of (ref, pin)
nets_dict = {}
# Split by (net (code
net_blocks = re.split(r'\(net \(code ', net_txt)
for block in net_blocks[1:]:
    name_m = re.search(r'\(name "([^"]+)"\)', block)
    if not name_m: continue
    name = name_m.group(1)
    pins = re.findall(r'\(node \(ref "([^"]+)"\) \(pin "([^"]+)"\)', block)
    nets_dict[name] = pins

print(f"Extracted {len(nets_dict)} nets from netlist.")

for target_pcb in [pcb_nozones, pcb_final]:
    print(f"\nProcessing {os.path.basename(target_pcb)}...")
    board = pcbnew.LoadBoard(target_pcb)

    # 1. Ensure all net objects exist in board
    for netname in nets_dict.keys():
        net_obj = board.FindNet(netname)
        if not net_obj:
            net_obj = pcbnew.NETINFO_ITEM(board, netname)
            board.AppendNet(net_obj)

    # 2. Assign nets to pads
    assigned_count = 0
    for netname, nodes in nets_dict.items():
        net_obj = board.FindNet(netname)
        if not net_obj: continue
        for ref, pin in nodes:
            fp = board.FindFootprintByReference(ref)
            if not fp: continue
            for pad in fp.Pads():
                if pad.GetName() == pin or pad.GetNumber() == pin:
                    pad.SetNet(net_obj)
                    assigned_count += 1

    print(f"Assigned {assigned_count} net connections to pads.")

    # 3. Footprint sync & BOM attributes
    for h in ["H1", "H2", "H3", "H4"]:
        fph = board.FindFootprintByReference(h)
        if fph: fph.SetBoardOnly(True)

    for i in range(1, 7):
        tp = board.FindFootprintByReference(f"TP{i}")
        if tp: tp.SetExcludedFromBOM(False)

    board.GetDesignSettings().m_TrackMinWidth = pcbnew.FromMM(0.10)
    board.GetDesignSettings().m_SilkToEdgeClearance = 0

    board.Save(target_pcb)
    print(f"Saved {os.path.basename(target_pcb)}")

print("\nNetlist assignment complete. Now running DRC & Parity check...")
drc_rpt = os.path.join(PRJ_DIR, "FDD-Test-Board-parity-check.rpt")
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "--output", drc_rpt, pcb_final]
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"DRC CLI Exit Code: {res.returncode}")
with open(drc_rpt, "r", encoding="utf-8") as f:
    for line in f:
        if any(k in line.lower() for k in ['parity', 'footprint', 'violation', 'error', 'unconnected', 'found']):
            print("  ", line.strip())
