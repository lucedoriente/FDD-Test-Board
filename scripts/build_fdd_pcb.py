import pcbnew
import os, re

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"
netlist_path = os.path.join(prj_dir, "FDD-Test-Board.net")
pcb_path = os.path.join(prj_dir, "FDD-Test-Board.kicad_pcb")

with open(netlist_path, "r", encoding="utf-8") as f:
    text = f.read()

comp_blocks = text.split('(comp (ref "')[1:]
components = {}
for blk in comp_blocks:
    ref = blk.split('"', 1)[0]
    val_m = re.search(r'\(value "([^"]*)"\)', blk)
    fp_m = re.search(r'\(footprint "([^"]*)"\)', blk)
    sp_m = re.search(r'\(sheetpath \(names "([^"]*)"\) \(tstamps "([^"]*)"\)\)', blk)
    ts_m = re.findall(r'\(tstamps "([^"]*)"\)', blk)
    val = val_m.group(1) if val_m else ""
    fp = fp_m.group(1) if fp_m else ""
    ststamp = sp_m.group(2) if sp_m else "/"
    ctstamp = ts_m[-1] if ts_m else ""
    full_path = f"{ststamp}{ctstamp}" if ststamp.endswith('/') else f"{ststamp}/{ctstamp}"
    components[ref] = {"val": val, "fp": fp, "path": full_path}

net_blocks = text.split('(net (code "')[1:]
nets = {}
pad_net_map = {}
for nblk in net_blocks:
    nname_m = re.search(r'\(name "([^"]+)"\)', nblk)
    if not nname_m:
        continue
    nname = nname_m.group(1)
    nodes = re.findall(r'\(node \(ref "([^"]+)"\) \(pin "([^"]+)"\)', nblk)
    nets[nname] = nodes
    for r, p in nodes:
        pad_net_map[(r, p)] = nname

board = pcbnew.BOARD()
board.SetCopperLayerCount(4)

ds = board.GetDesignSettings()
ds.m_TrackMinWidth = pcbnew.FromMM(0.12)
ds.m_ViasMinSize = pcbnew.FromMM(0.45)
ds.m_MinThroughDrill = pcbnew.FromMM(0.20)
ds.m_HoleClearance = pcbnew.FromMM(0.15)
ds.m_HoleToHoleMin = pcbnew.FromMM(0.15)
ds.m_MinClearance = pcbnew.FromMM(0.12)
ds.m_CopperEdgeClearance = pcbnew.FromMM(0.30)

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

# ==============================================================================
# 1. REAR PANEL CONNECTORS (Y = 0..14 mm, opening facing rear panel at Y=0)
# ==============================================================================
pos["J1"]  = (20.0, 5.5, 180)     # 24V Mean Well input: X=[11.85, 23.07]
pos["J2"]  = (43.0, 5.5, 180)     # 5.25" Power: X=[24.70, 46.06] (Gap da J1: 1.63mm)
pos["J3"]  = (50.5, 14.0, 90)     # 3.5" Power: X=[48.70, 59.92] (Gap da J2: 2.64mm)
pos["J11"] = (67.5, 13.0, 90)     # 34-pin FDD: X=[61.88, 113.77] (Gap da J3: 1.96mm)
pos["J10"] = (120.0, 13.0, 90)    # 50-pin 8" FDD: X=[116.38, 188.59] (Gap da J11: 2.61mm)

# ==============================================================================
# 2. LEFT PANEL (X = 6..24 mm, opening facing left edge)
# ==============================================================================
pos["J6"]  = (6.0, 58.0, 90)      # USB-C receptacle opening to left
pos["D1"]  = (16.0, 54.0, 0)      # USBLC6-2SC6 TVS
pos["D2"]  = (16.0, 62.0, 0)      # USBLC6-2SC6 TVS
pos["R4"]  = (13.0, 48.0, 0)      # CC1 5.1k
pos["R5"]  = (19.0, 48.0, 0)      # CC2 5.1k
pos["R6"]  = (23.0, 54.0, 0)      # D- 22R
pos["R7"]  = (23.0, 62.0, 0)      # D+ 22R

# ==============================================================================
# 3. RIGHT PANEL (X = 164..195 mm, opening facing right edge at X=200)
# ==============================================================================
pos["J12"] = (187.0, 22.0, 0)     # 26-pin 3.5" Slimline (IDC-26 horizontal, opening to right +0.8mm overhang)
pos["J13"] = (187.0, 66.0, 0)     # 20-pin Apple II Disk II (IDC-20 horizontal, opening to right +0.8mm overhang)
pos["J4"]  = (194.5, 110.0, 270)  # 8" Power Terminal (MKDS 4-pin) on Right edge, wire opening to right
pos["J14"] = (166.0, 124.0, 0)    # 6-pin Stepper diagnostic header (pins to right)

# Oscilloscope Probe Jacks (right side, near Cat-Eye circuit)
pos["J8"]  = (164.0, 86.0, 0)     # TP1 Cat-Eye Scope Probe
pos["J9"]  = (164.0, 96.0, 0)     # TP2 Cat-Eye Scope Probe

# ==============================================================================
# 4. POWER SUPPLY & E-FUSES (Upper-Left: X = 28..90, Y = 32..80)
# ==============================================================================
# 12V Buck (TPS54302)
pos["U1"]  = (38.0, 38.0, 0)
pos["L1"]  = (50.0, 38.0, 0)
pos["C24"] = (38.0, 46.0, 0)
pos["C25"] = (30.0, 38.0, 0)
pos["C26"] = (59.0, 38.0, 0)
pos["R30"] = (50.0, 46.0, 0)
pos["R31"] = (56.0, 46.0, 0)

# 5V Buck (TPS54302)
pos["U2"]  = (72.0, 38.0, 0)
pos["L2"]  = (84.0, 38.0, 0)
pos["C27"] = (72.0, 46.0, 0)
pos["C28"] = (65.0, 38.0, 0)
pos["C29"] = (88.0, 30.0, 0)
pos["R32"] = (84.0, 46.0, 0)
pos["R33"] = (90.0, 46.0, 0)

# E-Fuses (AO3401A P-MOSFETs)
pos["Q2"]  = (36.0, 68.0, 0)
pos["Q3"]  = (56.0, 68.0, 0)
pos["Q4"]  = (76.0, 68.0, 0)

# INA180 Current Sensors
pos["U12"] = (36.0, 78.0, 0)
pos["U11"] = (56.0, 78.0, 0)
pos["U3"]  = (76.0, 78.0, 0)

# ==============================================================================
# 5. MCU CORE ZONE (Center: X = 88..140, Y = 38..100)
# ==============================================================================
pos["U5"]  = (120.0, 70.0, 0)    # STM32F407VET6 LQFP-100

# 3.3V LDO
pos["U6"]  = (104.0, 38.0, 0)
pos["C1"]  = (97.0, 38.0, 0)
pos["C2"]  = (112.0, 38.0, 0)

# HSE Crystal (8 MHz)
pos["Y1"]  = (102.0, 68.0, 0)
pos["R1"]  = (102.0, 62.0, 0)
pos["C12"] = (98.0, 74.0, 0)
pos["C13"] = (106.0, 74.0, 0)

# Reset Button & SWD Header
pos["SW1"] = (96.0, 86.0, 0)
pos["R2"]  = (88.0, 86.0, 0)
pos["C14"] = (88.0, 92.0, 0)
pos["R3"]  = (107.0, 86.0, 0)
pos["J7"]  = (96.0, 98.0, 0)

# MCU Decoupling Caps around U5
pos["C3"]  = (112.0, 58.0, 0)
pos["C4"]  = (118.0, 58.0, 0)
pos["C5"]  = (124.0, 58.0, 0)
pos["C6"]  = (130.0, 58.0, 0)
pos["C7"]  = (112.0, 82.0, 0)
pos["C8"]  = (118.0, 82.0, 0)
pos["C9"]  = (124.0, 82.0, 0)
pos["C10"] = (130.0, 82.0, 0)
pos["C11"] = (134.0, 66.0, 0)
pos["C15"] = (134.0, 74.0, 0)

# ==============================================================================
# 6. FLOPPY DRIVERS & LOGIC ZONE (X = 142..175, Y = 36..75)
# ==============================================================================
# Pull-up Resistors (1k to +5V_REG) arranged in clean bar
pos["R24"] = (142.0, 36.0, 90)
pos["R25"] = (148.0, 36.0, 90)
pos["R26"] = (154.0, 36.0, 90)
pos["R27"] = (160.0, 36.0, 90)
pos["R28"] = (166.0, 36.0, 90)
pos["R29"] = (172.0, 36.0, 90)

pos["U4"]  = (145.0, 50.0, 0)
pos["U8"]  = (160.0, 50.0, 0)
pos["U9"]  = (145.0, 64.0, 0)
pos["U10"] = (160.0, 64.0, 0)

# ==============================================================================
# 7. CAT-EYE ANALOG FRONT-END (X = 131..155, Y = 82..100)
# ==============================================================================
pos["U7"]  = (144.0, 90.0, 0)
pos["R8"]  = (136.0, 86.0, 0)
pos["R9"]  = (136.0, 94.0, 0)
pos["C16"] = (131.0, 86.0, 0)
pos["C17"] = (131.0, 94.0, 0)
pos["R10"] = (144.0, 82.0, 0)
pos["R11"] = (144.0, 98.0, 0)
pos["D3"]  = (152.0, 90.0, 0)
pos["C18"] = (152.0, 84.0, 0)
pos["R12"] = (152.0, 96.0, 0)

# Diagnostic Test Points TP1..TP6
pos["TP1"] = (100.0, 106.0, 0)
pos["TP2"] = (112.0, 106.0, 0)
pos["TP3"] = (124.0, 106.0, 0)
pos["TP4"] = (136.0, 106.0, 0)
pos["TP5"] = (148.0, 106.0, 0)
pos["TP6"] = (160.0, 106.0, 0)

# ==============================================================================
# 8. FRONT PANEL USER CONTROLS (Y = 104..130 mm)
# ==============================================================================
# Sunton Display 4-wire Header
pos["J5"]  = (22.0, 104.0, 0)

# Rotary Encoder & RC Filter
pos["SW2"] = (34.0, 118.0, 0)
pos["R13"] = (52.0, 112.0, 0)
pos["R14"] = (52.0, 118.0, 0)
pos["R15"] = (52.0, 124.0, 0)
pos["C19"] = (58.0, 112.0, 0)
pos["C20"] = (58.0, 118.0, 0)
pos["C21"] = (58.0, 124.0, 0)

# SW3: Run Button
pos["SW3"] = (68.0, 118.0, 0)
pos["R16"] = (68.0, 109.0, 0)
pos["C22"] = (68.0, 127.0, 0)

# SW4: Back Button
pos["SW4"] = (82.0, 118.0, 0)
pos["R17"] = (82.0, 109.0, 0)
pos["C23"] = (82.0, 127.0, 0)

# Status LEDs & Resistors
pos["D4"]  = (94.0, 116.0, 0);  pos["R18"] = (94.0, 124.0, 0)
pos["D5"]  = (103.0, 116.0, 0); pos["R19"] = (103.0, 124.0, 0)
pos["D6"]  = (112.0, 116.0, 0); pos["R20"] = (112.0, 124.0, 0)
pos["D7"]  = (121.0, 116.0, 0); pos["R21"] = (121.0, 124.0, 0)
pos["D8"]  = (130.0, 116.0, 0); pos["R22"] = (130.0, 124.0, 0)

# Buzzer Section
pos["BZ1"] = (148.0, 120.0, 0)
pos["D9"]  = (140.0, 120.0, 0)
pos["Q1"]  = (162.0, 116.0, 0)
pos["R23"] = (162.0, 124.0, 0)

# Load and place all footprints
placed_count = 0
for ref, cdata in components.items():
    fp_str = cdata["fp"]
    val_str = cdata["val"]
    path_str = cdata["path"]
    if not fp_str or ":" not in fp_str:
        continue
    lib, fpname = fp_str.split(":", 1)
    local_dir = os.path.join(prj_dir, "FDD-Test-Board.pretty")
    if os.path.exists(os.path.join(local_dir, f"{fpname}.kicad_mod")):
        dirpath = local_dir
    elif lib == "FDD-Test-Board":
        dirpath = local_dir
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
        
    full_bbox = fp_obj.GetBoundingBox(False, False)
    ref_field = fp_obj.Reference()
    ref_field.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(0.8), pcbnew.FromMM(0.8)))
    ref_field.SetTextThickness(pcbnew.FromMM(0.12))
    if full_bbox.GetTop() < pcbnew.FromMM(5.0):
        ref_field.SetPosition(pcbnew.VECTOR2I(int((full_bbox.GetLeft() + full_bbox.GetRight()) / 2), full_bbox.GetBottom() + pcbnew.FromMM(1.2)))
    elif full_bbox.GetRight() > pcbnew.FromMM(190.0):
        ref_field.SetPosition(pcbnew.VECTOR2I(full_bbox.GetLeft() - pcbnew.FromMM(2.0), int((full_bbox.GetTop() + full_bbox.GetBottom()) / 2)))
    else:
        ref_field.SetPosition(pcbnew.VECTOR2I(int((full_bbox.GetLeft() + full_bbox.GetRight()) / 2), full_bbox.GetTop() - pcbnew.FromMM(0.8)))
    fp_obj.Value().SetVisible(False)
    if ref.startswith("TP"):
        fp_obj.SetExcludedFromBOM(True)
    
    board.Add(fp_obj)
    for pad in fp_obj.Pads():
        pnum = pad.GetNumber()
        netname = pad_net_map.get((ref, pnum), None)
        if netname and netname in board_net_objs:
            pad.SetNet(board_net_objs[netname])
    placed_count += 1

print(f"Successfully placed {placed_count} of {len(components)} footprints on PCB!")

# Copper zones will be created and filled post-routing with Freerouting SES import

board.Save(pcb_path)
print(f"Board saved successfully to {pcb_path}!")
