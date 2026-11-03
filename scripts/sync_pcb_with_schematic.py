import os, sys, re
import pcbnew

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
net_file = os.path.join(PRJ_DIR, "FDD-Test-Board.net")
pcb_nozones = os.path.join(PRJ_DIR, "FDD-Test-Board-nozones.kicad_pcb")
pcb_final = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"

# 1. Parse netlist to get components and nets
with open(net_file, "r", encoding="utf-8") as f:
    net_txt = f.read()

# Extract net mappings: net_name -> list of (ref, pin)
nets_dict = {}
for m in re.finditer(r'\(net \(code "(\d+)"\)\s*\(name "([^"]+)"\)(.*?)\n    \)', net_txt, re.DOTALL):
    code, name, body = m.group(1), m.group(2), m.group(3)
    pins = re.findall(r'\(node \(ref "([^"]+)"\) \(pin "([^"]+)"\)', body)
    nets_dict[name] = pins

print(f"Extracted {len(nets_dict)} nets from netlist.")

# Extract component footprints: ref -> (val, fpid)
comps_dict = {}
for m in re.finditer(r'\(comp \(ref "([^"]+)"\)\s*\(value "([^"]+)"\)\s*\(footprint "([^"]+)"\)', net_txt):
    comps_dict[m.group(1)] = (m.group(2), m.group(3))

print(f"Extracted {len(comps_dict)} components from netlist.")

for target_pcb in [pcb_nozones, pcb_final]:
    print(f"\nProcessing {os.path.basename(target_pcb)}...")
    board = pcbnew.LoadBoard(target_pcb)

    # 1. Remove J9
    j9 = board.FindFootprintByReference("J9")
    if j9:
        print("Deleting old J9...")
        board.Delete(j9)

    # 2. Update/Replace J8 (Conn_01x04)
    j8 = board.FindFootprintByReference("J8")
    if j8 and len(list(j8.Pads())) != 4:
        print("Replacing 2-pin J8 with 4-pin J8...")
        board.Delete(j8)
        j8 = None

    if not j8:
        fpid_j8 = pcbnew.LIB_ID("Connector_PinHeader_2.54mm", "PinHeader_1x04_P2.54mm_Vertical")
        fp_path = os.path.join(fp_dir, "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x04_P2.54mm_Vertical.kicad_mod")
        j8 = pcbnew.FootprintLoad(os.path.dirname(fp_path), "PinHeader_1x04_P2.54mm_Vertical")
        j8.SetReference("J8")
        j8.SetValue("J_SCOPE")
        j8.SetFPID(fpid_j8)
        j8.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(164.0), pcbnew.FromMM(114.0)))
        j8.SetOrientationDegrees(0.0)
        board.Add(j8)
        print("Added 4-pin J8 at (164, 114)")
    else:
        j8.SetValue("J_SCOPE")
        j8.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(164.0), pcbnew.FromMM(114.0)))

    # 3. Add J15 (Conn_02x07)
    j15 = board.FindFootprintByReference("J15")
    if not j15:
        fpid_j15 = pcbnew.LIB_ID("Connector_PinHeader_2.54mm", "PinHeader_2x07_P2.54mm_Vertical")
        fp_path = os.path.join(fp_dir, "Connector_PinHeader_2.54mm.pretty", "PinHeader_2x07_P2.54mm_Vertical.kicad_mod")
        j15 = pcbnew.FootprintLoad(os.path.dirname(fp_path), "PinHeader_2x07_P2.54mm_Vertical")
        j15.SetReference("J15")
        j15.SetValue("J_PANEL_UI")
        j15.SetFPID(fpid_j15)
        j15.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(75.0), pcbnew.FromMM(104.0)))
        j15.SetOrientationDegrees(0.0)
        board.Add(j15)
        print("Added 14-pin J15 at (75, 104)")

    # 4. Add SW5 (SW_BOOT)
    sw5 = board.FindFootprintByReference("SW5")
    if not sw5:
        fpid_sw5 = pcbnew.LIB_ID("Button_Switch_THT", "SW_PUSH_6mm_H5mm")
        fp_path = os.path.join(fp_dir, "Button_Switch_THT.pretty", "SW_PUSH_6mm_H5mm.kicad_mod")
        sw5 = pcbnew.FootprintLoad(os.path.dirname(fp_path), "SW_PUSH_6mm_H5mm")
        sw5.SetReference("SW5")
        sw5.SetValue("SW_BOOT")
        sw5.SetFPID(fpid_sw5)
        # Place next to SW1 (96, 86)
        sw5.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(96.0), pcbnew.FromMM(74.0)))
        sw5.SetOrientationDegrees(0.0)
        board.Add(sw5)
        print("Added SW5 (SW_BOOT) at (96, 74)")

    # 5. Synchronize nets on board from netlist
    # Ensure all net objects exist in board
    for netname in nets_dict.keys():
        net_obj = board.FindNet(netname)
        if not net_obj:
            net_obj = pcbnew.NETINFO_ITEM(board, netname)
            board.AppendNet(net_obj)

    # Assign nets to pads
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

    # Check H1..H4 board only
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

print("\nNetlist synchronization complete.")
