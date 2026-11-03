import pcbnew, os, re

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"
netlist_path = os.path.join(prj_dir, "FDD-Test-Board.net")

with open(netlist_path, "r", encoding="utf-8") as f:
    text = f.read()

comp_blocks = text.split('(comp (ref "')[1:]
components = {}
for blk in comp_blocks:
    ref = blk.split('"', 1)[0]
    fp_m = re.search(r'\(footprint "([^"]*)"\)', blk)
    components[ref] = fp_m.group(1) if fp_m else ""

pos = {}

# ==============================================================================
# 1. REAR PANEL CONNECTORS (Y = 10..18 mm, opening to Y=0 / Rear)
# ==============================================================================
pos["J1"]  = (14.0, 10.0, 0)     # 24V In MKDS 2-pin [10.9..22.2, 4.3..15.4]
pos["J2"]  = (28.0, 10.0, 0)     # 5.25" Pwr MKDS 4-pin [24.9..46.3, 4.3..15.4]
pos["J3"]  = (50.0, 14.0, 90)    # 3.5" Pwr 4-pin Berg [47.2..58.4, 3.4..15.8]
pos["J11"] = (68.0, 17.0, 90)    # IDC-34 [62.4..114.3, 3.2..19.4]
pos["J10"] = (125.0, 17.0, 90)   # IDC-50 [119.4..191.6, 3.2..19.4]

# ==============================================================================
# 2. LEFT PANEL (X = 6 mm, opening to -X / Left)
# ==============================================================================
pos["J6"]  = (6.0, 58.0, 90)     # USB-C receptacle opening to left
pos["D1"]  = (16.0, 54.0, 0)
pos["D2"]  = (16.0, 62.0, 0)
pos["R4"]  = (13.0, 48.0, 0)
pos["R5"]  = (19.0, 48.0, 0)
pos["R6"]  = (23.0, 54.0, 0)
pos["R7"]  = (23.0, 62.0, 0)

# ==============================================================================
# 3. RIGHT PANEL (X = 182..188 mm, opening to +X / Right)
# ==============================================================================
pos["J4"]  = (188.0, 30.0, 90)   # 8" Pwr MKDS 4-pin [182.6..193.7, 26.9..38.0]
pos["J12"] = (182.0, 48.0, 0)    # IDC-26 Slimline [179.6..195.8, 42.4..84.1]
pos["J13"] = (182.0, 90.0, 0)    # IDC-20 Apple II [179.6..195.8, 84.4..118.5]
pos["J14"] = (184.0, 122.0, 0)   # 6-pin Stepper [182.2..194.6, 120.2..136.5] -> wait, check MH_195_135!

# Scope Probes (near Cat-Eye front-end)
pos["J8"]  = (164.0, 88.0, 0)
pos["J9"]  = (164.0, 98.0, 0)

# ==============================================================================
# 4. POWER SUPPLY & E-FUSES (Upper-Left: X = 28..88, Y = 36..80)
# ==============================================================================
# 12V Buck
pos["U1"]  = (36.0, 38.0, 0)
pos["L1"]  = (48.0, 38.0, 0)
pos["C24"] = (36.0, 46.0, 0)
pos["C25"] = (28.0, 38.0, 0)
pos["C26"] = (57.0, 38.0, 0)
pos["R30"] = (48.0, 46.0, 0)
pos["R31"] = (54.0, 46.0, 0)

# 5V Buck
pos["U2"]  = (72.0, 38.0, 0)
pos["L2"]  = (84.0, 38.0, 0)
pos["C27"] = (72.0, 46.0, 0)
pos["C28"] = (65.0, 38.0, 0)
pos["C29"] = (93.0, 38.0, 0)
pos["R32"] = (84.0, 46.0, 0)
pos["R33"] = (90.0, 46.0, 0)

# E-Fuses
pos["Q2"]  = (36.0, 68.0, 0)
pos["Q3"]  = (56.0, 68.0, 0)
pos["Q4"]  = (76.0, 68.0, 0)

# INA180
pos["U12"] = (36.0, 78.0, 0)
pos["U11"] = (56.0, 78.0, 0)
pos["U3"]  = (76.0, 78.0, 0)

# ==============================================================================
# 5. MCU CORE ZONE (Center: X = 95..140, Y = 40..95)
# ==============================================================================
pos["U5"]  = (120.0, 70.0, 0)

# 3.3V LDO
pos["U6"]  = (104.0, 38.0, 0)
pos["C1"]  = (97.0, 38.0, 0)
pos["C2"]  = (112.0, 38.0, 0)

# HSE Crystal (8 MHz)
pos["Y1"]  = (102.0, 68.0, 0)
pos["R1"]  = (102.0, 62.0, 0)
pos["C12"] = (98.0, 74.0, 0)
pos["C13"] = (106.0, 74.0, 0)

# Reset Button & SWD
pos["SW1"] = (96.0, 86.0, 0)
pos["R2"]  = (88.0, 86.0, 0)
pos["C14"] = (88.0, 92.0, 0)
pos["R3"]  = (105.0, 86.0, 0)
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
# 7. CAT-EYE ANALOG FRONT-END (X = 135..155, Y = 85..105)
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
# 8. FRONT PANEL CONTROLS (Y = 114..132 mm)
# ==============================================================================
pos["J5"]  = (18.0, 116.0, 0)

pos["SW2"] = (34.0, 118.0, 0)
pos["R13"] = (52.0, 112.0, 0)
pos["R14"] = (52.0, 118.0, 0)
pos["R15"] = (52.0, 124.0, 0)
pos["C19"] = (58.0, 112.0, 0)
pos["C20"] = (58.0, 118.0, 0)
pos["C21"] = (58.0, 124.0, 0)

pos["SW3"] = (68.0, 118.0, 0)
pos["R16"] = (68.0, 109.0, 0)
pos["C22"] = (68.0, 127.0, 0)

pos["SW4"] = (82.0, 118.0, 0)
pos["R17"] = (82.0, 109.0, 0)
pos["C23"] = (82.0, 127.0, 0)

pos["D4"]  = (94.0, 116.0, 0);  pos["R18"] = (94.0, 124.0, 0)
pos["D5"]  = (103.0, 116.0, 0); pos["R19"] = (103.0, 124.0, 0)
pos["D6"]  = (112.0, 116.0, 0); pos["R20"] = (112.0, 124.0, 0)
pos["D7"]  = (121.0, 116.0, 0); pos["R21"] = (121.0, 124.0, 0)
pos["D8"]  = (130.0, 116.0, 0); pos["R22"] = (130.0, 124.0, 0)

pos["BZ1"] = (148.0, 120.0, 0)
pos["D9"]  = (140.0, 120.0, 0)
pos["Q1"]  = (162.0, 116.0, 0)
pos["R23"] = (162.0, 124.0, 0)

# Build and check overlaps
board = pcbnew.BOARD()
mh_dir = os.path.join(kicad_fp_dir, "MountingHole.pretty")

for hx, hy in [(5.0, 5.0), (195.0, 5.0), (195.0, 135.0), (5.0, 135.0)]:
    mh = pcbnew.FootprintLoad(mh_dir, "MountingHole_3.2mm_M3")
    if mh:
        mh.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(hx), pcbnew.FromMM(hy)))
        mh.SetReference(f"MH_{hx:.0f}_{hy:.0f}")
        board.Add(mh)

for ref, (px, py, prot) in pos.items():
    fp_str = components.get(ref, "")
    if not fp_str:
        continue
    lib, fpname = fp_str.split(":", 1)
    dirpath = os.path.join(prj_dir, "FDD-Test-Board.pretty") if lib == "FDD-Test-Board" else os.path.join(kicad_fp_dir, f"{lib}.pretty")
    fp = pcbnew.FootprintLoad(dirpath, fpname)
    if not fp:
        print(f"Failed to load {fp_str}")
        continue
    fp.SetReference(ref)
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py)))
    if prot != 0:
        fp.SetOrientation(pcbnew.EDA_ANGLE(prot, pcbnew.DEGREES_T))
    board.Add(fp)

fps = list(board.GetFootprints())
overlaps = []
for i in range(len(fps)):
    fp1 = fps[i]
    ref1 = fp1.GetReference()
    bb1 = fp1.GetBoundingBox(False, False)
    for j in range(i + 1, len(fps)):
        fp2 = fps[j]
        ref2 = fp2.GetReference()
        bb2 = fp2.GetBoundingBox(False, False)
        if bb1.Intersects(bb2):
            overlaps.append((ref1, ref2, bb1, bb2))

print(f"Total placed footprints: {len(fps)}")
print(f"Total overlapping pairs: {len(overlaps)}")
for r1, r2, b1, b2 in overlaps:
    print(f"  Overlap: {r1} and {r2}")
