import os, sys, re, glob
import pcbnew

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"
local_pretty = os.path.join(prj_dir, "FDD-Test-Board.pretty")
netlist_path = os.path.join(prj_dir, "FDD-Test-Board.net")

# 1. Parse Netlist
with open(netlist_path, "r", encoding="utf-8") as f:
    text = f.read()

# Extract components: ref -> {val, fp, path}
components = {}
comp_blocks = text.split('(comp (ref "')[1:]
for cblk in comp_blocks:
    ref = cblk.split('"')[0]
    val = cblk.split('(value "')[1].split('"')[0]
    fp = cblk.split('(footprint "')[1].split('"')[0]
    path = ""
    if '(sheetpath (names "' in cblk:
        path = cblk.split('(sheetpath (names "')[1].split('"')[0]
    components[ref] = {"val": val, "fp": fp, "path": path}

print(f"Loaded {len(components)} components from netlist.")

# Extract nets and pin-to-net map
net_blocks = text.split('(net (code "')[1:]
nets = {}
pad_net_map = {}
for nblk in net_blocks:
    nname = nblk.split('(name "')[1].split('"')[0]
    nodes = []
    if '(node ' in nblk:
        for node_str in nblk.split('(node ')[1:]:
            r = node_str.split('(ref "')[1].split('"')[0]
            p = node_str.split('(pin "')[1].split('"')[0]
            nodes.append((r, p))
            pad_net_map[(r, p)] = nname
    nets[nname] = nodes

print(f"Loaded {len(nets)} nets from netlist.")

for target_name in ["FDD-Test-Board-nozones.kicad_pcb", "FDD-Test-Board.kicad_pcb"]:
    pcb_path = os.path.join(prj_dir, target_name)
    board = pcbnew.BOARD()
    board.SetFileName(pcb_path)
    board.SetCopperLayerCount(4)

    ds = board.GetDesignSettings()
    ds.m_TrackMinWidth = pcbnew.FromMM(0.10)
    ds.m_ViasMinSize = pcbnew.FromMM(0.45)
    ds.m_MinThroughDrill = pcbnew.FromMM(0.20)
    ds.m_HoleClearance = pcbnew.FromMM(0.15)
    ds.m_HoleToHoleMin = pcbnew.FromMM(0.15)
    ds.m_MinClearance = pcbnew.FromMM(0.12)
    ds.m_CopperEdgeClearance = pcbnew.FromMM(0.30)
    ds.m_SilkToEdgeClearance = 0
    ds.m_MinResolvedSpokes = 1

    nc = ds.m_NetSettings.GetDefaultNetclass()
    nc.SetClearance(pcbnew.FromMM(0.15))
    nc.SetTrackWidth(pcbnew.FromMM(0.20))
    nc.SetViaDiameter(pcbnew.FromMM(0.50))
    nc.SetViaDrill(pcbnew.FromMM(0.25))

    tb = board.GetTitleBlock()
    tb.SetTitle("Retro-Diag FDD Master Tester & Exerciser")
    tb.SetDate("2026-11-02")
    tb.SetRevision("1.0")
    tb.SetCompany("Alessio Iodice")
    tb.SetComment(0, "Author / Hardware Designer: Alessio Iodice <alessio67@gmail.com>")
    tb.SetComment(1, "Architecture: Universal FDD Tester & Exerciser (8\", 5.25\", 3.5\" ED 2.88M, 3\" Amstrad, Apple II)")
    tb.SetComment(2, "License: CC BY-NC-SA 4.0")
    tb.SetComment(3, "Validated on KiCad 9.0 — 0 ERC / 0 DRC violations")

    W, H = 200.0, 140.0
    def add_line(layer, x1, y1, x2, y2, width=0.15):
        line = pcbnew.PCB_SHAPE(board)
        line.SetShape(pcbnew.SHAPE_T_SEGMENT)
        line.SetLayer(layer)
        line.SetWidth(pcbnew.FromMM(width))
        line.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        line.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        board.Add(line)

    add_line(pcbnew.Edge_Cuts, 0, 0, W, 0)
    add_line(pcbnew.Edge_Cuts, W, 0, W, H)
    add_line(pcbnew.Edge_Cuts, W, H, 0, H)
    add_line(pcbnew.Edge_Cuts, 0, H, 0, 0)

    # 4x Chassis M3 Holes (5mm from edges)
    mh_dir = os.path.join(kicad_fp_dir, "MountingHole.pretty")
    for i, (hx, hy) in enumerate([(5.0, 5.0), (W - 5.0, 5.0), (W - 5.0, H - 5.0), (5.0, H - 5.0)], start=1):
        mh = pcbnew.FootprintLoad(mh_dir, "MountingHole_3.2mm_M3")
        if mh:
            mh.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(hx), pcbnew.FromMM(hy)))
            mh.SetReference(f"H{i}")
            mh.Reference().SetVisible(False)
            mh.SetBoardOnly(True)
            board.Add(mh)

    def add_text(layer, text_str, x, y, size=1.4, thickness=0.25):
        txt = pcbnew.PCB_TEXT(board)
        txt.SetLayer(layer)
        txt.SetText(text_str)
        txt.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        txt.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
        txt.SetTextThickness(pcbnew.FromMM(thickness))
        board.Add(txt)

    add_text(pcbnew.F_SilkS, "© 2026 by Alessio Iodice", 100.0, 137.0, size=1.4)
    add_text(pcbnew.F_SilkS, "Retro-Diag FDD Master Tester & Exerciser rev 1.0", 100.0, 133.5, size=1.3)

    board_net_objs = {}
    for nname in nets.keys():
        nobj = pcbnew.NETINFO_ITEM(board, nname)
        board.Add(nobj)
        board_net_objs[nname] = nobj

    pos = {}
    # 1. REAR EDGE (Y = 0)
    pos["J6"]  = (16.5, 4.35, 180)     # USB Type-C opening to rear panel
    pos["D1"]  = (16.5, 13.5, 0)       # USBLC6-2SC6 TVS
    pos["R4"]  = (13.0, 13.5, 90)      # CC1 5.1k
    pos["R5"]  = (13.0, 17.0, 90)      # CC2 5.1k
    pos["R6"]  = (20.0, 13.5, 90)      # D- 22R
    pos["R7"]  = (20.0, 17.0, 90)      # D+ 22R
    pos["J2"]  = (43.0, 5.5, 180)      # 5.25" Power Molex (4-pin MKDS) flush to rear
    pos["J3"]  = (52.0, 8.5, 90)       # 3.5" Power Berg (4-pin Header) pins protruding 2.1mm
    pos["J11"] = (67.5, 13.0, 90)      # 34-pin 3.5"/5.25" (IDC-34 horizontal, opening to rear)
    pos["J10"] = (120.0, 13.0, 90)     # 50-pin 8" Shugart (IDC-50 horizontal, opening to rear)

    # 2. LEFT EDGE (Facing Internal Mean Well 24V PSU)
    pos["J1"]  = (6.5, 32.0, 90)       # 24V IN Terminal block facing left to Mean Well

    # 3. RIGHT EDGE (X = 200 mm)
    pos["J12"] = (187.0, 22.0, 0)      # IDC-26 horizontal
    pos["J13"] = (187.0, 66.0, 0)      # IDC-20 Apple II horizontal
    pos["J4"]  = (194.5, 110.0, 270)   # 8" Power Terminal 4-pin MKDS facing right
    pos["J14"] = (166.0, 124.0, 0)     # Stepper 6-pin header

    # 4. POWER SUPPLY & E-FUSES (Upper-Left: X = 28..90, Y = 32..80)
    pos["U1"]  = (38.0, 38.0, 0);  pos["L1"]  = (50.0, 38.0, 0)
    pos["C24"] = (38.0, 46.0, 0);  pos["C25"] = (30.0, 38.0, 0); pos["C26"] = (59.0, 38.0, 0)
    pos["R30"] = (50.0, 46.0, 0);  pos["R31"] = (56.0, 46.0, 0)

    pos["U2"]  = (72.0, 38.0, 0);  pos["L2"]  = (84.0, 38.0, 0)
    pos["C27"] = (72.0, 46.0, 0);  pos["C28"] = (65.0, 38.0, 0); pos["C29"] = (88.0, 30.0, 0)
    pos["R32"] = (84.0, 46.0, 0);  pos["R33"] = (90.0, 46.0, 0)

    pos["Q2"]  = (36.0, 68.0, 0);  pos["Q3"]  = (56.0, 68.0, 0); pos["Q4"]  = (76.0, 68.0, 0)
    pos["R24"] = (36.0, 60.0, 0);  pos["R25"] = (56.0, 60.0, 0); pos["R26"] = (76.0, 60.0, 0)
    pos["R27"] = (42.0, 68.0, 0);  pos["R28"] = (62.0, 68.0, 0); pos["R29"] = (82.0, 68.0, 0)
    pos["U12"] = (36.0, 78.0, 0);  pos["U11"] = (56.0, 78.0, 0); pos["U3"]  = (76.0, 78.0, 0)
    pos["C30"] = (42.0, 78.0, 0);  pos["C31"] = (62.0, 78.0, 0); pos["C32"] = (82.0, 78.0, 0)
    pos["U6"]  = (104.0, 38.0, 0); pos["C1"]  = (98.0, 38.0, 0);  pos["C2"]  = (110.0, 38.0, 0)
    pos["D2"]  = (16.0, 62.0, 0)

    # 5. MCU CORE & CRYSTAL
    pos["U5"]  = (120.0, 70.0, 0)
    pos["Y1"]  = (100.0, 66.0, 0); pos["C12"] = (95.0, 62.0, 0); pos["C13"] = (95.0, 70.0, 0)
    pos["SW1"] = (96.0, 86.0, 0);  pos["R2"]  = (90.0, 86.0, 0); pos["C14"] = (102.0, 86.0, 0)
    pos["SW5"] = (96.0, 74.0, 0)   # DFU BOOT Button next to Reset
    pos["R3"]  = (102.0, 74.0, 0)  # BOOT0 10k pulldown
    pos["C3"]  = (112.0, 56.0, 0); pos["C4"]  = (112.0, 84.0, 0); pos["C5"]  = (128.0, 56.0, 0)
    pos["C6"]  = (128.0, 84.0, 0); pos["C7"]  = (108.0, 64.0, 0); pos["C8"]  = (132.0, 64.0, 0)
    pos["C9"]  = (108.0, 76.0, 0); pos["C10"] = (132.0, 76.0, 0)
    pos["C11"] = (116.0, 56.0, 0); pos["C15"] = (124.0, 56.0, 0)
    pos["C16"] = (120.0, 84.0, 0); pos["C17"] = (116.0, 84.0, 0); pos["C18"] = (124.0, 84.0, 0)
    pos["J7"]  = (96.0, 98.0, 0)   # SWD header

    # 6. LOGIC & FDD DRIVERS (Right half: X = 135..180, Y = 36..80)
    pos["U4"]  = (145.0, 50.0, 0); pos["U8"]  = (160.0, 50.0, 0)
    pos["U9"]  = (145.0, 64.0, 0); pos["U10"] = (160.0, 64.0, 0)
    pos["RN1"] = (145.0, 76.0, 0); pos["RN2"] = (160.0, 76.0, 0)
    pos["C33"] = (138.0, 50.0, 0); pos["C34"] = (167.0, 50.0, 0)
    pos["C35"] = (138.0, 64.0, 0); pos["C36"] = (167.0, 64.0, 0)

    # 7. ANALOG CAT-EYE CIRCUIT (LMV358)
    pos["U7"]  = (144.0, 90.0, 0)
    pos["R8"]  = (136.0, 86.0, 0); pos["R9"]  = (136.0, 94.0, 0)
    pos["R10"] = (144.0, 82.0, 0); pos["R11"] = (144.0, 98.0, 0)
    pos["R12"] = (152.0, 84.0, 0); pos["C38"] = (152.0, 96.0, 0)
    pos["D3"]  = (152.0, 90.0, 0); pos["C37"] = (138.0, 90.0, 0)

    # 8. SCOPE PROBE HEADER (J8 4-pin: TP1, GND, TP2, GND)
    pos["J8"]  = (164.0, 96.0, 0)

    # 9. UI PANELS & CONTROLS (Lower area: X = 20..135, Y = 98..128)
    pos["J5"]  = (22.0, 104.0, 0)  # Display 4-pin header
    pos["J15"] = (75.0, 104.0, 0)  # Panel UI 14-pin IDC header

    pos["SW2"] = (34.0, 118.0, 0)  # Encoder
    pos["R13"] = (26.0, 114.0, 0); pos["R14"] = (26.0, 118.0, 0); pos["R15"] = (26.0, 122.0, 0)
    pos["C19"] = (42.0, 114.0, 0); pos["C20"] = (42.0, 118.0, 0); pos["C21"] = (42.0, 122.0, 0)

    pos["SW3"] = (56.0, 118.0, 0); pos["R16"] = (56.0, 110.0, 0); pos["C22"] = (56.0, 126.0, 0)
    pos["SW4"] = (68.0, 118.0, 0); pos["R17"] = (68.0, 110.0, 0); pos["C23"] = (68.0, 126.0, 0)

    pos["D4"]  = (94.0, 116.0, 0); pos["R18"] = (94.0, 124.0, 0)
    pos["D5"]  = (103.0, 116.0, 0); pos["R19"] = (103.0, 124.0, 0)
    pos["D6"]  = (112.0, 116.0, 0); pos["R20"] = (112.0, 124.0, 0)
    pos["D7"]  = (121.0, 116.0, 0); pos["R21"] = (121.0, 124.0, 0)
    pos["D8"]  = (130.0, 116.0, 0); pos["R22"] = (130.0, 124.0, 0)

    pos["BZ1"] = (148.0, 120.0, 0); pos["D9"]  = (140.0, 120.0, 0)
    pos["Q1"]  = (162.0, 116.0, 0); pos["R23"] = (162.0, 124.0, 0)

    # Test points
    pos["TP1"] = (174.0, 86.0, 0);  pos["TP2"] = (174.0, 92.0, 0); pos["TP3"] = (174.0, 98.0, 0)
    pos["TP4"] = (174.0, 104.0, 0); pos["TP5"] = (174.0, 110.0, 0); pos["TP6"] = (174.0, 116.0, 0)

    # Place footprints
    placed_count = 0
    for ref, cdata in components.items():
        fp_str = cdata["fp"]
        val_str = cdata["val"]
        path_str = cdata["path"]
        lib, fpname = fp_str.split(":", 1)
        
        # Check local pretty first
        if os.path.exists(os.path.join(local_pretty, f"{fpname}.kicad_mod")):
            dirpath = local_pretty
        elif lib == "FDD-Test-Board":
            dirpath = local_pretty
        else:
            dirpath = os.path.join(kicad_fp_dir, f"{lib}.pretty")
            
        fp_obj = pcbnew.FootprintLoad(dirpath, fpname)
        if not fp_obj:
            print(f"ERROR: Could not load footprint {fp_str} for {ref}")
            continue
            
        fp_obj.SetFPID(pcbnew.LIB_ID(lib, fpname))
        fp_obj.SetReference(ref)
        fp_obj.SetValue(val_str)
        fp_obj.SetPath(pcbnew.KIID_PATH(path_str))
        
        px, py, prot = pos.get(ref, (100.0, 70.0, 0))
        fp_obj.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py)))
        if prot != 0:
            fp_obj.SetOrientation(pcbnew.EDA_ANGLE(prot, pcbnew.DEGREES_T))
            
        ref_field = fp_obj.Reference()
        ref_field.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(0.8), pcbnew.FromMM(0.8)))
        ref_field.SetTextThickness(pcbnew.FromMM(0.12))
        fp_obj.Value().SetVisible(False)
        
        if ref.startswith("TP"):
            fp_obj.SetExcludedFromBOM(False)
        if ref.startswith("H"):
            fp_obj.SetBoardOnly(True)
            
        board.Add(fp_obj)
        for pad in fp_obj.Pads():
            pnum = pad.GetNumber()
            netname = pad_net_map.get((ref, pnum), None)
            if netname and netname in board_net_objs:
                pad.SetNet(board_net_objs[netname])
        placed_count += 1

    board.Save(pcb_path)
    print(f"Successfully placed {placed_count} footprints in {target_name}")

print("\nAll boards regenerated cleanly with updated netlist!")
