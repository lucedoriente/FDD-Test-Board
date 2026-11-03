import pcbnew, os

kicad_fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"
fp = pcbnew.FootprintLoad(os.path.join(kicad_fp_dir, "TerminalBlock_Phoenix.pretty"), "TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal")

for rot in [0, 90, 180, 270]:
    fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(100.0), pcbnew.FromMM(50.0)))
    bb = fp.GetBoundingBox(False, False)
    # Check silkscreen / fab graphics to find wire entry
    print(f"Rot {rot}: X=[{bb.GetLeft()/1e6:.1f}, {bb.GetRight()/1e6:.1f}], Y=[{bb.GetTop()/1e6:.1f}, {bb.GetBottom()/1e6:.1f}]")
